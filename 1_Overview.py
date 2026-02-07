import streamlit as st

st.header("📊 Overview")

df = st.session_state.get("current_df")

if df is None:
    st.warning("Upload a file to see overview")
    st.stop()

st.metric("Total Transactions", len(df))
st.metric("Total Amount", f"₹ {df['amount'].sum():,.0f}")
st.dataframe(df)
