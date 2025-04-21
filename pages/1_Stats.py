import streamlit as st
from src.stats_helpers import display_stats
from src.fit_helpers import generate_activity_name

st.title("📊 Ride Statistics")

if "df" in st.session_state:
    df = st.session_state["df"]
    st.subheader(f"Suggested Ride Name: {st.session_state.get('activity_name', 'Activity')}")
    if st.button("Generate New Activity Name"):
        # Generate new activity name using the provided logic in your helper function
        new_activity_name = generate_activity_name(df)

        # Save the new activity name to session_state
        st.session_state["activity_name"] = new_activity_name

        # Display the updated activity name
        st.success(f"New Activity Name: {new_activity_name}")

    display_stats(df)
else:
    st.warning("⚠️ Please upload a .fit file on the home page first.")