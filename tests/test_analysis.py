import math

import pandas as pd

from so_ece.analysis.ai import complex_good_share, share_uses_ai
from so_ece.analysis.compare import compare_items, diff_ci
from so_ece.analysis.multi import admired, share, shares_table, split_multi
from so_ece.harmonise import harmonise, warnings_for
from so_ece.labels import pct, points, sample_status
from so_ece.population import Filters, add_population_columns, select_data_profiles


def test_correspondance_exacte_micropython():
    df = pd.DataFrame({"LanguagesHaveWorkedWith": ["Python;SQL", "MicroPython", "C", None]})
    p, n = share(df, "LanguagesHaveWorkedWith", "Python")
    assert n == 3  # les non-réponses ne comptent pas dans le dénominateur
    assert math.isclose(p, 100 / 3)


def test_split_multi_ignore_les_vides():
    assert split_multi("A; B;;C ") == ["A", "B", "C"]


def test_shares_table():
    df = pd.DataFrame({"x": ["A;B", "A", None]})
    t = shares_table(df, "x").set_index("item")
    assert t.loc["A", "share"] == 100 and t.loc["B", "share"] == 50 and t.loc["A", "n"] == 2


def test_admired_masque_sous_le_seuil():
    df = pd.DataFrame({"have": ["Rust"] * 10, "want": ["Rust"] * 10})
    p, n = admired(df, "have", "want", "Rust")
    assert math.isnan(p) and n == 10


def test_intervalle_et_significativite():
    # mêmes ordres de grandeur que DuckDB dans la note : 13,5 % (733) -> 19,9 % (331)
    assert math.isclose(diff_ci(13.5, 733, 19.9, 331), 4.98, abs_tol=0.05)
    a = pd.DataFrame({"x": ["A"] * 10 + ["B"] * 90})
    b = pd.DataFrame({"x": ["A"] * 40 + ["B"] * 60})
    r = compare_items(a, b, "x", ["A"]).iloc[0]
    assert r["diff"] == 30 and r["significant"]


def test_harmonisation_docker_et_colonnes():
    raw = pd.DataFrame({"PlatformHaveWorkedWith": ["Docker;Pip;AWS"], "AISent": ["Indifferent"], "DevType": ["Data engineer"]})
    h = harmonise(raw, 2025)
    assert h.loc[0, "CloudPlatHaveWorkedWith"] == "Docker / Docker Compose;pip;AWS"
    assert h.loc[0, "AISentiment"] == "Neutral"
    assert h.loc[0, "Role"] == "Data engineer"
    assert warnings_for("CloudPlatHaveWorkedWith", "Docker / Docker Compose")
    assert warnings_for("AIComplex")
    assert not warnings_for("CloudPlatHaveWorkedWith", "pip")


def test_population_europe_et_dba_regroupes():
    df = pd.DataFrame(
        {
            "Country": ["France", "France", "India", "Germany"],
            "Role": ["Database administrator or engineer", "Developer, full-stack", "Data scientist", "Data engineer"],
            "WorkExp": [3, 12, 4, 8],
        }
    )
    pop = add_population_columns(df)
    assert pop.loc[0, "role_group"] == "Data engineer et DBA"
    assert pop.loc[1, "role_group"] == "Autres développeurs"
    sel = select_data_profiles(pop, Filters(region="Europe"))
    assert list(sel["Country"]) == ["France", "Germany"]
    sel = select_data_profiles(pop, Filters(region="Monde", exp_bands=("0-5 ans",)))
    assert len(sel) == 2


def test_usage_ia_et_taches_complexes_2025_limite_aux_utilisateurs():
    d25 = pd.DataFrame(
        {
            "year": 2025,
            "AISelect": ["Yes, I use AI tools daily", "No, and I don't plan to"],
            "AIComplex": ["Very well at handling complex tasks", "Bad at handling complex tasks"],
        }
    )
    assert share_uses_ai(d25) == (50.0, 2)
    assert complex_good_share(d25) == (100.0, 1)  # le non-utilisateur est exclu
    d26 = pd.DataFrame({"year": 2026, "AISelect": ["I don’t use AI tools", "General-purpose AI chat tools"]})
    assert share_uses_ai(d26) == (50.0, 2)


def test_formats():
    assert pct(87.94) == "87,9 %"
    assert points(-11.64) == "−11,6 pt"
    assert sample_status(27) == "masqué" and sample_status(90) == "avertissement" and sample_status(331) == "ok"


def test_filtres_periode():
    from so_ece.population import COMPARE

    f = Filters()
    assert f.compare and f.level_year == 2026 and f.years == (2025, 2026) and f.others
    f = Filters(period="2025")
    assert not f.compare and f.level_year == 2025 and f.years == (2025,)


def test_autres_devs_meme_experience():
    from so_ece.population import select_other_devs

    df = pd.DataFrame(
        {
            "Country": ["France", "France", "France"],
            "Role": ["Developer, full-stack", "Developer, back-end", "Data scientist"],
            "WorkExp": [2, 15, 3],
        }
    )
    pop = add_population_columns(df)
    sel = select_other_devs(pop, Filters(exp_bands=("0-5 ans",)))
    assert list(sel["Role"]) == ["Developer, full-stack"]


def test_lecture_groupe_de_controle():
    from so_ece.analysis.home import net_ci, trend_reading

    assert trend_reading(False, 3, True, 3, 0, 1) == "Dans la marge d'incertitude"
    # cas DuckDB : +6,4 chez les profils data, +2,0 chez les autres, écart net 4,4 ± 5,0 -> pas propre aux profils data
    assert trend_reading(True, 6.4, True, 2.0, 4.4, net_ci(5.0, 0.6)).startswith("Aussi chez les autres devs")
    # cas Jupyter : −11,6 contre −2,3, écart net −9,3 ± 6,1 -> plus marqué chez les profils data
    assert trend_reading(True, -11.6, True, -2.3, -9.3, net_ci(6.1, 0.9)) == "Plus marquée chez les profils data/IA"
    assert trend_reading(True, 6, False, 0.1, 5.9, 3) == "Propre aux profils data/IA"
    assert trend_reading(True, 6, True, -2, 8, 3) == "Propre aux profils data/IA"


def test_donnees_manquantes_detectees(tmp_path):
    from so_ece.download import FILES, missing_files

    assert missing_files(tmp_path) == list(FILES)
