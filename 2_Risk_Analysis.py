import streamlit as st

st.header("⚠️ Risk Analysis")

df = st.session_state.get("current_df")

if df is None:
    st.warning("Upload a file to see risk analysis")
    st.stop()

st.bar_chart(df["risk_level"].value_counts())
