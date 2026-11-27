"""Questions à choix multiples : découpage sur « ; » et correspondance exacte.

Règle de la note de cadrage : on compare les réponses mot pour mot après découpage.
Une recherche de texte (str.contains) compterait « MicroPython » comme « Python ».
"""

from __future__ import annotations

import pandas as pd

SEP = ";"


def split_multi(cell: str) -> list[str]:
    return [item.strip() for item in cell.split(SEP) if item.strip()]


def respondents(df: pd.DataFrame, col: str) -> pd.Series:
    """Réponses non vides d'une question : c'est le dénominateur de toutes les parts."""
    return df[col].dropna()


def has_item(answers: pd.Series, item: str) -> pd.Series:
    return answers.map(lambda cell: item in split_multi(cell))


def share(df: pd.DataFrame, col: str, item: str) -> tuple[float, int]:
    """Part (en %) des répondants à la question qui ont coché `item`, et effectif n."""
    answers = respondents(df, col)
    n = len(answers)
    if n == 0:
        return float("nan"), 0
    return float(has_item(answers, item).mean() * 100), n


def shares_table(df: pd.DataFrame, col: str) -> pd.DataFrame:
    """Toutes les réponses d'une question, avec leur part et l'effectif commun n."""
    answers = respondents(df, col)
    n = len(answers)
    counts = answers.map(split_multi).explode().value_counts()
    table = counts.rename("count").to_frame()
    table["share"] = table["count"] / n * 100 if n else float("nan")
    table["n"] = n
    table.index.name = "item"
    return table.reset_index().sort_values("share", ascending=False, ignore_index=True)


def admired(df: pd.DataFrame, have_col: str, want_col: str, item: str, min_users: int = 30) -> tuple[float, int]:
    """Parmi les utilisateurs de `item`, part qui veut continuer. NaN sous `min_users` utilisateurs."""
    both = df[[have_col, want_col]].dropna()
    users = both[has_item(both[have_col], item)]
    if len(users) < min_users:
        return float("nan"), len(users)
    return float(has_item(users[want_col], item).mean() * 100), len(users)
