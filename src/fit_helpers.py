import pandas as pd
from fitparse import FitFile
import plotly.express as px
from io import BytesIO
import streamlit as st
import plotly.graph_objects as go
import random
from datetime import datetime

@st.cache_data
def parse_fitfile(uploaded_file):
    fitfile = FitFile(BytesIO(uploaded_file.read()))
    records = []

    for record in fitfile.get_messages('record'):
        data = {}
        for record_data in record:
            data[record_data.name] = record_data.value
        records.append(data)

    df = pd.DataFrame(records)

    if 'speed' in df.columns:
        df['speed_kmh'] = (df['speed'] * 3.6).round(1)

    df = df.iloc[::5]
    return df

def plot_metric(df, y_col, title, y_label):
    if y_col not in df.columns:
        return
    fig = px.line(
        df,
        x="timestamp",
        y=y_col,
        title=title,
        labels={y_col: y_label, "timestamp": "Time"},
    )
    fig.update_layout(
        xaxis=dict(showgrid=True, gridwidth=1, zeroline=True),
        yaxis_title=y_label,
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

def plot_combined_metrics(df):
    fig = go.Figure()

    # Speed - first row (primary y-axis)
    if 'speed_kmh' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['speed_kmh'],
            mode='lines',
            name='Speed (km/h)',
            line=dict(color='blue'),
            yaxis='y1'
        ))

    # Cadence - second row (secondary y-axis)
    if 'cadence' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['cadence'],
            mode='lines',
            name='Cadence (rpm)',
            line=dict(color='orange'),
            yaxis='y2'
        ))

    # Power - third row (third y-axis)
    if 'power' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['power'],
            mode='lines',
            name='Power (W)',
            line=dict(color='green'),
            yaxis='y3'
        ))

    # Heart Rate - fourth row (fourth y-axis)
    if 'heart_rate' in df.columns:
        fig.add_trace(go.Scatter(
            x=df['timestamp'],
            y=df['heart_rate'],
            mode='lines',
            name='Heart Rate (bpm)',
            line=dict(color='red'),
            yaxis='y4'
        ))

    # Layout updates to stack the axes vertically
    fig.update_layout(
        title="📊 Combined Cycling Metrics",
        xaxis=dict(title='Time'),
        yaxis1=dict(
            title='Speed (km/h)',
            tickfont=dict(color='blue'),
            domain=[0.75, 1]   # This places it on the top 25% of the space
        ),
        yaxis2=dict(
            title='Cadence (rpm)',
            tickfont=dict(color='orange'),
            domain=[0.5, 0.75]  # This places it on the middle 25% of the space
        ),
        yaxis3=dict(
            title='Power (W)',
            tickfont=dict(color='green'),
            domain=[0.25, 0.5],  # This places it on the lower middle 25% of the space
        ),
        yaxis4=dict(
            title='Heart Rate (bpm)',
            tickfont=dict(color='red'),
            domain=[0, 0.25],  # This places it on the bottom 25% of the space
        ),
        legend=dict(title='Metrics'),
        height=800,  # Adjusted height to give space to each axis
        hovermode='x unified'
    )

    st.plotly_chart(fig, use_container_width=True)


def calculate_normalized_power(df):
    if 'power' not in df.columns or df['power'].isna().all():
        return None  # No power data

    df = df.copy()
    
    # Use a rolling 30s window - assumes 1s sampling rate
    rolling_power = df['power'].rolling(window=30, min_periods=30).mean()
    
    # Raise to the 4th power
    rolling_power_4th = rolling_power ** 4

    # Drop NaNs from rolling calculation
    valid_rolling_power_4th = rolling_power_4th.dropna()

    if len(valid_rolling_power_4th) == 0:
        return None

    # Mean of the 4th powers
    mean_power_4th = valid_rolling_power_4th.mean()

    # 4th root to get NP
    np_power = mean_power_4th ** 0.25
    return round(np_power, 2)

def generate_activity_name(df):
    time_of_day = get_time_of_day()

    # Extract some ride-level stats from df
    distance_km = df['distance_km'].sum() if 'distance_km' in df.columns else None
    elevation_gain_m = df['elevation_gain_m'].sum() if 'elevation_gain_m' in df.columns else None
    avg_speed_kmh = df['speed_kmh'].mean() if 'speed_kmh' in df.columns else None

    moods = [
        "Leg Burner 🔥", "Casual Cruise 🧘‍♂️", "Power Hour ⚡️", "Wind Warrior 🌬️",
        "Climb Crusher 🧗", "Coffee Ride ☕", "Chasing KOMs 🏁", "Just Keep Pedaling 🚴",
        "No Pain No Gain 💪", "Spin & Grin 😁", "Zone 2 Zen 🧘", "Beast Mode Engaged 🦁"
    ]

    templates = [
        f"{time_of_day} {random.choice(moods)}",
        f"{random.choice(['Epic', 'Chill', 'Solid', 'Quick'])} {time_of_day} Ride 🚴",
        f"{random.choice(['Into the Wind', 'Over the Hills', 'Through the City'])} We Go 🌍",
        f"{random.choice(['Sweat', 'Suffer', 'Spin'])} Session - {time_of_day} Edition",
        f"{random.choice(['Rolling', 'Rippin’', 'Grinding'])} {random.choice(['with Friends', 'Solo'])} 🎧"
    ]

    if distance_km and distance_km > 80:
        templates.append("Century Vibes 🎯")
    if elevation_gain_m and elevation_gain_m > 1000:
        templates.append("King of the Mountain Day 👑")
    if avg_speed_kmh and avg_speed_kmh > 32:
        templates.append("Speed Demon Mode 🚀")

    return random.choice(templates)

def get_time_of_day():
    hour = datetime.now().hour
    if hour < 12:
        return "Morning"
    elif hour < 17:
        return "Afternoon"
    else:
        return "Evening"
