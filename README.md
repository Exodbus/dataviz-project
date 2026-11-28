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

## Population

- Les région par défaut : l'Europe (UE à 27, Royaume-Uni, Suisse, Norvège,
Islande), listée dans `data/europe.csv`.
- Profils data/IA : les rôles de `data/roles.csv`, en 6 groupes (les DBA avec
les data engineers, trop peu nombreux seuls).
- Expérience professionnelle en trois tranches : 0-5 ans, 6-10 ans, plus de
10 ans.
- Moins de 30 répondants : chiffre masqué ; entre 30 et 100 : affiché avec un
avertissement (`src/so_ece/labels.py`).
- Les répondants sont des volontaires : aucune part n'est présentée comme
celle de tous les développeurs.
`load_year(2026)` (`src/so_ece/dataset.py`) lit, harmonise et ajoute ces
colonnes en une fois.

## Comparaisons, indicateurs IA et tests

Les calculs communs à l'accueil et aux axes sont dans `src/so_ece/analysis/`, sans Streamlit :

- `compare.py` : écart entre deux parts (2025 → 2026, ou profils data/IA face aux autres développeurs), avec son intervalle à 95 %.
- `ai.py` : part qui utilise l'IA, et part qui la juge bonne sur les tâches complexes (limitée aux utilisateurs d'IA les deux années, car la question 2026 ne leur est posée qu'à eux).
- `home.py` : tableau de l'accueil. Chaque évolution est comparée à celle des autres développeurs (groupe de contrôle) : une hausse n'est dite « propre aux profils data/IA » que si l'écart net est lui-même significatif.
- `src/so_ece/catalog.py` : les technologies suivies sur l'accueil (Docker exclu, son libellé a changé).

Un écart est significatif s'il dépasse son intervalle à 95 %. Sinon, il est affiché comme « dans la marge d'incertitude ».

Les tests se lancent avec `uv run pytest`, et `uv run python scripts/figures_note.py` recalcule les chiffres clés de la note de cadrage.

## Notebooks

`notebooks/00_prise_en_main.ipynb` montre comment charger une population et calculer une part, une évolution et le groupe de contrôle avec les fonctions du socle. Chaque membre y ajoute le notebook de son axe ; les règles sont dans `notebooks/README.md`.



## Lancer l'app

```
uv run streamlit run app/streamlit_app.py   # http://localhost:8501
```

Si les données n'ont pas été téléchargées, l'app le fait elle-même au premier lancement. L'interface est dans `app/` et ne fait aucun calcul : les calculs restent dans `src/so_ece/`. L'architecture (flux des données, cache, session) est décrite dans `docs/architecture.md`.

| Filtre | Valeurs | Par défaut |
| --- | --- | --- |
| Région | Europe ou Monde | Europe |
| Rôles data/IA | les 6 groupes de `data/roles.csv` | tous |
| Expérience | 0-5 ans, 6-10 ans, plus de 10 ans | toutes |
| Période | 2026, 2025, ou comparaison 2025 → 2026 | comparaison |
| Autres développeurs | groupe de contrôle (même région, même expérience) | activé |
