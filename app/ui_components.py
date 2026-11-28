"""Briques d'affichage communes : population sous chaque chiffre, avertissements, indicateurs."""

from __future__ import annotations

import streamlit as st

from so_ece.labels import pct, population_label, sample_status


def population(n: int, year: int | str, who: str) -> None:
    """À appeler sous chaque chiffre ou graphique : n, année, population, volontaires."""
    st.caption(population_label(n, year, who))
    status = sample_status(n)
    if status == "avertissement":
        st.caption(":orange[:material/warning: Moins de 100 répondants : à interpréter avec prudence.]")
    elif status == "masqué":
        st.caption(":red[:material/visibility_off: Moins de 30 répondants : chiffre masqué.]")


def harmonisation_warnings(notes: list[str]) -> None:
    for note in notes:
        st.warning(note, icon=":material/compare_arrows:")


def kpi(label: str, value: float, n: int, year: int | str, who: str, help: str | None = None) -> None:
    """Indicateur avec sa population ; masqué sous 30 répondants."""
    with st.container(border=True):
        shown = pct(value) if sample_status(n) != "masqué" else "—"
        st.metric(label, shown, help=help)
        population(n, year, who)
