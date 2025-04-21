import streamlit as st
import pandas as pd
from src.fit_helpers import parse_fitfile, generate_activity_name

st.set_page_config(
    page_title="FIT File Reader",  # Title in the browser tab
    page_icon="🚴",                # Icon in the browser tab (optional)
    layout="wide",                 # Layout of the page
    initial_sidebar_state="expanded"  # Optional, to start with the sidebar expanded
)

st.title("🚴 FIT File Reader")

uploaded_file = st.file_uploader("Upload your .fit file", type=["fit"])

if uploaded_file is not None:
    df = parse_fitfile(uploaded_file)

    # Check on required columns
    required_columns = ['speed_kmh', 'cadence', 'power', 'heart_rate']

    for col in required_columns:
        if col not in df.columns:
            st.error("❌ Missing data. This looks like incomplete training data — please check your file and try again.")
            st.stop()

    # Save it to session_state
    st.session_state["df"] = df
    st.session_state["activity_name"] = generate_activity_name(df)

    st.success("✅ FIT file loaded successfully! Head over to the pages on the left to explore your ride.")
else:
    st.info("👆 Upload a .fit file to get started.")