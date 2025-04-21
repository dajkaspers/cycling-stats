import streamlit as st
import numpy as np
from src.fit_helpers import calculate_normalized_power

def display_stats(df):
    st.subheader("📋 Ride Summary")

    col1, col2, col3 = st.columns(3)

    with col1:
        # Calculate the duration by subtracting the first timestamp from the last timestamp
        duration = df['timestamp'].max() - df['timestamp'].min()

        # Convert duration to a readable format (e.g., hours:minutes:seconds)
        duration_in_seconds = duration.total_seconds()  # Convert to seconds

        # Display the duration in a user-friendly format
        hours = int(duration_in_seconds // 3600)  # Get the number of full hours
        minutes = int((duration_in_seconds % 3600) // 60)  # Get the remaining minutes
        seconds = int(duration_in_seconds % 60)  # Get the remaining seconds

        # Show the duration as a metric in the format hours:minutes:seconds
        st.metric("Duration", f"{hours:02}:{minutes:02}:{seconds:02}")
        st.metric("Avg Speed", f"{df['speed_kmh'].mean():.1f} km/h")
        st.metric("Max Speed", f"{df['speed_kmh'].max():.1f} km/h")

    with col2:
        if 'heart_rate' in df.columns:
            st.metric("Avg HR", f"{df['heart_rate'].mean():.0f} bpm")
            st.metric("Max HR", f"{df['heart_rate'].max():.0f} bpm")
        if 'power' in df.columns:
            st.metric("Avg Power", f"{df['power'].mean():.0f} W")

    with col3:
        if 'cadence' in df.columns:
            st.metric("Avg Cadence", f"{df['cadence'].mean():.0f} rpm")
        if 'power' in df.columns:
            st.metric("Max Power", f"{df['power'].max():.0f} W")
        np_value = calculate_normalized_power(df)
        if np_value:
            st.metric("⚡ Normalized Power", f"{np_value} W")
        else:
            st.warning("No valid power data for calculating Normalized Power.")
