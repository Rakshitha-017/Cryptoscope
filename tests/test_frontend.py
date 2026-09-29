import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_page_files_exist():
    expected = [
        ROOT / "pages" / "01_Algorithm_Lab.py",
        ROOT / "pages" / "02_Attack_Lab.py",
        ROOT / "pages" / "03_Security_Analyzer.py",
    ]
    assert all(path.exists() for path in expected)


def test_attack_modules_import():
    import attacks.hash_attack
    import attacks.mitm
    import attacks.rsa_attack
    import utils.analyzer
