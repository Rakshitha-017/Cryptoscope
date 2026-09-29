"""Educational bounded SHA-256 dictionary/brute-force demonstration."""

import itertools
import string
from typing import Iterable, Optional

from crypto.sha256 import hash_text


MAX_CANDIDATES = 10_000


def _validate_target(target_hash: str) -> str:
    if not isinstance(target_hash, str):
        raise TypeError("Target hash must be a string.")
    target_hash = target_hash.strip().lower()
    if len(target_hash) != 64:
        raise ValueError("SHA-256 hashes must contain exactly 64 hexadecimal characters.")
    try:
        int(target_hash, 16)
    except ValueError as exc:
        raise ValueError("Target hash must be hexadecimal.") from exc
    return target_hash


def dictionary_attack(target_hash: str, candidates: Iterable[str], max_attempts: int = MAX_CANDIDATES):
    """Try a bounded candidate list. This is intentionally educational."""
    target_hash = _validate_target(target_hash)
    if max_attempts < 1 or max_attempts > MAX_CANDIDATES:
        raise ValueError(f"max_attempts must be between 1 and {MAX_CANDIDATES}.")

    attempts = 0
    for candidate in candidates:
        if attempts >= max_attempts:
            break
        if not isinstance(candidate, str):
            continue
        attempts += 1
        if hash_text(candidate) == target_hash:
            return {
                "found": True,
                "recovered": candidate,
                "attempts": attempts,
                "method": "dictionary",
            }
    return {
        "found": False,
        "recovered": None,
        "attempts": attempts,
        "method": "dictionary",
    }


def brute_force_attack(
    target_hash: str,
    alphabet: str = string.ascii_lowercase,
    max_length: int = 3,
    max_attempts: int = MAX_CANDIDATES,
):
    """Bounded brute-force demonstration for very small toy inputs."""
    target_hash = _validate_target(target_hash)
    if not alphabet or len(alphabet) > 64:
        raise ValueError("Use a non-empty alphabet of at most 64 characters.")
    if max_length < 1 or max_length > 6:
        raise ValueError("max_length must be between 1 and 6.")
    if max_attempts < 1 or max_attempts > MAX_CANDIDATES:
        raise ValueError(f"max_attempts must be between 1 and {MAX_CANDIDATES}.")

    attempts = 0
    for length in range(1, max_length + 1):
        for chars in itertools.product(alphabet, repeat=length):
            if attempts >= max_attempts:
                return {
                    "found": False, "recovered": None,
                    "attempts": attempts, "method": "brute-force",
                    "bounded": True,
                }
            candidate = "".join(chars)
            attempts += 1
            if hash_text(candidate) == target_hash:
                return {
                    "found": True, "recovered": candidate,
                    "attempts": attempts, "method": "brute-force",
                    "bounded": True,
                }
    return {
        "found": False, "recovered": None,
        "attempts": attempts, "method": "brute-force",
        "bounded": True,
    }


def attack_hash(target_hash: str, candidates: Optional[Iterable[str]] = None, **kwargs):
    """Convenience API used by the Streamlit page."""
    if candidates is not None:
        return dictionary_attack(target_hash, candidates, **kwargs)
    return brute_force_attack(target_hash, **kwargs)
