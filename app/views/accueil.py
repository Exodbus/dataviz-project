"""Accueil : le message pour l'ECE, quatre indicateurs, l'encart France, deux vues croisées, un tableau."""

import streamlit as st

from so_ece.analysis.ai import share_uses_ai
from so_ece.analysis.compare import diff_ci
from so_ece.analysis.home import strongest
from so_ece.analysis.multi import share
from so_ece.harmonise import warnings_for
from so_ece.labels import delta, pct, points, thousands
from ui_charts import evolution_figure, used_vs_admired_figure
from ui_components import population
from ui_data import france_all_devs, home, other_devs, profiles_for
from ui_filters import filter_bar

st.title("Quelles technologies enseigner dans la majeure Data & IA ?")
st.markdown(
    "> **« Gardez Python et SQL, modernisez le SQL analytique et l'outillage, "
    "et apprenez aux étudiants à vérifier l'IA. »**"
)

f = filter_bar()
who = f.describe()
year = f.level_year
table = home(f)
d = profiles_for(year, f)
o = other_devs(year, f)
d25 = profiles_for(2025, f)


def others_line(label: str, p: float, n: int) -> None:
    if f.others:
        prefix = f"{label} " if label else ""
        st.caption(f"Autres développeurs : {prefix}{pct(p)} (n = {thousands(n)})")


# --- Quatre indicateurs -------------------------------------------------------
c1, c2, c3, c4 = st.columns([1.35, 1, 1, 1])
with c1, st.container(border=True):
    st.markdown("**Socle Python et SQL**")
    a, b = st.columns(2)
    for col, lang in ((a, "Python"), (b, "SQL")):
        p, n = share(d, "LanguagesHaveWorkedWith", lang)
        p25, n25 = share(d25, "LanguagesHaveWorkedWith", lang)
        sig = abs(p - p25) > diff_ci(p25, n25, p, n)
        col.metric(lang, pct(p), delta(p - p25) if f.compare else None, delta_color="normal" if sig else "off",
                   help=None if sig else "Écart 2025 → 2026 dans la marge d'incertitude")
    population(n, year, who)
    if f.others:
        po, no = share(o, "LanguagesHaveWorkedWith", "Python")
        so, _ = share(o, "LanguagesHaveWorkedWith", "SQL")
        st.caption(f"Autres développeurs : Python {pct(po)}, SQL {pct(so)} (n = {thousands(no)})")
with c2, st.container(border=True):
    p, n = share_uses_ai(d)
    st.metric("Utilisent l'IA au travail", pct(p))
    population(n, year, who)
    others_line("", *share_uses_ai(o))
    if f.compare:
        st.caption("Pas d'évolution affichée : la question a changé de forme entre 2025 et 2026.")
for col, direction, title in ((c3, "up", "Plus forte hausse significative"), (c4, "down", "Plus forte baisse significative")):
    with col, st.container(border=True):
        r = strongest(table, direction)
        if r is None:
            st.metric(title, "Aucune")
            st.caption("Aucun écart ne dépasse la marge d'incertitude")
            continue
        st.metric(title, r["label"], delta(r["diff"]))
        st.caption(f"2025 → 2026 · {who} · n = {r['n_a']} puis {r['n_b']}")
        if f.others:
            st.caption(f"Autres développeurs : {points(r['o_diff'])}"
                       + (" (significatif)" if r["o_significant"] else " (dans la marge)"))

# --- Encart France -------------------------------------------------------------
fr = france_all_devs(2026)
with st.container(border=True):
    st.markdown("**Encart France · 2026 · tous les développeurs français, pas seulement les profils data**")
    a, b, c = st.columns(3)
    for col, (label, (p, n)) in zip(
        (a, b, c),
        [
            ("Python", share(fr, "LanguagesHaveWorkedWith", "Python")),
            ("SQL", share(fr, "LanguagesHaveWorkedWith", "SQL")),
            ("Utilisent l'IA", share_uses_ai(fr)),
        ],
    ):
        with col:
            st.metric(label, pct(p))
            population(n, 2026, "tous développeurs · France")
    st.caption(
        "La France ne compte que 52 profils data/IA en 2026 : trop peu pour un filtre dédié. "
        "Un diplômé ECE travaille avec les mêmes technologies qu'à Berlin ou à Londres."
    )

# --- Deux vues croisées ----------------------------------------------------------
left, right = st.columns([1.1, 1])
with left:
    st.subheader("Ce qui monte, ce qui descend (2025 → 2026)")
    st.caption(
        "Barres : profils data/IA. Vert ou rouge : écart significatif · gris : dans la marge d'incertitude. "
        + ("Losanges : la même évolution chez les autres développeurs. Si elle apparaît aussi chez eux, "
           "ce n'est pas une tendance propre aux métiers de la data (tendance générale ou effet d'échantillon). " if f.others else "")
        + "Cliquez sur une barre pour sa fiche."
    )
    evo = st.plotly_chart(evolution_figure(table, show_control=f.others), on_select="rerun",
                          selection_mode="points", key="evo")
    st.caption(
        f"n = {thousands(int(table['n_a'].min()))} à {thousands(int(table['n_a'].max()))} en 2025, "
        f"{thousands(int(table['n_b'].min()))} à {thousands(int(table['n_b'].max()))} en 2026 selon la question · {who}"
        + (f" · autres développeurs : n = {thousands(int(table['o_n_b'].min()))} à {thousands(int(table['o_n_b'].max()))} en 2026"
           if f.others else "")
        + " · répondants volontaires du sondage Stack Overflow · Docker exclu (libellé modifié entre les deux années)"
    )
with right:
    st.subheader(f"Utilisée × appréciée ({year})")
    st.caption("En haut à gauche : peu utilisées mais très appréciées. Étiquettes sur les points clés, les autres au survol.")
    quad = st.plotly_chart(used_vs_admired_figure(table, year), on_select="rerun", selection_mode="points", key="quad")
    st.caption(f"Appréciée = part des utilisateurs qui veulent continuer, calculée à partir de 30 utilisateurs · {who} · {year}")


# --- Fiche détaillée -------------------------------------------------------------
@st.dialog("Fiche technologie", width="large")
def fiche(label: str) -> None:
    r = table[table["label"] == label].iloc[0]
    st.subheader(f"{r['label']} · {r['category']}")
    a, b, c = st.columns(3)
    a.metric("Utilisée en 2025", pct(r["share_a"]))
    b.metric("Utilisée en 2026", pct(r["share_b"]), delta(r["diff"]))
    c.metric("Désirée en 2026", pct(r["wanted_b"]))
    marge = f"{r['ci']:.1f}".replace(".", ",")
    verdict = "**significatif**" if r["significant"] else "**dans la marge d'incertitude**"
    st.markdown(f"Écart {points(r['diff'])} ± {marge} point (intervalle à 95 %) : {verdict}.")
    st.markdown(f"**Lecture :** {r['reading']}.")
    st.caption(f"n = {r['n_a']} en 2025, {r['n_b']} en 2026 · {who} · répondants volontaires du sondage Stack Overflow")
    if f.others:
        st.markdown(
            f"**Autres développeurs :** {pct(r['o_share_a'])} → {pct(r['o_share_b'])}, "
            f"{points(r['o_diff'])} ({'significatif' if r['o_significant'] else 'dans la marge'})"
        )
        net_margin = f"{r['net_ci']:.1f}".replace(".", ",")
        st.markdown(
            f"**Écart net** (profils data/IA − autres développeurs) : {points(r['net_diff'])} ± {net_margin} point, "
            + ("significatif." if r["net_significant"] else "dans la marge d'incertitude.")
        )
        rel = f"{r['rel']:+.0f} %".replace("-", "−")
        o_rel = f"{r['o_rel']:+.0f} %".replace("-", "−")
        st.markdown(f"**En proportion de l'usage de 2025 :** {rel} chez les profils data/IA, {o_rel} chez les autres développeurs.")
        st.caption(f"n = {r['o_n_a']} en 2025, {r['o_n_b']} en 2026 · autres développeurs · {f.region}")
    for note in warnings_for(r["column"], r["item"]):
        st.warning(note)


def open_once(source: str, label: str | None) -> None:
    """Ouvre la fiche seulement quand la sélection change (sinon elle se rouvrirait à chaque rerun)."""
    key = f"{source}:{label}"
    if label and st.session_state.get("fiche_ouverte") != key:
        st.session_state["fiche_ouverte"] = key
        fiche(label)


for source, event in (("evo", evo), ("quad", quad)):
    pts = event.get("selection", {}).get("points", []) if event else []
    if pts:
        cd = pts[0].get("customdata")
        open_once(source, cd if isinstance(cd, str) else (cd[0] if cd else pts[0].get("y")))

# --- Tableau ---------------------------------------------------------------------
st.subheader("Toutes les technologies suivies")
cols = {"label": "Technologie", "category": "Catégorie"}
if f.compare or year == 2025:
    cols["share_a"] = "Utilisée 2025"
if f.compare or year == 2026:
    cols["share_b"] = "Utilisée 2026"
if f.compare:
    cols |= {"diff": "Écart (pt)", "ci": "± (pt)", "reading": "Lecture"}
cols |= ({"wanted_b": "Désirée 2026", "admired_b": "Appréciée 2026"} if year == 2026
         else {"wanted_a": "Désirée 2025", "admired_a": "Appréciée 2025"})
if f.others:
    cols |= {"o_share_b" if year == 2026 else "o_share_a": f"Autres devs {year}"}
    if f.compare:
        cols |= {"o_diff": "Autres devs : écart (pt)", "net_diff": "Écart net (pt)", "net_ci": "± net (pt)"}
cols["n_b" if year == 2026 else "n_a"] = f"n {year}"
view = table[list(cols)].rename(columns=cols)
pct_cols = [c for c in view.columns if c.startswith(("Utilisée", "Désirée", "Appréciée", "Autres devs 20"))]
pt_cols = [c for c in view.columns if c in ("Écart (pt)", "Autres devs : écart (pt)", "Écart net (pt)")]
margin_cols = [c for c in view.columns if c.startswith("±")]
config = {c: st.column_config.NumberColumn(format="%.1f %%") for c in pct_cols}
config |= {c: st.column_config.NumberColumn(format="%+.1f") for c in pt_cols}
config |= {c: st.column_config.NumberColumn(format="%.1f") for c in margin_cols}
sel = st.dataframe(view, hide_index=True, on_select="rerun", selection_mode="single-row", key="table", width="stretch",
                   column_config=config)
if sel and sel.get("selection", {}).get("rows"):
    open_once("table", view.iloc[sel["selection"]["rows"][0]]["Technologie"])
st.caption(f"Parts en % des répondants à chaque question · {who} · répondants volontaires du sondage Stack Overflow")
