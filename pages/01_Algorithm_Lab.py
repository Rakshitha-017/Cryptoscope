import streamlit as st

from crypto.rsa import generate_keypair, encrypt, decrypt
from crypto.diffie_hellman import (
    DHParameters,
    calculate_public_key,
    calculate_shared_secret,
)
from crypto.sha256 import hash_text

st.set_page_config(page_title="Algorithm Lab", page_icon="🔐", layout="wide")
st.title("🔐 Algorithm Lab")
st.caption("Toy parameters only — for education, not production cryptography.")

tab1, tab2, tab3 = st.tabs(["RSA", "Diffie-Hellman", "SHA-256"])

with tab1:
    st.header("RSA")
    st.write("Generate a small educational RSA keypair and observe encryption/decryption.")

    c1, c2 = st.columns(2)
    with c1:
        p = st.number_input("Prime p", min_value=3, value=61, step=1)
        q = st.number_input("Prime q", min_value=3, value=53, step=1)
        e = st.number_input("Public exponent e", min_value=3, value=17, step=1)
    with c2:
        message = st.number_input("Integer message", min_value=0, value=65, step=1)

    if st.button("Run RSA", key="rsa_run"):
        try:
            pair = generate_keypair(p=p, q=q, e=e)
            ciphertext = encrypt(message, pair.public)
            plaintext = decrypt(ciphertext, pair.private)
            st.success("RSA round trip completed.")
            a, b, c = st.columns(3)
            a.metric("Public key", f"({pair.public.exponent}, {pair.public.modulus})")
            b.metric("Ciphertext", str(ciphertext))
            c.metric("Recovered", str(plaintext))
            with st.expander("Educational intermediate values"):
                st.json(pair.intermediate_values if hasattr(pair, "intermediate_values") else {})
        except Exception as exc:
            st.error(f"Invalid RSA input: {exc}")

with tab2:
    st.header("Diffie-Hellman")
    prime = st.number_input("Prime p", min_value=5, value=23, step=1, key="dh_p")
    generator = st.number_input("Generator g", min_value=2, value=5, step=1, key="dh_g")
    alice = st.number_input("Alice private key", min_value=1, value=6, step=1)
    bob = st.number_input("Bob private key", min_value=1, value=15, step=1)

    if st.button("Run DH Exchange", key="dh_run"):
        try:
            params = DHParameters(prime=prime, generator=generator)
            alice_public = calculate_public_key(alice, params.generator, params.prime)
            bob_public = calculate_public_key(bob, params.generator, params.prime)
            alice_secret = calculate_shared_secret(alice, bob_public, params.prime)
            bob_secret = calculate_shared_secret(bob, alice_public, params.prime)

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Alice public", alice_public)
            c2.metric("Bob public", bob_public)
            c3.metric("Alice secret", alice_secret)
            c4.metric("Bob secret", bob_secret)
            st.success("Shared secret matches." if alice_secret == bob_secret else "Secret mismatch.")
        except Exception as exc:
            st.error(f"Invalid DH input: {exc}")

with tab3:
    st.header("SHA-256")
    text = st.text_area("Text to hash", value="Hello Cryptoscope")
    if st.button("Generate SHA-256", key="sha_run"):
        digest = hash_text(text)
        st.code(digest)
        st.caption("SHA-256 is a one-way hash function, not encryption.")
