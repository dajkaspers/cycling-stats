import streamlit as st
from src.fit_helpers import plot_combined_metrics

st.title("📈 Ride Graphs")

if "df" in st.session_state:
    df = st.session_state["df"]
    plot_combined_metrics(df)
else:
    st.warning("⚠️ Please upload a .fit file on the home page first.")