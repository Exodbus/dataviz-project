"""Gabarit commun des pages d'axes : en-tête, filtres, et une première vue de départ."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from so_ece.analysis.multi import shares_table
from so_ece.harmonise import warnings_for
from so_ece.labels import sample_status
from so_ece.population import Filters
from ui_charts import grouped_shares
from ui_components import harmonisation_warnings, population
from ui_data import other_devs, profiles_for
from ui_filters import filter_bar


def header(title: str, question: str, branch: str, owner: str) -> Filters:
    st.title(title)
    st.markdown(f"**Question de l'ECE :** {question}")
    st.info(f"Axe en construction sur la branche `{branch}`. Responsable : {owner}.", icon=":material/construction:")
    return filter_bar()


def series_for(f: Filters, column: str) -> list[tuple[str, pd.DataFrame, int, str]]:
    """Séries à afficher selon les filtres : (nom, population, année, description).

    Profils data/IA pour chaque année de la période, puis les autres développeurs
    pour l'année des niveaux si l'option est activée. Une année est ignorée si la question n'y existe pas.
    """
    out = []
    for year in sorted(f.years, reverse=True):
        df = profiles_for(year, f)
        if column in df.columns:
            out.append((f"Profils data/IA {year}", df, year, f.describe()))
    if f.others:
        df = other_devs(f.level_year, f)
        if column in df.columns:
            out.append((f"Autres développeurs {f.level_year}", df, f.level_year, f"autres développeurs · {f.region}"))
    return out


def starter_view(f: Filters, column: str, subtitle: str) -> None:
    """Vue de départ : classement des réponses d'une question, avec la population de chaque série."""
    st.subheader(subtitle)
    available = series_for(f, column)
    if not available:
        st.info(f"Cette question n'existe pas dans le sondage {f.level_year}.", icon=":material/info:")
        return
    parts, captions = [], []
    for name, df, year, who in available:
        t = shares_table(df, column)
        n = int(t["n"].iloc[0]) if len(t) else 0
        captions.append((n, year, who))
        if sample_status(n) != "masqué":
            parts.append(t.assign(series=name))
    if f.compare and not any(y == 2025 for _, y, _ in captions):
        st.caption("Cette question n'existe pas dans le sondage 2025 : seule l'année 2026 est affichée.")
    if not parts:
        st.warning("Moins de 30 répondants avec ces filtres : vue masquée.")
    else:
        st.plotly_chart(grouped_shares(pd.concat(parts)))
    for n, year, who in captions:
        population(n, year, who)
    if f.compare:
        harmonisation_warnings(warnings_for(column))
