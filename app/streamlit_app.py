"""Point d'entrée : uv run streamlit run app/streamlit_app.py"""

import sys
from pathlib import Path

# Rend le paquet so_ece importable même quand il n'est pas installé
# (Streamlit Community Cloud installe les dépendances, pas le projet lui-même).
SRC = Path(__file__).resolve().parents[1] / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

import streamlit as st  # noqa: E402

from ui_data import ensure_raw_data  # noqa: E402

st.set_page_config(
    page_title="Majeure Data & IA — Stack Overflow 2026",
    page_icon=":material/school:",
    layout="wide",
)

# Au premier lancement (déploiement), data/raw/ est vide : l'app télécharge les données elle-même.
ensure_raw_data()

pages = {
    "": [st.Page("views/accueil.py", title="Accueil", icon=":material/home:", default=True)],
    "Les 5 axes": [
        st.Page("views/axe_1_advanced_data.py", title="1. Advanced Data (SQL)", icon=":material/database:"),
        st.Page("views/axe_2_data_frameworks.py", title="2. Data Frameworks", icon=":material/cloud:"),
        st.Page("views/axe_3_ml_llm.py", title="3. ML et LLM", icon=":material/model_training:"),
        st.Page("views/axe_4_ia_quotidien.py", title="4. IA au quotidien", icon=":material/smart_toy:"),
        st.Page("views/axe_5_metiers.py", title="5. Métiers visés", icon=":material/badge:"),
    ],
}

st.navigation(pages, position="top").run()
