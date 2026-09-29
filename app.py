import streamlit as st

st.set_page_config(
    page_title="Cryptoscope",
    page_icon="🔐",
    layout="wide",
)

st.title("CRYPTOSCOPE")
st.subheader("Cryptographic Security & Attack Analysis Platform")

st.markdown(
    """
Cryptoscope is an **educational cryptography laboratory** where you can
experiment with RSA, Diffie-Hellman and SHA-256, then observe controlled
demonstrations of common weaknesses and attacks.

### Modules

- 🔐 **Algorithm Lab** — experiment with RSA, Diffie-Hellman and SHA-256.
- ⚔️ **Attack Lab** — bounded hash, RSA weakness and DH MITM demonstrations.
- 📊 **Security Analyzer** — heuristic analysis of password/text patterns.

> **Important:** Cryptoscope uses deliberately small/toy cryptographic
> parameters for learning. It is not a production security tool.
> Attack demonstrations are bounded and intended only for authorized,
> educational use.
"""
)

st.info("Use the pages in the sidebar to begin.")
