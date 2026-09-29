import hashlib

import pytest

from attacks.hash_attack import dictionary_attack, brute_force_attack
from attacks.mitm import simulate_mitm
from attacks.rsa_attack import factor_modulus
from utils.analyzer import analyze_secret, summarize_findings


def test_dictionary_hash_attack_success():
    target = hashlib.sha256(b"admin123").hexdigest()
    result = dictionary_attack(target, ["password", "admin", "admin123"])
    assert result["found"] is True
    assert result["recovered"] == "admin123"
    assert result["attempts"] == 3


def test_dictionary_hash_attack_failure():
    target = hashlib.sha256(b"admin123").hexdigest()
    result = dictionary_attack(target, ["password", "admin"])
    assert result["found"] is False
    assert result["attempts"] == 2


@pytest.mark.parametrize("bad", ["abc", "g" * 64, "", "0" * 63])
def test_invalid_hash(bad):
    with pytest.raises(ValueError):
        dictionary_attack(bad, ["test"])


def test_bruteforce_is_deterministic():
    target = hashlib.sha256(b"ab").hexdigest()
    r1 = brute_force_attack(target, alphabet="ab", max_length=2)
    r2 = brute_force_attack(target, alphabet="ab", max_length=2)
    assert r1 == r2
    assert r1["found"] is True
    assert r1["recovered"] == "ab"


def test_mitm_creates_two_attacker_secrets():
    result = simulate_mitm(23, 5, 6, 15)
    assert result["mitm_success"] is True
    assert result["attacker"]["secret_with_alice"] == result["alice"]["derived_secret"]
    assert result["attacker"]["secret_with_bob"] == result["bob"]["derived_secret"]
    assert result["alice"]["derived_secret"] != result["bob"]["derived_secret"]


def test_small_rsa_modulus_can_be_factored():
    assert factor_modulus(3233) == (53, 61)


def test_analyzer_weak_input():
    findings = analyze_secret("123456")
    summary = summarize_findings(findings)
    assert summary["counts"]["HIGH"] >= 1


def test_analyzer_stronger_input():
    findings = analyze_secret("correct-horse-battery")
    assert findings
    assert all("correct-horse-battery" not in str(f) for f in findings)


def test_analyzer_empty_input():
    findings = analyze_secret("")
    assert findings[0]["severity"] == "HIGH"
