# Quelles technologies enseigner dans la majeure Data & IA de l'ECE ?

App Streamlit d'analyse du **Stack Overflow Developer Survey 2026**, comparé à l'édition 2025.
Projet final du cours Data Visualisation (ECE).

**Sponsor :** l'ECE, qui refond sa majeure Data & IA (Advanced Data, Data Frameworks, Machine Learning, et un nouveau cours « IA au quotidien »).

## Installation

Le projet utilise [uv](https://docs.astral.sh/uv/) pour l'environnement Python.

- Linux, macOS ou WSL : `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Windows (PowerShell) : `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

```bash
git clone https://github.com/Exodbus/dataviz-project.git
cd dataviz-project
uv sync
uv run python scripts/download.py   # données 2025 et 2026 (≈ 250 Mo), vérifiées par SHA-256
```

## Données

Les données ne sont jamais commitées : elles sont téléchargées dans `data/raw/`, qui est dans le `.gitignore`.

- 2026 : [archive officielle Stack Overflow](https://github.com/StackExchange/Survey/tree/main/packages/archive/2026), `survey_results_public.csv` et `survey_results_schema.csv`.
- 2025 : même archive, dossier `2025`, `results.csv` et `schema.csv`.

## Organisation

```text
src/so_ece/
  paths.py      chemins du projet
  download.py   téléchargement vérifié par SHA-256
  load.py       lecture des colonnes utiles des deux sondages
scripts/
  download.py   lance le téléchargement
```