"""Educational toy-RSA weakness demonstration.

This module demonstrates why very small RSA moduli are factorable. It is
deliberately bounded and rejects large moduli.
"""

from math import isqrt

from crypto.rsa import decrypt


MAX_DEMO_MODULUS = 1_000_000


def _factor_small_modulus(n: int):
    if not isinstance(n, int) or n <= 1:
        raise ValueError("n must be an integer greater than 1.")
    if n > MAX_DEMO_MODULUS:
        raise ValueError(
            f"Educational RSA attack only accepts n <= {MAX_DEMO_MODULUS}."
        )
    for p in range(2, isqrt(n) + 1):
        if n % p == 0:
            q = n // p
            if p != q and p * q == n:
                return p, q
    return None


def factor_modulus(n: int):
    """Return toy RSA factors or None if no small factor is found."""
    return _factor_small_modulus(n)


def demonstrate_factorization(n: int, e: int, ciphertext: int):
    if not all(isinstance(x, int) for x in (n, e, ciphertext)):
        raise TypeError("n, e and ciphertext must be integers.")
    if n <= 1:
        raise ValueError("n must be greater than 1.")
    if not 1 < e < n:
        raise ValueError("e must satisfy 1 < e < n.")
    if not 0 <= ciphertext < n:
        raise ValueError("ciphertext must be in [0, n).")

    factors = _factor_small_modulus(n)
    if factors is None:
        return {
            "success": False,
            "factors": None,
            "message": None,
            "lesson": "The bounded factorization demo could not factor this toy modulus.",
            "mitigation": "Use sufficiently large RSA parameters and secure padding in real systems.",
        }

    p, q = factors
    phi = (p - 1) * (q - 1)

    # Compute d without importing private implementation details.
    from utils.math import modular_inverse
    d = modular_inverse(e, phi)
    message = decrypt(ciphertext, type("PrivateKey", (), {"d": d, "n": n})())

    return {
        "success": True,
        "factors": (p, q),
        "phi": phi,
        "recovered_private_exponent": d,
        "message": message,
        "lesson": "Factoring a weak RSA modulus reveals the private exponent.",
        "mitigation": "Use adequately sized RSA keys, secure padding such as OAEP, and authenticated protocols.",
    }


# Friendly alias for pages/tests.
rsa_weak_key_attack = demonstrate_factorization
