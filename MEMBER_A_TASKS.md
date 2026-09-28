# Member A Tasks

This checklist covers the cryptography and shared utility work for CRYPTOSCOPE.

## 1. Prepare the development environment

- [ ] Create and activate a Python virtual environment.
- [ ] Decide the supported Python version with the team.
- [x] Add only required dependencies to `requirements.txt`.
- [ ] Agree with Member B on function names, parameters, return values, and error behavior before implementing shared code.

## 2. Implement mathematical utilities

File: `utils/math.py`

- [x] Implement modular exponentiation.
- [x] Implement the greatest common divisor function.
- [x] Implement the extended Euclidean algorithm.
- [x] Implement modular multiplicative inverse.
- [x] Add primality checking suitable for the educational project.
- [x] Add prime generation helpers if RSA needs them.
- [x] Validate invalid inputs such as non-positive moduli and unavailable inverses.
- [x] Keep functions deterministic where practical so tests are reproducible.

## 3. Implement helper utilities

File: `utils/helpers.py`

- [x] Add conversions needed by the crypto modules, such as text/bytes/integer conversion.
- [x] Add input validation helpers shared by the algorithm pages.
- [x] Add formatting helpers for displaying keys, hashes, and intermediate values.
- [x] Keep helpers small and independent of Streamlit or page-specific code.
- [x] Document the expected input and output for each public helper.

## 4. Implement RSA

File: `crypto/rsa.py`

- [x] Define a clear key representation for public and private keys.
- [x] Implement key generation using the functions from `utils/math.py`.
- [x] Implement encryption for supported messages.
- [x] Implement decryption.
- [x] Implement signing and verification if required by the project design.
- [x] Validate that messages are in the supported range before modular arithmetic.
- [x] Expose intermediate values needed by the Algorithm Lab without duplicating the algorithm.
- [x] Handle invalid keys and invalid ciphertext with clear errors.
- [x] Verify that encrypting and then decrypting a valid message returns the original message.

## 5. Implement Diffie-Hellman

File: `crypto/diffie_hellman.py`

- [x] Define the public parameters and private/public key flow.
- [x] Implement private key generation or accept caller-provided private values.
- [x] Implement public key calculation.
- [x] Implement shared-secret calculation.
- [x] Validate parameters and reject invalid private keys.
- [x] Make sure both participants calculate the same shared secret.
- [x] Return intermediate values needed for educational visualization.

## 6. Implement SHA-256 functionality

File: `crypto/sha256.py`

- [x] Decide whether the module wraps Python's standard-library SHA-256 implementation or demonstrates the algorithm internally.
- [x] Implement hashing for text and byte input consistently.
- [x] Return a predictable hexadecimal digest format.
- [x] Add optional intermediate or comparison data only if the UI requires it.
- [x] Verify the implementation against known SHA-256 test vectors.
- [x] Do not describe hashing as encryption in the UI or documentation.

## 7. Add crypto tests

File: `tests/test_crypto.py`

- [x] Test modular arithmetic utilities, including edge cases.
- [x] Test RSA key generation and encrypt/decrypt round trips.
- [x] Test RSA invalid-message and invalid-key handling.
- [x] Test Diffie-Hellman public-key calculations.
- [x] Test that both Diffie-Hellman participants derive the same shared secret.
- [x] Test SHA-256 with an empty string and known standard vectors.
- [x] Test text, bytes, and boundary inputs supported by the public API.
- [x] Keep tests independent and deterministic.

## 8. Coordinate shared interfaces with Member B

- [ ] Share the public APIs of `crypto/rsa.py`, `crypto/diffie_hellman.py`, and `crypto/sha256.py`.
- [ ] Share the public APIs of `utils/math.py` and `utils/helpers.py`.
- [ ] Tell Member B which values are safe and useful to display in the pages.
- [ ] Tell Member B which exceptions or validation messages the UI should handle.
- [ ] Confirm how `app.py` and the pages will import the modules.
- [ ] Avoid changing Member B's attack, analyzer, page, and frontend test files without agreement.

## 9. Integration check

- [x] Run the full crypto test file.
- [ ] Run the complete test suite after Member B's modules are available.
- [x] Check imports from the project root.
- [ ] Check that the UI can call the public crypto APIs without accessing private implementation details.
- [x] Review for accidental secrets, debug prints, or hard-coded production keys.
- [x] Confirm that educationally small parameters are clearly labeled as demonstrations and not production cryptography.

## 10. Handoff to the team

- [ ] Summarize implemented functions and their signatures.
- [ ] List dependencies added to `requirements.txt`.
- [ ] List test commands and their results.
- [ ] Note any limitations, especially toy RSA or Diffie-Hellman parameters.
- [ ] Commit only the files assigned to Member A unless the team agrees otherwise.

## Suggested implementation order

1. `utils/math.py`
2. `utils/helpers.py`
3. `crypto/rsa.py`
4. `crypto/diffie_hellman.py`
5. `crypto/sha256.py`
6. `tests/test_crypto.py`
7. Interface coordination and integration checks

## Suggested test command

```bash
python -m pytest tests/test_crypto.py -q
```
