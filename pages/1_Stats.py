import streamlit as st
from src.stats_helpers import display_stats

st.title("📊 Ride Statistics")

if "df" in st.session_state:
    df = st.session_state["df"]
    st.subheader(st.session_state.get("activity_name", "Activity"))
    display_stats(df)
else:
    st.warning("⚠️ Please upload a .fit file on the home page first.")