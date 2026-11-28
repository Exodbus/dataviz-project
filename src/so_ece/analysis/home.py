"""Tableau de la page d'accueil.

Pour chaque technologie suivie : part d'utilisateurs 2025 et 2026 chez les profils data/IA,
écart avec son intervalle à 95 %, part désirée et appréciée pour chaque année,
et la même évolution chez les autres développeurs (groupe de contrôle).

Le groupe de contrôle sert à distinguer une vraie tendance des profils data/IA d'un simple
changement d'échantillon entre les deux éditions du sondage (49 191 répondants en 2025, 30 903 en 2026).
On calcule l'écart net = écart des profils data/IA − écart des autres développeurs, avec son
intervalle à 95 % : une évolution n'est dite « propre aux profils data/IA » que si cet écart net
est lui-même significatif.
"""

from __future__ import annotations

import math

import pandas as pd

from ..catalog import HOME_ITEMS, WANT_COLUMN
from .compare import compare_items
from .multi import admired, has_item


def share_want(df: pd.DataFrame, have_col: str, item: str) -> tuple[float, int]:
    """Part qui veut travailler avec `item` l'an prochain, parmi les répondants à la question « utilisée »."""
    base = df[df[have_col].notna()]
    if not len(base):
        return float("nan"), 0
    wants = has_item(base[WANT_COLUMN[have_col]].dropna(), item).sum()
    return float(wants / len(base) * 100), len(base)


def net_ci(ci: float, o_ci: float) -> float:
    """Intervalle à 95 % de l'écart net (échantillons indépendants : les variances s'additionnent)."""
    return math.sqrt(ci**2 + o_ci**2)


def relative_change(a: float, b: float) -> float:
    """Évolution en proportion de l'usage de départ (en %), NaN si l'usage de départ est nul."""
    return (b / a - 1) * 100 if a else float("nan")


def trend_reading(sig: bool, diff: float, o_sig: bool, o_diff: float, net: float, net_margin: float) -> str:
    """Lecture en une expression de l'évolution des profils data/IA, comparée au groupe de contrôle."""
    if not sig:
        return "Dans la marge d'incertitude"
    if abs(net) <= net_margin:
        return "Aussi chez les autres devs (tendance générale ou effet d'échantillon)"
    if o_sig and (diff > 0) == (o_diff > 0):
        return "Plus marquée chez les profils data/IA"
    return "Propre aux profils data/IA"


def home_table(d25: pd.DataFrame, d26: pd.DataFrame, o25: pd.DataFrame, o26: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for col, item, label, category in HOME_ITEMS:
        r = compare_items(d25, d26, col, [item]).iloc[0].to_dict()
        o = compare_items(o25, o26, col, [item]).iloc[0]
        want = WANT_COLUMN[col]
        r.update(
            column=col,
            label=label,
            category=category,
            wanted_a=share_want(d25, col, item)[0],
            wanted_b=share_want(d26, col, item)[0],
            admired_a=admired(d25, col, want, item)[0],
            admired_b=admired(d26, col, want, item)[0],
            n_users_b=admired(d26, col, want, item)[1],
            o_share_a=o["share_a"],
            o_n_a=o["n_a"],
            o_share_b=o["share_b"],
            o_n_b=o["n_b"],
            o_diff=o["diff"],
            o_ci=o["ci"],
            o_significant=o["significant"],
        )
        r["net_diff"] = r["diff"] - r["o_diff"]
        r["net_ci"] = net_ci(r["ci"], r["o_ci"])
        r["net_significant"] = abs(r["net_diff"]) > r["net_ci"]
        r["rel"] = relative_change(r["share_a"], r["share_b"])
        r["o_rel"] = relative_change(r["o_share_a"], r["o_share_b"])
        r["reading"] = trend_reading(
            r["significant"], r["diff"], r["o_significant"], r["o_diff"], r["net_diff"], r["net_ci"]
        )
        rows.append(r)
    return pd.DataFrame(rows)


def strongest(t: pd.DataFrame, direction: str) -> pd.Series | None:
    """Plus forte hausse (direction='up') ou baisse ('down') significative, ou None."""
    sig = t[t["significant"]]
    sig = sig[sig["diff"] > 0] if direction == "up" else sig[sig["diff"] < 0]
    if sig.empty:
        return None
    return sig.loc[sig["diff"].idxmax()] if direction == "up" else sig.loc[sig["diff"].idxmin()]
