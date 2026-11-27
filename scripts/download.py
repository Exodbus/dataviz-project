"""Télécharge les fichiers du Stack Overflow Developer Survey 2025 et 2026 dans data/raw/.

Chaque fichier est vérifié par son empreinte SHA-256 : si l'archive officielle change,
le script s'arrête au lieu de produire des chiffres différents de ceux de la note de cadrage.
La logique vit dans src/so_ece/download.py, partagée avec l'app (téléchargement automatique).

Usage : uv run python scripts/download.py
"""

import sys

from so_ece.download import ChecksumError, ensure_data

if __name__ == "__main__":
    try:
        ensure_data()
    except ChecksumError as e:
        print(f"ERREUR {e}", file=sys.stderr)
        sys.exit(1)
