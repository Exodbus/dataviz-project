"""Barre de filtres horizontale : appliquée en une fois (formulaire), gardée en session et dans l'URL.

Filtres : région, rôles data/IA, expérience, période (2026, 2025 ou comparaison 2025 → 2026)
et affichage des autres développeurs comme groupe de comparaison.

Pourquoi la session en plus de l'URL : quand on change de page avec la navigation du haut,
Streamlit repart d'une URL sans paramètres. Les filtres sont alors relus dans st.session_state,
puis réécrits dans l'URL, pour qu'une vue reste partageable par un lien sur toutes les pages.
"""

from __future__ import annotations

import streamlit as st

from so_ece.population import COMPARE, EXP_BANDS, PERIODS, REGIONS, Filters, data_groups

URL_KEYS = ("region", "role", "exp", "periode", "autres")
SESSION_KEY = "filtres"


def _from_url() -> Filters:
    qp = st.query_params
    region = qp.get("region", "Europe")
    region = region if region in REGIONS else "Europe"
    groups = tuple(g for g in qp.get_all("role") if g in data_groups())
    exp = tuple(e for e in qp.get_all("exp") if e in EXP_BANDS)
    period = qp.get("periode", COMPARE)
    period = period if period in PERIODS else COMPARE
    others = qp.get("autres", "1") != "0"
    return Filters(region, groups, exp, period, others)


def _to_url(f: Filters) -> None:
    st.query_params.from_dict(
        {
            "region": f.region,
            "role": list(f.groups),
            "exp": list(f.exp_bands),
            "periode": f.period,
            "autres": "1" if f.others else "0",
        }
    )


def current_filters() -> Filters:
    """Filtres en cours. Un lien avec des paramètres fait foi ; sinon on reprend ceux de la session."""
    if any(k in st.query_params for k in URL_KEYS):
        f = _from_url()
    else:
        f = st.session_state.get(SESSION_KEY, Filters())
        _to_url(f)
    st.session_state[SESSION_KEY] = f
    return f


def filter_bar(key: str = "filtres_form") -> Filters:
    cur = current_filters()
    with st.form(key, border=True):
        r1c1, r1c2, r1c3 = st.columns([1.1, 2.6, 2.3], vertical_alignment="bottom")
        region = r1c1.segmented_control("Région", REGIONS, default=cur.region)
        groups = r1c2.multiselect("Rôles data/IA", data_groups(), default=list(cur.groups),
                                  placeholder="Tous les profils data/IA")
        exp = r1c3.pills("Expérience professionnelle", EXP_BANDS, default=list(cur.exp_bands), selection_mode="multi")
        r2c1, r2c2, r2c3 = st.columns([2.2, 2.6, 1.2], vertical_alignment="bottom")
        period = r2c1.segmented_control("Période", PERIODS, default=cur.period)
        others = r2c2.toggle("Comparer aux autres développeurs", value=cur.others,
                             help="Affiche les autres développeurs de la même région et de la même expérience.")
        submitted = r2c3.form_submit_button("Appliquer", type="primary", width="stretch")
    if submitted:
        new = Filters(region or "Europe", tuple(groups), tuple(exp), period or COMPARE, others)
        st.session_state[SESSION_KEY] = new
        _to_url(new)
        st.rerun()
    return cur
