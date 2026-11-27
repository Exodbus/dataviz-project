"""Téléchargement des données brutes, vérifiées par SHA-256.

Utilisé par scripts/download.py (en local) et par l'app elle-même quand data/raw/ est vide
(déploiement sur Streamlit Community Cloud, qui ne lance aucun script avant l'app).

Les fichiers sont stockés avec Git LFS sur GitHub : on passe par media.githubusercontent.com,
jamais par le lien « raw », qui ne renvoie qu'un pointeur LFS.
"""

from __future__ import annotations

import hashlib
import urllib.request
from collections.abc import Callable
from pathlib import Path

from .paths import RAW_DIR

BASE = "https://media.githubusercontent.com/media/StackExchange/Survey/main/packages/archive"

# chemin local (dans data/raw/) -> (URL, SHA-256 attendu)
FILES = {
    "2026/survey_results_public.csv": (
        f"{BASE}/2026/survey_results_public.csv",
        "ad520b4d5d71f240141e63f0d6f81a3b1898cbdc69efe9ea985496533b15fc2c",
    ),
    "2026/survey_results_schema.csv": (
        f"{BASE}/2026/survey_results_schema.csv",
        "0892967cacdac5cdd1a7668de6f5edd8947bcc0ab204b7ec3e2d81084eb00b63",
    ),
    "2025/results.csv": (
        f"{BASE}/2025/results.csv",
        "2d1f65308877282edfb4470520eabbc08cb499118432a3dcec6a66c086aa2baa",
    ),
    "2025/schema.csv": (
        f"{BASE}/2025/schema.csv",
        "1d24951e04eab46c6f9fecef6ce8e6b32a0a14a3f0eecdcf62f70833a74b3ff8",
    ),
}


class ChecksumError(RuntimeError):
    pass


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def missing_files(raw_dir: Path = RAW_DIR) -> list[str]:
    """Fichiers absents de data/raw/ (vérification rapide, sans recalculer les empreintes)."""
    return [name for name in FILES if not (raw_dir / name).exists()]


def ensure_data(raw_dir: Path = RAW_DIR, log: Callable[[str], None] = print, verify_existing: bool = True) -> None:
    """Télécharge les fichiers manquants ou altérés. Lève ChecksumError si une empreinte ne correspond pas."""
    for name, (url, expected) in FILES.items():
        target = raw_dir / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and (not verify_existing or sha256(target) == expected):
            log(f"ok     {name} (déjà présent)")
            continue
        log(f"get    {name} ...")
        tmp = target.with_suffix(target.suffix + ".part")
        urllib.request.urlretrieve(url, tmp)
        got = sha256(tmp)
        if got != expected:
            tmp.unlink(missing_ok=True)
            raise ChecksumError(f"{name} : empreinte {got} au lieu de {expected}")
        tmp.replace(target)
        log(f"ok     {name}")
