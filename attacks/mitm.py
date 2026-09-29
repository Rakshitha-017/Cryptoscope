"""Educational Diffie-Hellman man-in-the-middle demonstration.

This models an attacker replacing unauthenticated DH public values.
All parameters are intentionally toy-sized for educational use.
"""

from crypto.diffie_hellman import (
    DHParameters,
    calculate_public_key,
    calculate_shared_secret,
)
from utils.math import is_prime


def simulate_mitm(
    prime: int,
    generator: int,
    alice_private: int,
    bob_private: int,
    attacker_private_alice: int = 5,
    attacker_private_bob: int = 7,
):
    """Simulate a DH MITM attack against unauthenticated public values."""

    # Validate parameters
    if not isinstance(prime, int) or not is_prime(prime):
        raise ValueError("prime must be a valid prime integer.")

    if not isinstance(generator, int) or not (1 < generator < prime):
        raise ValueError("generator must satisfy 1 < generator < prime.")

    for name, private_key in [
        ("Alice", alice_private),
        ("Bob", bob_private),
        ("Attacker A", attacker_private_alice),
        ("Attacker B", attacker_private_bob),
    ]:
        if not isinstance(private_key, int) or not (1 < private_key < prime - 1):
            raise ValueError(
                f"{name} private key must be between 1 and prime - 1."
            )

    # Keep the parameter object for visualization/documentation.
    params = DHParameters(prime=prime, generator=generator)
    params.validate()

    # ---------------------------------------------------------
    # 1. Alice and Bob generate their genuine public keys
    # ---------------------------------------------------------
    alice_public = calculate_public_key(
        alice_private,
        generator,
        prime,
    )

    bob_public = calculate_public_key(
        bob_private,
        generator,
        prime,
    )

    # ---------------------------------------------------------
    # 2. Attacker generates TWO fake public keys
    # ---------------------------------------------------------
    attacker_public_a = calculate_public_key(
        attacker_private_alice,
        generator,
        prime,
    )

    attacker_public_b = calculate_public_key(
        attacker_private_bob,
        generator,
        prime,
    )

    # ---------------------------------------------------------
    # 3. Alice receives attacker's public key
    #
    # Alice thinks this came from Bob.
    # ---------------------------------------------------------
    alice_attacker_secret = calculate_shared_secret(
        alice_private,
        attacker_public_a,
        prime,
    )

    attacker_alice_secret = calculate_shared_secret(
        attacker_private_alice,
        alice_public,
        prime,
    )

    # ---------------------------------------------------------
    # 4. Bob receives attacker's other public key
    #
    # Bob thinks this came from Alice.
    # ---------------------------------------------------------
    bob_attacker_secret = calculate_shared_secret(
        bob_private,
        attacker_public_b,
        prime,
    )

    attacker_bob_secret = calculate_shared_secret(
        attacker_private_bob,
        bob_public,
        prime,
    )

    # What Alice and Bob would have shared without an attacker
    direct_alice_bob_secret = calculate_shared_secret(
        alice_private,
        bob_public,
        prime,
    )

    mitm_success = (
        alice_attacker_secret == attacker_alice_secret
        and bob_attacker_secret == attacker_bob_secret
        and alice_attacker_secret != bob_attacker_secret
    )

    return {
        "parameters": {
            "prime": prime,
            "generator": generator,
        },

        "alice": {
            "private": alice_private,
            "original_public": alice_public,
            "received_public": attacker_public_a,
            "derived_secret": alice_attacker_secret,
        },

        "bob": {
            "private": bob_private,
            "original_public": bob_public,
            "received_public": attacker_public_b,
            "derived_secret": bob_attacker_secret,
        },

        "attacker": {
            "private_a": attacker_private_alice,
            "private_b": attacker_private_bob,
            "public_a": attacker_public_a,
            "public_b": attacker_public_b,
            "secret_with_alice": attacker_alice_secret,
            "secret_with_bob": attacker_bob_secret,
        },

        "direct_alice_bob_secret": direct_alice_bob_secret,

        "mitm_success": mitm_success,

        "lesson": (
            "Unauthenticated Diffie-Hellman does not prove who supplied "
            "a public value. Authentication or digital signatures are "
            "needed to prevent public-key substitution."
        ),
    }