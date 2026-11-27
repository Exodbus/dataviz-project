from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"

RAW_FILES = {
    2025: RAW_DIR / "2025" / "results.csv",
    2026: RAW_DIR / "2026" / "survey_results_public.csv",
}
