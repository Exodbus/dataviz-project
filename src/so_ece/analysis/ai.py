"""Indicateurs sur l'usage de l'IA (axe 4 « IA au quotidien »)."""

from __future__ import annotations

import pandas as pd

NO_AI_2026 = "I don’t use AI tools"  # apostrophe typographique, comme dans le fichier 2026
GOOD_COMPLEX = ("Good, but not great at handling complex tasks", "Very well at handling complex tasks")


def uses_ai(df: pd.DataFrame) -> pd.Series:
    """Booléen par répondant ayant répondu à AISelect. La question diffère entre 2025 et 2026."""
    answers = df["AISelect"].dropna()
    year = int(df["year"].iloc[0]) if len(df) else 2026
    if year == 2025:
        return answers.str.startswith("Yes")
    return answers != NO_AI_2026


def share_uses_ai(df: pd.DataFrame) -> tuple[float, int]:
    s = uses_ai(df)
    return (float(s.mean() * 100), len(s)) if len(s) else (float("nan"), 0)


def complex_good_share(df: pd.DataFrame) -> tuple[float, int]:
    """Part des utilisateurs d'IA qui la jugent bonne sur les tâches complexes.

    En 2026, la question n'est posée qu'aux utilisateurs d'IA ; en 2025 elle l'était à tous.
    On restreint donc 2025 aux utilisateurs d'IA pour comparer des populations comparables.
    """
    sub = df
    if len(df) and int(df["year"].iloc[0]) == 2025:
        users = uses_ai(df)
        sub = df.loc[users[users].index]
    answers = sub["AIComplex"].dropna()
    if not len(answers):
        return float("nan"), 0
    return float(answers.isin(GOOD_COMPLEX).mean() * 100), len(answers)
