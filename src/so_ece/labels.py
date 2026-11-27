"""Formats d'affichage et règle « population sous chaque chiffre »."""

from __future__ import annotations

import math

MIN_SHOW = 30  # en dessous : masqué
MIN_SAFE = 100  # en dessous : affiché avec avertissement


def pct(x: float, digits: int = 1) -> str:
    if x is None or math.isnan(x):
        return "—"
    return f"{x:.{digits}f}".replace(".", ",") + " %"


def points(x: float, digits: int = 1) -> str:
    if x is None or math.isnan(x):
        return "—"
    sign = "+" if x > 0 else ("−" if x < 0 else "")
    return f"{sign}{abs(x):.{digits}f}".replace(".", ",") + " pt"


def delta(x: float, digits: int = 1) -> str:
    """Delta pour st.metric : tiret ASCII en tête, pour que Streamlit colore la baisse en rouge."""
    return f"{x:+.{digits}f}".replace(".", ",") + " pt"


def thousands(n: int) -> str:
    return f"{n:,}".replace(",", " ")


def population_label(n: int, year: int | str, population: str) -> str:
    return f"n = {thousands(n)} · {year} · {population} · répondants volontaires du sondage Stack Overflow"


def sample_status(n: int) -> str:
    if n < MIN_SHOW:
        return "masqué"
    if n < MIN_SAFE:
        return "avertissement"
    return "ok"
