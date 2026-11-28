# Architecture technique

Ce document est le premier que le jury lit. Il montre où vit chaque fonctionnalité,
et comment une donnée va du fichier brut jusqu'à chaque chiffre affiché.

## Principe

**L'analyse est séparée de l'interface.**

- `src/so_ece/` contient toute la logique : téléchargement, chargement, harmonisation, population, calculs. Ce paquet n'importe pas Streamlit, et il est testé par `tests/`.
- `app/` contient l'interface Streamlit. Les pages (`app/views/`) appellent les fonctions de `so_ece` et affichent le résultat. Elles ne calculent rien elles-mêmes.

## Flux des données

```text
src/so_ece/download.py     ensure_data() : télécharge les CSV 2025 et 2026 dans data/raw/, vérifiés par SHA-256
        │                  (appelé par scripts/download.py, ou par l'app si data/raw/ est vide)
src/so_ece/load.py         read_raw(year) : lit seulement les colonnes utiles
        │
src/so_ece/harmonise.py    harmonise(df, year) : noms de colonnes et libellés 2025 -> 2026,
        │                  d'après data/harmonisation.csv
src/so_ece/population.py   add_population_columns(df) : Europe ou non, groupe de rôle, tranche d'expérience,
        │                  d'après data/europe.csv et data/roles.csv
src/so_ece/dataset.py      load_year(year) = les trois étapes ci-dessus
        │
app/ui_data.py             get_year(year), mis en cache, puis profils data/IA et autres développeurs filtrés
        │
src/so_ece/analysis/       parts, comparaisons, intervalles, groupe de contrôle, indicateurs IA (fonctions pures)
        │
app/views/*.py             affichage : indicateurs, graphiques, tableaux, avec la population sous chaque chiffre
```

## Fonctionnalités et fichiers

| Fonctionnalité | Fichiers et fonctions |
| --- | --- |
| Téléchargement reproductible | `so_ece/download.py` : `FILES` (URL + SHA-256), `ensure_data()`, `missing_files()` ; `scripts/download.py` |
| Téléchargement au premier lancement (déploiement) | `app/ui_data.py` : `ensure_raw_data()`, appelé par `app/streamlit_app.py` |
| Lecture des fichiers | `so_ece/load.py` : `COLUMNS`, `read_raw()` |
| Harmonisation 2025 -> 2026 | `data/harmonisation.csv`, `so_ece/harmonise.py` : `harmonise()`, `warnings_for()` |
| Population (Europe, rôles, expérience) | `data/europe.csv`, `data/roles.csv`, `so_ece/population.py` : `add_population_columns()`, `select_data_profiles()`, `select_other_devs()` |
| Filtres (région, rôles, expérience, période, autres développeurs) | `so_ece/population.py` : `Filters` ; `app/ui_filters.py` : `filter_bar()` |
| Parts sur les questions à choix multiples | `so_ece/analysis/multi.py` : `share()`, `shares_table()`, `admired()` (correspondance exacte après découpage sur « ; ») |
| Évolution 2025 -> 2026 avec intervalle à 95 % | `so_ece/analysis/compare.py` : `diff_ci()`, `compare_items()` |
| Groupe de contrôle (autres développeurs) | `so_ece/analysis/home.py` : `home_table()`, `net_ci()`, `relative_change()`, `trend_reading()` |
| Indicateurs IA | `so_ece/analysis/ai.py` : `share_uses_ai()`, `complex_good_share()` |
| Tableau de l'accueil | `so_ece/catalog.py` : `HOME_ITEMS` ; `so_ece/analysis/home.py` : `home_table()`, `strongest()` |
| Population sous chaque chiffre | `so_ece/labels.py` : `population_label()`, `sample_status()` ; `app/ui_components.py` : `population()` |
| Graphiques | `app/ui_charts.py` : `evolution_figure()`, `used_vs_admired_figure()`, `grouped_shares()` |
| Navigation | `app/streamlit_app.py` : `st.navigation` |
| Accueil | `app/views/accueil.py` |
| Axes 1 à 5 | `app/views/axe_*.py`, gabarit commun `app/ui_axis.py` : `header()`, `starter_view()` |
| Exploration | `notebooks/` (un notebook par axe) |
| Vérification des chiffres de la note | `scripts/figures_note.py` |

## Ce qui est en cache, ce qui est en session

| Où | Quoi | Pourquoi |
| --- | --- | --- |
| `st.cache_data` | `get_year(year)` : chaque année téléchargée si besoin, chargée et harmonisée | Lire et harmoniser 80 000 lignes prend quelques secondes : une seule fois par serveur |
| `st.cache_data` | `data_profiles(...)`, `other_devs_cached(...)`, `france_all_devs(...)`, `home_cached(...)` | Les sous-populations et le tableau de l'accueil ne sont recalculés que si les filtres changent |
| `st.cache_resource` | `_download_lock()` | Empêche deux visiteurs de lancer le téléchargement en même temps au premier lancement |
| `st.query_params` (URL) | Région, rôles, expérience, période, autres développeurs | Une vue filtrée se partage par un lien |
| `st.session_state` | `filtres` : les filtres en cours (`ui_filters.current_filters()`) | La navigation entre pages repart d'une URL vide : les filtres sont relus en session puis réécrits dans l'URL |
| `st.session_state` | `fiche_ouverte` : dernière fiche technologie ouverte | Évite que la fiche se rouvre à chaque rerun tant que la sélection ne change pas |
| `lru_cache` (hors Streamlit) | Tables de référence (`europe.csv`, `roles.csv`, `harmonisation.csv`) | Lues une fois par processus |

## Règles de rigueur dans le code

- **Population sous chaque chiffre :** `population()` affiche n, année, population, région et le rappel « répondants volontaires ».
- **Seuils :** `sample_status()` masque sous 30 répondants et avertit sous 100.
- **Dénominateur :** une part se calcule toujours sur les répondants à la question (`respondents()`), jamais sur tous les répondants.
- **Correspondance exacte :** `has_item()` compare les réponses mot pour mot ; une recherche de texte compterait « MicroPython » comme « Python ».
- **Groupe de contrôle :** chaque évolution des profils data/IA est comparée à celle des autres développeurs de la même région et de la même expérience. L'écart net (profils data/IA − autres) a son propre intervalle à 95 % (`net_ci()`). `trend_reading()` ne parle d'évolution « propre aux profils data/IA » ou « plus marquée chez eux » que si cet écart net est significatif ; sinon l'évolution est classée « aussi chez les autres devs » (tendance générale ou effet d'échantillon). La fiche montre aussi l'évolution en proportion de l'usage de départ, car un écart en points dépend du niveau d'usage.
- **Avertissements d'harmonisation :** `warnings_for()` lit les notes `warning:` de `data/harmonisation.csv` (Docker, tâches complexes).
- **Tâches complexes :** `complex_good_share()` limite 2025 aux utilisateurs d'IA, car en 2026 la question ne leur est posée qu'à eux.
- **Questions absentes d'une année :** les vues d'axes l'indiquent au lieu d'afficher un graphique vide.
