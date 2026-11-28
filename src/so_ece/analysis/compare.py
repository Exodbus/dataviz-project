"""Comparaisons 2025 -> 2026 et profils data/IA -> autres développeurs, avec marge d'incertitude."""

from __future__ import annotations

import math

import pandas as pd

from .multi import share

Z95 = 1.96


def diff_ci(p1: float, n1: int, p2: float, n2: int) -> float:
    """Demi-largeur de l'intervalle à 95 % de l'écart entre deux parts (en points).

    Approximation normale pour deux proportions indépendantes, comme dans la note de cadrage.
    """
    if not n1 or not n2 or math.isnan(p1) or math.isnan(p2):
        return float("nan")
    a, b = p1 / 100, p2 / 100
    return Z95 * math.sqrt(a * (1 - a) / n1 + b * (1 - b) / n2) * 100


def compare_items(df_a: pd.DataFrame, df_b: pd.DataFrame, col: str, items: list[str]) -> pd.DataFrame:
    """Pour chaque item : part dans A, part dans B, écart B - A, intervalle et significativité."""
    rows = []
    for item in items:
        pa, na = share(df_a, col, item)
        pb, nb = share(df_b, col, item)
        ci = diff_ci(pa, na, pb, nb)
        d = pb - pa
        rows.append(
            {
                "item": item,
                "share_a": pa,
                "n_a": na,
                "share_b": pb,
                "n_b": nb,
                "diff": d,
                "ci": ci,
                "significant": (not math.isnan(ci)) and abs(d) > ci,
            }
        )
    return pd.DataFrame(rows)
