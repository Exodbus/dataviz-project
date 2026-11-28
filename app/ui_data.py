"""Couche de cache de l'interface : les données sont chargées et harmonisées une seule fois.

Ce qui est en cache (st.cache_data) : chaque année harmonisée, les sous-populations filtrées
et le tableau de l'accueil. Ce qui est en session : les filtres, stockés dans l'URL
(st.query_params) pour pouvoir partager une vue.
"""

from __future__ import annotations

import threading

import pandas as pd
import streamlit as st

from so_ece.analysis.home import home_table
from so_ece.dataset import load_year
from so_ece.download import ensure_data, missing_files
from so_ece.population import Filters, apply_region, select_data_profiles, select_other_devs


@st.cache_resource
def _download_lock() -> threading.Lock:
    return threading.Lock()


def ensure_raw_data() -> None:
    """Télécharge les données si data/raw/ est incomplet (premier lancement, déploiement)."""
    if not missing_files():
        return
    with _download_lock():
        if not missing_files():  # une autre session vient de le faire
            return
        with st.status("Premier lancement : téléchargement des données (≈ 250 Mo, une seule fois)…", expanded=True) as box:
            ensure_data(log=box.write, verify_existing=False)
            box.update(label="Données téléchargées et vérifiées", state="complete", expanded=False)


@st.cache_data(show_spinner="Chargement des données…")
def get_year(year: int) -> pd.DataFrame:
    if missing_files():
        ensure_data(log=lambda _msg: None, verify_existing=False)
    return load_year(year)


@st.cache_data
def data_profiles(year: int, region: str, groups: tuple[str, ...], exp_bands: tuple[str, ...]) -> pd.DataFrame:
    return select_data_profiles(get_year(year), Filters(region, groups, exp_bands))


@st.cache_data
def other_devs_cached(year: int, region: str, exp_bands: tuple[str, ...]) -> pd.DataFrame:
    return select_other_devs(get_year(year), Filters(region, (), exp_bands))


@st.cache_data
def france_all_devs(year: int) -> pd.DataFrame:
    d = apply_region(get_year(year), "Monde")
    return d[d["Country"] == "France"]


@st.cache_data
def home_cached(region: str, groups: tuple[str, ...], exp_bands: tuple[str, ...]) -> pd.DataFrame:
    return home_table(
        data_profiles(2025, region, groups, exp_bands),
        data_profiles(2026, region, groups, exp_bands),
        other_devs_cached(2025, region, exp_bands),
        other_devs_cached(2026, region, exp_bands),
    )


def profiles_for(year: int, f: Filters) -> pd.DataFrame:
    """Profils data/IA de l'année, selon les filtres."""
    return data_profiles(year, f.region, f.groups, f.exp_bands)


def other_devs(year: int, f: Filters) -> pd.DataFrame:
    """Groupe de comparaison : autres développeurs, même région, même expérience."""
    return other_devs_cached(year, f.region, f.exp_bands)


def home(f: Filters) -> pd.DataFrame:
    return home_cached(f.region, f.groups, f.exp_bands)
