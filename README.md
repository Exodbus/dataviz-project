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
  paths.py        chemins du projet
  download.py     téléchargement vérifié par SHA-256
  load.py         lecture des colonnes utiles des deux sondages
  harmonise.py    passe les données 2025 dans le vocabulaire 2026
  analysis/
    multi.py      calcul des parts pour les questions à choix multiples
data/
  harmonisation.csv   correspondances entre 2025 et 2026
scripts/
  download.py     lance le téléchargement
```

## Harmonisation 2025 / 2026

Les deux sondages n'ont pas toujours les mêmes noms de colonnes ni les mêmes réponses. Par exemple, `LanguageHaveWorkedWith` en 2025 s'appelle `LanguagesHaveWorkedWith` en 2026, et `Docker` est devenu `Docker / Docker Compose`.

Toutes ces correspondances sont dans `data/harmonisation.csv`, pas dans le code. Quand une question a changé entre les deux années (Docker, IA sur les tâches complexes), l'app affiche un avertissement.

Pour les parts, les réponses sont découpées sur « ; » puis comparées mot pour mot. Sinon « MicroPython » serait compté comme « Python ».