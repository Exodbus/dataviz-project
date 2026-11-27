# Quelles technologies enseigner dans la majeure Data & IA de l'ECE ?

App Streamlit d'analyse du **Stack Overflow Developer Survey 2026**, comparé à l'édition 2025.
Projet final du cours Data Visualisation (ECE).

**Sponsor :** l'ECE, qui refond sa majeure Data & IA.

## Installation

Le projet utilise [uv](https://docs.astral.sh/uv/) pour l'environnement Python.

```bash
git clone https://github.com/Exodbus/dataviz-project.git
cd dataviz-project
uv sync
uv run python scripts/download.py   # télécharge les données 2025 et 2026
```

Les données ne sont jamais commitées : `data/raw/` est dans le `.gitignore`.