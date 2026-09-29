import streamlit as st

from utils.analyzer import analyze_secret, summarize_findings

st.set_page_config(page_title="Security Analyzer", page_icon="📊", layout="wide")
st.title("📊 Security Analyzer")
st.caption("Heuristic educational analysis. Your input is analyzed in memory and is not displayed after analysis.")

secret = st.text_input(
    "Enter a demo password or text",
    type="password",
    help="Do not enter a real password or production secret.",
)

if st.button("Analyze"):
    try:
        findings = analyze_secret(secret)
        summary = summarize_findings(findings)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Overall", summary["overall"])
        c2.metric("High", summary["counts"]["HIGH"])
        c3.metric("Medium", summary["counts"]["MEDIUM"])
        c4.metric("Low", summary["counts"]["LOW"])

        for severity in ["HIGH", "MEDIUM", "LOW"]:
            matching = [f for f in findings if f["severity"] == severity]
            if matching:
                st.subheader(f"{severity} findings")
                for finding in matching:
                    with st.container(border=True):
                        st.markdown(f"**{finding['issue']}**")
                        st.write(finding["explanation"])
                        st.caption("Recommendation: " + finding["recommendation"])

        st.info(
            "This is a heuristic educational analyzer. It does not prove that a "
            "password or text is secure or insecure."
        )
    except Exception as exc:
        st.error(f"Unable to analyze input: {exc}")
