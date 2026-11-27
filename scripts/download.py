"""Télécharge les données du sondage Stack Overflow (2025 et 2026) dans data/raw/.

On vérifie le SHA-256 de chaque fichier. Si Stack Overflow modifie l'archive, le script
s'arrête : sinon on obtiendrait d'autres chiffres que ceux de la note de cadrage.
Le code est dans src/so_ece/download.py (l'app s'en sert aussi pour télécharger
les données au premier lancement).

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
