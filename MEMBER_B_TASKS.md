# Member B Tasks

This checklist covers the attack demonstrations, security analyzer, Streamlit pages, frontend tests, and integration work for CRYPTOSCOPE.

## 1. Prepare the development environment

- [ ] Activate the project virtual environment.
- [ ] Install dependencies with `python -m pip install -r requirements.txt`.
- [ ] Confirm imports from the project root.
- [ ] Run the current tests with `python -m pytest -q`.
- [ ] Agree with Member A on the public crypto APIs before integrating pages.

## 2. Implement hash attacks

File: `attacks/hash_attack.py`

- [ ] Implement a small educational dictionary or brute-force hash attack.
- [ ] Accept a target hash and a controlled candidate word list or character range.
- [ ] Support SHA-256 through `crypto.sha256` rather than duplicating hashing logic.
- [ ] Return a clear result containing whether a match was found, the recovered input if found, and the number of attempts.
- [ ] Validate the hash format and reject unsupported input sizes or unsafe search ranges.
- [ ] Make the attack deterministic for tests.
- [ ] Clearly label the feature as an educational demonstration, not a production password-cracking tool.

## 3. Implement man-in-the-middle demonstration

File: `attacks/mitm.py`

- [ ] Demonstrate how an attacker can substitute public Diffie-Hellman values when authentication is absent.
- [ ] Use `crypto.diffie_hellman` for the underlying public-key and shared-secret calculations.
- [ ] Model Alice, Bob, and the attacker with explicit public/private values.
- [ ] Return intermediate public keys and the two attacker-controlled shared secrets for visualization.
- [ ] Show that Alice and Bob do not share the same secret directly in the intercepted exchange.
- [ ] Validate prime, generator, and private-key inputs.
- [ ] Keep all values toy-sized and clearly marked as demonstrations.

## 4. Implement RSA attack demonstration

File: `attacks/rsa_attack.py`

- [ ] Implement an educational attack or weakness demonstration appropriate for toy RSA.
- [ ] Document the assumptions and why the attack works with small demonstration keys.
- [ ] Reuse `crypto.rsa` and `utils.math` instead of duplicating RSA operations.
- [ ] Return structured results suitable for display in the Algorithm Lab or Attack Lab.
- [ ] Reject production-sized or unsafe inputs if the demonstration is intended only for small keys.
- [ ] Explain the security lesson and mitigation, such as larger keys, secure padding, and authenticated encryption.

## 5. Implement security analyzer

File: `utils/analyzer.py`

- [ ] Define a stable analyzer result format with severity, issue, explanation, and recommendation fields.
- [ ] Analyze user-provided passwords or text without storing secrets or printing them.
- [ ] Check password length, character diversity, common-password patterns, and obvious repeated/sequential patterns.
- [ ] Provide educational findings without claiming that a heuristic is a complete security assessment.
- [ ] Reuse `crypto.sha256` only when a hash demonstration is explicitly requested.
- [ ] Keep analyzer functions independent of Streamlit so they can be unit tested.
- [ ] Add input validation and clear behavior for empty input.

## 6. Build the Streamlit application shell

File: `app.py`

- [ ] Create the application title and concise project description.
- [ ] Add navigation or clear links to the three pages.
- [ ] Explain that the cryptographic values are small educational examples and are not production security.
- [ ] Keep secrets and user inputs out of logs and source code.
- [ ] Verify the application starts with `streamlit run app.py`.

## 7. Build Algorithm Lab page

File: `pages/01_Algorithm_Lab.py`

- [ ] Add controls for RSA key generation and message encryption/decryption.
- [ ] Display public key, private key, ciphertext, plaintext, and safe intermediate values from `intermediate_values`.
- [ ] Add controls for Diffie-Hellman parameters and both participant private keys.
- [ ] Display public keys and both shared secrets using `exchange_values`.
- [ ] Add SHA-256 text and byte-oriented demonstrations with hexadecimal output.
- [ ] Validate inputs before calling crypto functions.
- [ ] Catch expected validation errors and show useful user-facing messages.
- [ ] Do not call hashing encryption.
- [ ] Label toy parameters and avoid implying production readiness.

## 8. Build Attack Lab page

File: `pages/02_Attack_Lab.py`

- [ ] Add a separate interface for the hash attack demonstration.
- [ ] Add a separate interface for the Diffie-Hellman man-in-the-middle demonstration.
- [ ] Add a separate interface for the RSA weakness demonstration.
- [ ] Display attack assumptions, intermediate values, result status, and mitigation guidance.
- [ ] Put bounds on candidate lists, search lengths, and computational work so the UI remains responsive.
- [ ] Handle invalid inputs without exposing stack traces to users.
- [ ] Make clear that the demonstrations are for authorized educational use only.

## 9. Build Security Analyzer page

File: `pages/03_Security_Analyzer.py`

- [ ] Add a text input area for analyzer demonstrations.
- [ ] Display findings grouped by severity.
- [ ] Display actionable recommendations from `utils.analyzer`.
- [ ] Do not display or log the original secret after analysis.
- [ ] Explain limitations of heuristic analysis.
- [ ] Add empty-input and invalid-input handling.

## 10. Add attack, analyzer, and frontend tests

Files: `tests/test_attacks.py`, `tests/test_frontend.py`

- [ ] Test hash attack success, failure, invalid hashes, and deterministic attempt counts.
- [ ] Test man-in-the-middle public-key substitution and attacker shared secrets.
- [ ] Test RSA attack behavior and invalid-input handling.
- [ ] Test analyzer findings for weak, strong, empty, and repetitive input.
- [ ] Test that page modules import successfully from the project root.
- [ ] Test key page functions without requiring a running browser where possible.
- [ ] Add Streamlit smoke checks only where they are stable and lightweight.
- [ ] Keep tests independent from network services and external data.

## 11. Coordinate with Member A

- [ ] Use the public APIs documented in `skills.md`.
- [ ] Confirm function names, parameters, return values, and expected exceptions before changing shared interfaces.
- [ ] Use `crypto.rsa` for RSA operations, `crypto.diffie_hellman` for DH operations, and `crypto.sha256` for hashing.
- [ ] Use `utils.helpers` for conversions and formatting where appropriate.
- [ ] Tell Member A about any interface changes before making them.
- [ ] Do not change Member A's crypto modules or tests without agreement.

## 12. Security and usability review

- [ ] Do not include real passwords, private keys, credentials, or production secrets.
- [ ] Do not describe toy RSA or Diffie-Hellman as secure production cryptography.
- [ ] Add warnings before computational demonstrations that may take time.
- [ ] Keep all attack demonstrations bounded and local.
- [ ] Avoid logging user-provided secrets.
- [ ] Use clear labels, validation messages, and reproducible examples.
- [ ] Confirm the UI remains usable on normal desktop and narrow browser widths.

## 13. Integration checks

- [ ] Run the focused attack and analyzer tests.
- [ ] Run the complete test suite with `python -m pytest -q`.
- [ ] Start the app with `streamlit run app.py`.
- [ ] Open each page and verify the main workflow manually.
- [ ] Verify that invalid inputs produce friendly messages.
- [ ] Verify that all pages can import Member A's public APIs.
- [ ] Review for debug prints, stack traces, accidental secrets, and unbounded loops.

## 14. Handoff

- [ ] Update `skills.md` with every implementation change, its reason, and its use.
- [ ] Summarize public attack and analyzer APIs for Member A.
- [ ] List the test commands and results.
- [ ] Record known limitations of each educational demonstration.
- [ ] Confirm which files were changed.
- [ ] Commit only Member B files unless the team agrees otherwise.

## Suggested implementation order

1. `attacks/hash_attack.py`
2. `attacks/mitm.py`
3. `attacks/rsa_attack.py`
4. `utils/analyzer.py`
5. `app.py`
6. `pages/01_Algorithm_Lab.py`
7. `pages/02_Attack_Lab.py`
8. `pages/03_Security_Analyzer.py`
9. `tests/test_attacks.py`
10. `tests/test_frontend.py`
11. Integration and handoff

## Suggested commands

```bash
python -m pip install -r requirements.txt
python -m pytest tests/test_attacks.py tests/test_frontend.py -q
python -m pytest -q
streamlit run app.py
```
