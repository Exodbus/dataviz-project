"""Définition de la population : région, groupe de rôle, tranche d'expérience.

Population de l'app : les profils data et IA (rôle déclaré, data/roles.csv),
comparés aux autres développeurs. Europe = UE à 27, Royaume-Uni, Suisse, Norvège, Islande
(data/europe.csv).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from functools import lru_cache

import pandas as pd

from .paths import DATA_DIR

AUTRES = "Autres développeurs"
EXP_BANDS = ["0-5 ans", "6-10 ans", "Plus de 10 ans"]
REGIONS = ["Europe", "Monde"]


@lru_cache(maxsize=1)
def europe_countries() -> frozenset[str]:
    return frozenset(pd.read_csv(DATA_DIR / "europe.csv")["country"])


@lru_cache(maxsize=1)
def role_groups() -> dict[str, str]:
    t = pd.read_csv(DATA_DIR / "roles.csv")
    return dict(zip(t["role"], t["groupe"]))


def data_groups() -> list[str]:
    return list(dict.fromkeys(role_groups().values()))


def add_population_columns(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["is_europe"] = out["Country"].isin(europe_countries())
    groups = role_groups()
    out["role_group"] = out["Role"].map(lambda r: groups.get(r, AUTRES) if isinstance(r, str) else None)
    out["is_data"] = out["Role"].isin(groups.keys())
    exp = pd.to_numeric(out["WorkExp"], errors="coerce")
    out["work_exp"] = exp
    out["exp_band"] = pd.cut(exp, [-1, 5, 10, 200], labels=EXP_BANDS).astype("object")
    return out


@dataclass(frozen=True)
class Filters:
    region: str = "Europe"
    groups: tuple[str, ...] = field(default_factory=tuple)  # vide = tous les profils data/IA
    exp_bands: tuple[str, ...] = field(default_factory=tuple)  # vide = toutes les expériences

    def describe(self) -> str:
        who = ", ".join(self.groups) if self.groups else "profils data/IA"
        exp = f" · {', '.join(self.exp_bands)}" if self.exp_bands else ""
        return f"{who}{exp} · {self.region}"


def apply_region(df: pd.DataFrame, region: str) -> pd.DataFrame:
    return df[df["is_europe"]] if region == "Europe" else df


def select_data_profiles(df: pd.DataFrame, f: Filters) -> pd.DataFrame:
    out = apply_region(df, f.region)
    out = out[out["is_data"]]
    if f.groups:
        out = out[out["role_group"].isin(f.groups)]
    if f.exp_bands:
        out = out[out["exp_band"].isin(f.exp_bands)]
    return out


def select_other_devs(df: pd.DataFrame, f: Filters) -> pd.DataFrame:
    """Groupe de comparaison : les autres développeurs de la même région."""
    out = apply_region(df, f.region)
    return out[out["role_group"] == AUTRES]
