"""Point d'entrée unique des données : brut -> harmonisé -> colonnes de population."""

from __future__ import annotations

import pandas as pd

from .harmonise import harmonise
from .load import read_raw
from .population import add_population_columns

YEARS = (2025, 2026)


def load_year(year: int) -> pd.DataFrame:
    return add_population_columns(harmonise(read_raw(year), year))
