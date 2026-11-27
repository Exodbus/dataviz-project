"""Lecture des fichiers bruts : seulement les colonnes utiles à l'app."""

from __future__ import annotations

import pandas as pd

from .paths import RAW_FILES

# Colonnes lues, sous leur nom d'origine dans chaque fichier
COLUMNS = {
    2026: [
        "ResponseId", "Country", "Role", "WorkExp",
        "LanguagesHaveWorkedWith", "LanguagesWantToWorkWith",
        "DatabasesHaveWorkedWith", "DatabasesWantToWorkWith",
        "CloudPlatHaveWorkedWith", "CloudPlatWantToWorkWith",
        "DevIDEHaveWorkedWith", "DevIDEWantToWorkWith",
        "LLMHaveWorkedWith", "AIOrchHaveWorkedWith", "AIObsHaveWorkedWith",
        "AICodeAgentHaveWorkedWith",
        "AISelect", "AITrust", "AIWorkNext", "Disruption", "ContextWork",
        "AIComplex", "AISentiment", "LearnAI", "LearnAIHow",
    ],
    2025: [
        "ResponseId", "Country", "DevType", "WorkExp",
        "LanguageHaveWorkedWith", "LanguageWantToWorkWith",
        "DatabaseHaveWorkedWith", "DatabaseWantToWorkWith",
        "PlatformHaveWorkedWith", "PlatformWantToWorkWith",
        "DevEnvsHaveWorkedWith", "DevEnvsWantToWorkWith",
        "AIAgentOrchestration", "AISelect", "AIComplex", "AISent",
    ],
}


def read_raw(year: int) -> pd.DataFrame:
    """Lit le fichier brut d'une année. Lance une erreur claire s'il n'a pas été téléchargé."""
    path = RAW_FILES[year]
    if not path.exists():
        raise FileNotFoundError(
            f"{path} est introuvable. Lancez d'abord : uv run python scripts/download.py"
        )
    return pd.read_csv(path, usecols=COLUMNS[year], low_memory=False)
