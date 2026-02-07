import streamlit as st

st.header("👥 Customer Analysis")

df = st.session_state.get("current_df")

if df is None:
    st.warning("Upload a file to see customer analysis")
    st.stop()

st.bar_chart(df.groupby("customer_id")["amount"].sum())
