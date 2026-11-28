# Notebooks d'exploration

Un notebook par membre et par axe, versionné dans le dépôt : l'énoncé demande de garder la trace de la phase d'exploration.

| Notebook | Auteur | Axe |
| --- | --- | --- |
| `00_prise_en_main.ipynb` | socle commun | exemple d'utilisation du socle |
| `axe1_exploration.ipynb` | Corentin | 1. Advanced Data (SQL) |
| `axe2_exploration.ipynb` | Erwan | 2. Data Frameworks |
| `axe3_exploration.ipynb` | Alexandre | 3. ML et LLM |
| `axe4_exploration.ipynb` | Lyam | 4. IA au quotidien |
| `axe5_exploration.ipynb` | Paul | 5. Métiers visés |

Règles :

- Charger les données avec `so_ece.dataset.load_year()`, jamais avec un `pd.read_csv` sur un chemin à soi : le notebook doit tourner chez tout le monde.
- Vider les sorties avant de committer (dans VS Code : « Clear All Outputs »), pour garder des différences lisibles dans l'historique.
- Les calculs retenus pour l'app passent ensuite dans `src/so_ece/analysis/`, avec un test.

Ouvrir un notebook : dans VS Code, choisir le noyau `.venv` du projet, ou lancer `uv run --with jupyter jupyter lab`.
