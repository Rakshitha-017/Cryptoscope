# Member A Implementation Log

## Dependencies

- Added `streamlit` to `requirements.txt` because the application pages are designed to run as a Streamlit app.
- Added `pytest` to `requirements.txt` because the repository uses pytest for its automated tests.
- The cryptography implementation uses Python's standard library for randomness and SHA-256, so no third-party crypto package was added.

## `utils/math.py`

- Added modular exponentiation with validation for positive moduli and non-negative exponents. This is the reusable square-and-multiply operation used by RSA and Diffie-Hellman.
- Added `gcd` and `extended_gcd` for key-generation arithmetic.
- Added modular inverse with clear errors when an inverse does not exist.
- Added deterministic trial-division primality checking suitable for the project's small educational values.
- Added configurable prime generation with an injectable random source so tests can remain reproducible.

## `utils/helpers.py`

- Added UTF-8 text/bytes conversion and big-endian bytes/integer conversion for displaying and processing messages.
- Added positive-integer validation and hexadecimal formatting helpers for shared page input and output handling.
- Kept this module independent of Streamlit so the crypto code and tests can use it directly.

## `crypto/rsa.py`

- Added immutable public/private key dataclasses and an `RSAKeyPair` container.
- Added key generation from supplied educational primes or generated primes, including validation of distinct primes and a coprime public exponent.
- Added integer encryption, decryption, signing, and verification with modulus-range validation.
- Added `intermediate_values` for Algorithm Lab visualizations without exposing implementation details.
- This is intentionally toy RSA for education and must not be used for production security.

## `crypto/diffie_hellman.py`

- Added validated parameter representation, private-key generation, public-key calculation, and shared-secret calculation.
- Added `exchange_values` to expose public values and both derived secrets for educational visualization.
- Validation rejects non-prime parameters and invalid private/public key ranges.

## `crypto/sha256.py`

- Added `hash_text`, `hash_bytes`, and `sha256` wrappers around `hashlib.sha256`.
- Text is encoded as UTF-8 and all results are predictable lowercase hexadecimal digests.
- SHA-256 is hashing, not encryption.

## `tests/test_crypto.py`

- Added tests for arithmetic identities and invalid inputs.
- Added conversion round-trip and boundary tests.
- Added RSA round-trip, signatures, intermediate values, and invalid-key/message tests.
- Added Diffie-Hellman public-key and shared-secret agreement tests.
- Added SHA-256 empty-string and standard `abc` test vectors for text and bytes.

## `crypto/cli.py`

- Added an interactive command-line runner so users can enter their own RSA or Diffie-Hellman values.
- Run it with `python -m crypto.cli` from the project root.
- RSA prompts for two distinct primes and an integer message smaller than their product.
- Diffie-Hellman prompts for a prime, generator, and both private keys, then displays public keys and matching shared secrets.

## Public APIs for page integration

- Math: `modular_exponentiation`, `gcd`, `extended_gcd`, `modular_inverse`, `is_prime`, `generate_prime`.
- Helpers: `text_to_bytes`, `bytes_to_int`, `int_to_bytes`, `validate_positive_integer`, `format_hex`.
- RSA: `generate_keypair`, `encrypt`, `decrypt`, `sign`, `verify`, `intermediate_values`.
- Diffie-Hellman: `DHParameters`, `generate_private_key`, `calculate_public_key`, `calculate_shared_secret`, `exchange_values`.
- SHA-256: `hash_text`, `hash_bytes`, `sha256`.

## Validation

- Direct smoke checks passed for all three crypto modules.
- `./venv/bin/python -m pytest tests/test_crypto.py -q` passed all 5 tests after installing `requirements.txt`.
- All existing project packages import successfully from the repository root.
