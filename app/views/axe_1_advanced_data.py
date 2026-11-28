"""Axe 1 : Advanced Data (SQL). Bases transactionnelles contre bases analytiques."""

from ui_axis import header, starter_view

f = header(
    "1. Advanced Data (SQL)",
    "PostgreSQL suffit-il, ou faut-il enseigner le SQL analytique (DuckDB, Databricks SQL, BigQuery, Snowflake) ?",
    "axis-1",
    "Corentin",
)
starter_view(f, "DatabasesHaveWorkedWith", "Bases de données utilisées")

# À faire sur la branche de l'axe :
# - évolution 2025 -> 2026 avec intervalle (so_ece.analysis.compare.compare_items)
# - profils data/IA face aux autres développeurs (ui_data.other_devs)
# - transactionnelles vs analytiques, désirées et appréciées
