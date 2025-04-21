import streamlit as st
import pandas as pd
from fit_helpers import parse_fitfile, plot_combined_metrics
from stats_helpers import display_stats

st.set_page_config(page_title="FIT File Reader", layout="wide")
st.title("🚴 FIT File Reader with Graphs")

uploaded_file = st.file_uploader("Upload your .fit file", type=["fit"])

if uploaded_file is not None:
    df = parse_fitfile(uploaded_file)

    # 🧼 Clean + Prep
    if 'speed_kmh' in df.columns:
        df = df[df['speed_kmh'] > 0]
    df.reset_index(drop=True, inplace=True)

    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')
        df['timestamp'] = df['timestamp'] - df['timestamp'].min()

    # ✅ Show Data
    st.success("File loaded! Here's your ride data:")
    st.dataframe(df[["timestamp", "speed_kmh", "heart_rate", "power", "cadence"]].dropna(how="all"))

    # 📋 Summary
    display_stats(df)

    # 📈 Plots
    plot_combined_metrics(df)

else:
    st.info("👆 Upload a .fit file to get started.")
