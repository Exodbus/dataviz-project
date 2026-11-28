"""Graphiques Plotly de l'app. Les données arrivent déjà calculées depuis src/so_ece."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go

from so_ece.labels import pct, points

UP, DOWN, FLAT = "#2e7d32", "#c62828", "#a7a7a7"
CONTROL = "#5b5b5b"
MAIN = "#1f6fd1"
CATEGORY_COLORS = {
    "Langages": "#1f6fd1",
    "Bases de données": "#e07b00",
    "Cloud": "#7b3fb6",
    "Éditeurs": "#0f8a7e",
}
SERIES_COLORS = ["#1f6fd1", "#9cc0ee", "#8a8a8a", "#c9c9c9"]


def _comma(x: float) -> str:
    return f"{x:.1f}".replace(".", ",")


def evolution_figure(cmp: pd.DataFrame, show_control: bool = True) -> go.Figure:
    """Barres divergentes de l'écart 2025 -> 2026 chez les profils data/IA, avec intervalle à 95 %,
    et le même écart chez les autres développeurs (losanges gris) comme groupe de contrôle."""
    t = cmp.sort_values("diff")
    colors = [(UP if d > 0 else DOWN) if s else FLAT for d, s in zip(t["diff"], t["significant"])]
    hover = [
        f"<b>{r.label}</b> ({r.category})<br>Profils data/IA : {pct(r.share_a)} (n = {r.n_a}) → {pct(r.share_b)} (n = {r.n_b})"
        f"<br>Écart : {points(r.diff)} ± {_comma(r.ci)}<br>Lecture : {r.reading}"
        for r in t.itertuples()
    ]
    fig = go.Figure(
        go.Bar(
            x=t["diff"], y=t["label"], orientation="h", name="Profils data/IA", showlegend=False,
            marker_color=colors,
            error_x=dict(type="data", array=t["ci"], color="#6b6b6b", thickness=1.2, width=4),
            hovertext=hover, hoverinfo="text", customdata=t["label"],
        )
    )
    if show_control:
        fig.add_trace(
            go.Scatter(
                x=t["o_diff"], y=t["label"], mode="markers", name="Autres développeurs (contrôle)",
                marker=dict(symbol="diamond", size=9, color=CONTROL, line=dict(color="white", width=1)),
                error_x=dict(type="data", array=t["o_ci"], color=CONTROL, thickness=1, width=3),
                hovertext=[
                    f"<b>{r.label}</b> · autres développeurs<br>{pct(r.o_share_a)} (n = {r.o_n_a}) → {pct(r.o_share_b)} (n = {r.o_n_b})"
                    f"<br>Écart : {points(r.o_diff)} ± {_comma(r.o_ci)}"
                    for r in t.itertuples()
                ],
                hoverinfo="text", customdata=t["label"],
            )
        )
    fig.add_vline(x=0, line_width=1, line_color="#6b6b6b")
    fig.update_layout(
        height=28 * len(t) + 110,
        margin=dict(l=10, r=10, t=10, b=40),
        xaxis_title="Écart de la part d'utilisateurs 2025 → 2026, en points (intervalle à 95 %)",
        showlegend=show_control,  # seule la légende du groupe de contrôle ; les barres sont expliquées en légende de la page
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0),
    )
    return fig


def labelled_points(t: pd.DataFrame, used: str, adm: str, min_dx: float = 7.0, min_dy: float = 3.0) -> set[str]:
    """Étiquettes affichées : évolutions significatives, puis les plus utilisées, puis les plus et moins appréciées.
    Une étiquette trop proche d'une étiquette déjà retenue est sautée ; les autres technologies restent au survol."""
    candidates = (
        list(t.loc[t["significant"], "label"])
        + list(t.nlargest(3, used)["label"])
        + list(t.nlargest(2, adm)["label"])
        + list(t.nsmallest(2, adm)["label"])
    )
    pos = t.set_index("label")[[used, adm]]
    keep: list[str] = []
    for label in dict.fromkeys(candidates):
        x, y = pos.loc[label]
        if all(abs(x - pos.loc[k, used]) >= min_dx or abs(y - pos.loc[k, adm]) >= min_dy for k in keep):
            keep.append(label)
    return set(keep)


def used_vs_admired_figure(t: pd.DataFrame, year: int) -> go.Figure:
    """Nuage « utilisée × appréciée », coloré par catégorie, étiquettes sélectives."""
    used, adm = ("share_b", "admired_b") if year == 2026 else ("share_a", "admired_a")
    t = t.dropna(subset=[adm])
    keep = labelled_points(t, used, adm)
    fig = go.Figure()
    for category, color in CATEGORY_COLORS.items():
        c = t[t["category"] == category]
        if c.empty:
            continue
        fig.add_trace(
            go.Scatter(
                x=c[used], y=c[adm], mode="markers+text", name=category,
                text=[lbl if lbl in keep else "" for lbl in c["label"]],
                textposition="top center", textfont=dict(size=11),
                marker=dict(size=11, color=color, opacity=0.85, line=dict(color="white", width=1)),
                hovertext=[f"<b>{r.label}</b> ({category})<br>Utilisée : {pct(getattr(r, used))}<br>Appréciée : {pct(getattr(r, adm))}"
                           for r in c.itertuples()],
                hoverinfo="text", customdata=c["label"],
            )
        )
    fig.update_layout(
        height=470,
        margin=dict(l=10, r=10, t=10, b=40),
        xaxis_title=f"Utilisée en {year} (% des répondants à la question)",
        yaxis_title="Appréciée (% des utilisateurs qui veulent continuer)",
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0),
    )
    return fig


def grouped_shares(long: pd.DataFrame, top: int = 15) -> go.Figure:
    """Barres horizontales groupées : une série par population et par année, valeur au bout de chaque barre.

    `long` : colonnes item, share, series, dans l'ordre d'affichage voulu (première série = référence).
    Les items sont classés d'après la première série. Dans chaque groupe, les barres se lisent de haut en bas
    dans le même ordre que la légende.
    """
    series = list(dict.fromkeys(long["series"]))
    order = (long[long["series"] == series[0]].nlargest(top, "share")["item"]).tolist()
    fig = go.Figure()
    # Plotly dessine la première série en bas de chaque groupe : on ajoute les séries à l'envers,
    # et on inverse l'ordre de la légende, pour que légende et barres se lisent dans le même sens.
    for i, s in reversed(list(enumerate(series))):
        d = long[(long["series"] == s) & long["item"].isin(order)].set_index("item").reindex(order[::-1])
        fig.add_trace(
            go.Bar(
                x=d["share"], y=d.index, orientation="h", name=s,
                marker_color=SERIES_COLORS[i % len(SERIES_COLORS)],
                text=[pct(v) if pd.notna(v) else "" for v in d["share"]],
                textposition="outside", textfont=dict(size=11), cliponaxis=False,
                hovertemplate="%{y} : %{x:.1f} %<extra>" + s + "</extra>",
            )
        )
    xmax = float(long.loc[long["item"].isin(order), "share"].max() or 0)
    fig.update_layout(
        barmode="group", bargap=0.25, bargroupgap=0.05,
        height=(18 + 16 * len(series)) * len(order) + 90,
        margin=dict(l=10, r=10, t=10, b=40),
        xaxis=dict(title="% des répondants à la question", range=[0, xmax * 1.18 + 1]),
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0, traceorder="reversed"),
        showlegend=len(series) > 1,
    )
    return fig
