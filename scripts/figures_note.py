"""Recalcule les chiffres clés de la note de cadrage, pour vérifier qu'ils sont reproductibles.

Usage : uv run python scripts/figures_note.py
"""

import pandas as pd

from so_ece.analysis.ai import complex_good_share, share_uses_ai
from so_ece.analysis.compare import compare_items
from so_ece.analysis.multi import share
from so_ece.dataset import load_year
from so_ece.labels import pct, points
from so_ece.population import Filters, apply_region, select_data_profiles, select_other_devs

d25, d26 = load_year(2025), load_year(2026)
f = Filters(region="Europe")
e25, e26 = select_data_profiles(d25, f), select_data_profiles(d26, f)
o26 = select_other_devs(d26, f)

print(f"Profils data/IA en Europe : {len(e25)} en 2025, {len(e26)} en 2026 ; autres devs 2026 : {len(o26)}")
print(f"Profils data/IA monde 2026 : {int(d26['is_data'].sum())} ; France : {int((d26['is_data'] & (d26['Country'] == 'France')).sum())}")

cmp = pd.concat([
    compare_items(e25, e26, "DatabasesHaveWorkedWith", ["DuckDB"]),
    compare_items(e25, e26, "DevIDEHaveWorkedWith", ["Jupyter Notebook/JupyterLab"]),
])
for _, r in cmp.iterrows():
    print(f"{r['item']}: {pct(r['share_a'])} -> {pct(r['share_b'])} ({points(r['diff'])} ± {r['ci']:.1f}, significatif={r['significant']})")

p, n = share(e26, "LanguagesHaveWorkedWith", "Python")
print(f"Python, profils data/IA Europe 2026 : {pct(p)} (n = {n})")
p, n = share_uses_ai(e26)
print(f"Utilisent l'IA : {pct(p)} (n = {n})")
for df, y in ((e25, 2025), (e26, 2026)):
    p, n = complex_good_share(df)
    print(f"IA bonne sur tâches complexes, utilisateurs d'IA {y} : {pct(p)} (n = {n})")

fr26 = apply_region(d26, "Monde")
fr26 = fr26[fr26["Country"] == "France"]
p, n = share(fr26, "LanguagesHaveWorkedWith", "Python")
print(f"France, tous développeurs 2026, Python : {pct(p)} (n = {n})")
