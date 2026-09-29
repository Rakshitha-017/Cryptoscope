import hashlib
import streamlit as st

from attacks.hash_attack import dictionary_attack, brute_force_attack
from attacks.mitm import simulate_mitm
from attacks.rsa_attack import demonstrate_factorization

st.set_page_config(page_title="Attack Lab", page_icon="⚔️", layout="wide")
st.title("⚔️ Attack Lab")
st.warning("Educational demonstrations only. Values are deliberately toy-sized and bounded.")

tab1, tab2, tab3 = st.tabs(["Hash Attack", "DH MITM", "RSA Weakness"])

with tab1:
    st.header("SHA-256 Dictionary / Brute-Force Demonstration")
    mode = st.radio("Mode", ["Dictionary", "Brute-force"], horizontal=True)

    if mode == "Dictionary":
        secret = st.text_input("Demo secret", value="admin123", type="password")
        target = hashlib.sha256(secret.encode()).hexdigest()
        candidates_text = st.text_area(
            "Candidate list (one per line)",
            value="password\n123456\nadmin\nadmin123\nwelcome",
        )
        if st.button("Run hash attack"):
            candidates = [x for x in candidates_text.splitlines() if x]
            result = dictionary_attack(target, candidates)
            st.code(f"Target SHA-256: {target}")
            if result["found"]:
                st.success(f"Match found after {result['attempts']} attempts.")
                st.code(result["recovered"])
            else:
                st.info(f"No match in the bounded list. Attempts: {result['attempts']}")
    else:
        secret = st.text_input("Tiny demo secret (lowercase)", value="cat", type="password")
        target = hashlib.sha256(secret.encode()).hexdigest()
        alphabet = st.text_input("Alphabet", value="abcdefghijklmnopqrstuvwxyz")
        max_len = st.slider("Maximum length", 1, 4, 3)
        if st.button("Run brute-force attack"):
            try:
                result = brute_force_attack(target, alphabet, max_len)
                if result["found"]:
                    st.success(f"Recovered after {result['attempts']} attempts.")
                    st.code(result["recovered"])
                else:
                    st.info(f"Not found within the bound. Attempts: {result['attempts']}")
            except Exception as exc:
                st.error(str(exc))

with tab2:
    st.header("Diffie-Hellman Man-in-the-Middle")
    st.write("The attacker replaces unauthenticated public values, creating two separate secrets.")
    p = st.number_input("Prime", min_value=5, value=23, step=1, key="mitm_p")
    g = st.number_input("Generator", min_value=2, value=5, step=1, key="mitm_g")
    a = st.number_input("Alice private", min_value=1, value=6, step=1, key="mitm_a")
    b = st.number_input("Bob private", min_value=1, value=15, step=1, key="mitm_b")

    if st.button("Simulate MITM"):
        try:
            result = simulate_mitm(p, g, a, b)
            c1, c2, c3 = st.columns(3)
            c1.metric("Alice's received public", result["alice"]["received_public"])
            c2.metric("Attacker→Alice secret", result["attacker"]["secret_with_alice"])
            c3.metric("Attacker→Bob secret", result["attacker"]["secret_with_bob"])

            st.error(
                "MITM successful: Alice and Bob are not directly sharing the same secret."
                if result["mitm_success"] else
                "MITM condition was not demonstrated."
            )
            with st.expander("Intermediate values"):
                st.json(result)
            st.info("Mitigation: authenticate public-key exchanges, for example with signatures or certificates.")
        except Exception as exc:
            st.error(f"Invalid DH input: {exc}")

with tab3:
    st.header("RSA Weak-Modulus Demonstration")
    st.write("A deliberately tiny RSA modulus can be factored, revealing the private exponent.")
    n = st.number_input("RSA modulus n", min_value=15, value=3233, step=1)
    e = st.number_input("Public exponent e", min_value=3, value=17, step=1)
    ciphertext = st.number_input("Ciphertext", min_value=0, value=2790, step=1)

    if st.button("Run RSA weakness demo"):
        try:
            result = demonstrate_factorization(n, e, ciphertext)
            if result["success"]:
                st.success(f"Toy modulus factored: p={result['factors'][0]}, q={result['factors'][1]}")
                st.metric("Recovered private exponent", result["recovered_private_exponent"])
                st.metric("Recovered message", result["message"])
            else:
                st.info(result["lesson"])
            st.write("**Mitigation:**", result["mitigation"])
        except Exception as exc:
            st.error(f"Invalid RSA input: {exc}")
