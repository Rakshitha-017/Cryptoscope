"""Non-invasive heuristic analyzer for educational password/text analysis.

The original secret is never returned, printed, or stored by this module.
"""

import re
from dataclasses import asdict, dataclass
from typing import List


COMMON_PATTERNS = {
    "password", "password123", "admin", "admin123", "qwerty",
    "qwerty123", "letmein", "welcome", "iloveyou", "123456",
    "12345678", "123456789", "abc123",
}


@dataclass(frozen=True)
class Finding:
    severity: str
    issue: str
    explanation: str
    recommendation: str

    def as_dict(self):
        return asdict(self)


def _severity_for_length(length: int) -> str:
    if length < 8:
        return "HIGH"
    if length < 12:
        return "MEDIUM"
    return "LOW"


def _has_sequential_pattern(value: str) -> bool:
    lowered = value.lower()
    sequences = (
        "abcdefghijklmnopqrstuvwxyz",
        "0123456789",
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm",
    )
    for seq in sequences:
        for i in range(len(seq) - 2):
            if seq[i:i+3] in lowered or seq[i:i+3][::-1] in lowered:
                return True
    return False


def analyze_secret(secret: str) -> List[dict]:
    if secret is None:
        raise ValueError("Input cannot be None.")
    if not isinstance(secret, str):
        raise TypeError("Input must be text.")
    if secret == "":
        return [{
            "severity": "HIGH",
            "issue": "Empty input",
            "explanation": "No secret was supplied for analysis.",
            "recommendation": "Provide a non-empty example for the educational analysis.",
        }]

    findings = []
    length = len(secret)

    if length < 8:
        findings.append(Finding(
            "HIGH", "Short input",
            "Very short secrets have a much smaller search space.",
            "Use a longer passphrase or password.",
        ))
    elif length < 12:
        findings.append(Finding(
            "MEDIUM", "Moderate length",
            "The input is longer than the minimum baseline but could be strengthened.",
            "Prefer 12 or more characters when practical.",
        ))
    else:
        findings.append(Finding(
            "LOW", "Good length",
            "The input meets the analyzer's length heuristic.",
            "Keep using long, unique secrets.",
        ))

    classes = sum([
        bool(re.search(r"[a-z]", secret)),
        bool(re.search(r"[A-Z]", secret)),
        bool(re.search(r"\d", secret)),
        bool(re.search(r"[^A-Za-z0-9]", secret)),
    ])
    if classes <= 1:
        findings.append(Finding(
            "MEDIUM", "Low character diversity",
            "Only one character class is present.",
            "Mix character classes or, preferably, use a long unique passphrase.",
        ))
    else:
        findings.append(Finding(
            "LOW", "Character diversity",
            "Multiple character classes are present.",
            "Maintain uniqueness and avoid predictable substitutions.",
        ))

    lowered = secret.lower()
    if lowered in COMMON_PATTERNS or any(p in lowered for p in COMMON_PATTERNS):
        findings.append(Finding(
            "HIGH", "Common-password pattern",
            "The input contains a commonly guessed password pattern.",
            "Avoid dictionary words and well-known password patterns.",
        ))

    if re.search(r"(.)\1{2,}", secret):
        findings.append(Finding(
            "MEDIUM", "Repeated characters",
            "The input contains a repeated-character sequence.",
            "Avoid predictable repetitions.",
        ))

    if _has_sequential_pattern(secret):
        findings.append(Finding(
            "MEDIUM", "Sequential pattern",
            "The input contains an obvious keyboard or alphanumeric sequence.",
            "Avoid sequences such as abc, 123, or keyboard runs.",
        ))

    # Never include the original input in findings.
    return [f.as_dict() if isinstance(f, Finding) else f for f in findings]


def analyze_text(secret: str) -> List[dict]:
    """Alias kept simple for page integration."""
    return analyze_secret(secret)


def summarize_findings(findings: List[dict]) -> dict:
    counts = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for finding in findings:
        severity = finding.get("severity", "MEDIUM")
        counts[severity] = counts.get(severity, 0) + 1
    overall = "HIGH" if counts["HIGH"] else "MEDIUM" if counts["MEDIUM"] else "LOW"
    return {"overall": overall, "counts": counts}
