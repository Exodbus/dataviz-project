"""Axe 5 : Métiers visés. Quels rôles utilisent quelles technologies, part de juniors."""

import streamlit as st

from so_ece.labels import sample_status
from ui_axis import header
from ui_components import population
from ui_data import profiles_for

f = header(
    "5. Métiers visés",
    "Quels métiers utilisent quelles technologies, et quelle place pour les juniors ?",
    "axis-5",
    "Paul",
)
st.warning(
    "Par rôle et par question, les effectifs européens vont de 28 à 134 répondants : "
    "presque tout passe sous 100 (avertissement), certains chiffres sous 30 (masqués). "
    "Les DBA (27 en Europe) sont regroupés avec les data engineers.",
    icon=":material/info:",
)
df = profiles_for(f.level_year, f)
counts = df["role_group"].value_counts().rename("Répondants").to_frame()
counts["Statut"] = counts["Répondants"].map(sample_status)
st.subheader(f"Profils data/IA par rôle ({f.level_year})")
st.dataframe(counts, width="stretch")
population(len(df), f.level_year, f.describe())

# À faire sur la branche de l'axe :
# - pour chaque rôle : part qui utilise SQL, DuckDB, Databricks SQL, Jupyter... (masquer sous 30)
# - part de juniors (0-5 ans) par rôle
# - pas de salaires : effectifs trop faibles en Europe (voir la note de cadrage)
