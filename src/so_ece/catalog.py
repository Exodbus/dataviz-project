"""Technologies suivies sur la page d'accueil, avec leur colonne et leur catégorie.

Docker est volontairement absent : son libellé a changé entre 2025 et 2026 (voir harmonisation.csv).
"""

HOME_ITEMS = [
    # (colonne, réponse exacte, libellé court, catégorie)
    ("LanguagesHaveWorkedWith", "Python", "Python", "Langages"),
    ("LanguagesHaveWorkedWith", "SQL", "SQL", "Langages"),
    ("LanguagesHaveWorkedWith", "R", "R", "Langages"),
    ("LanguagesHaveWorkedWith", "Bash/Shell (all shells)", "Bash/Shell", "Langages"),
    ("LanguagesHaveWorkedWith", "Rust", "Rust", "Langages"),
    ("DatabasesHaveWorkedWith", "PostgreSQL", "PostgreSQL", "Bases de données"),
    ("DatabasesHaveWorkedWith", "SQLite", "SQLite", "Bases de données"),
    ("DatabasesHaveWorkedWith", "MySQL", "MySQL", "Bases de données"),
    ("DatabasesHaveWorkedWith", "Microsoft SQL Server", "SQL Server", "Bases de données"),
    ("DatabasesHaveWorkedWith", "DuckDB", "DuckDB", "Bases de données"),
    ("DatabasesHaveWorkedWith", "BigQuery", "BigQuery", "Bases de données"),
    ("DatabasesHaveWorkedWith", "Databricks SQL", "Databricks SQL", "Bases de données"),
    ("DatabasesHaveWorkedWith", "MongoDB", "MongoDB", "Bases de données"),
    ("DatabasesHaveWorkedWith", "Redis", "Redis", "Bases de données"),
    ("CloudPlatHaveWorkedWith", "Amazon Web Services (AWS)", "AWS", "Cloud"),
    ("CloudPlatHaveWorkedWith", "Microsoft Azure", "Azure", "Cloud"),
    ("CloudPlatHaveWorkedWith", "Google Cloud", "Google Cloud", "Cloud"),
    ("CloudPlatHaveWorkedWith", "Kubernetes", "Kubernetes", "Cloud"),
    ("DevIDEHaveWorkedWith", "Visual Studio Code", "VS Code", "Éditeurs"),
    ("DevIDEHaveWorkedWith", "Jupyter Notebook/JupyterLab", "Jupyter", "Éditeurs"),
    ("DevIDEHaveWorkedWith", "PyCharm", "PyCharm", "Éditeurs"),
    ("DevIDEHaveWorkedWith", "Cursor", "Cursor", "Éditeurs"),
]

WANT_COLUMN = {
    "LanguagesHaveWorkedWith": "LanguagesWantToWorkWith",
    "DatabasesHaveWorkedWith": "DatabasesWantToWorkWith",
    "CloudPlatHaveWorkedWith": "CloudPlatWantToWorkWith",
    "DevIDEHaveWorkedWith": "DevIDEWantToWorkWith",
}
