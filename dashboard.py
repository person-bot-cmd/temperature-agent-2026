import streamlit as st #For live data presentation
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def make_temp_chart(data, title):
    # Find highest and lowest points
    max_row = data.loc[data["temperature_F"].idxmax()]
    min_row = data.loc[data["temperature_F"].idxmin()]

    fig = go.Figure()

    # Main temperature line
    fig.add_trace(go.Scatter(
        x=data["time"],
        y=data["temperature_F"],
        mode="lines",
        name="Temperature",
        hovertemplate="Time: %{x}<br>Temp: %{y:.1f}°F<extra></extra>"
    ))

    # Highest point
    fig.add_trace(go.Scatter(
        x=[max_row["time"]],
        y=[max_row["temperature_F"]],
        mode="markers+text",
        name="Highest",
        text=[f'High: {max_row["temperature_F"]:.1f}°F'],
        textposition="top center",
        marker=dict(size=12, color = "red", symbol="circle")
    ))

    # Lowest point
    fig.add_trace(go.Scatter(
        x=[min_row["time"]],
        y=[min_row["temperature_F"]],
        mode="markers+text",
        name="Lowest",
        text=[f'Low: {min_row["temperature_F"]:.1f}°F'],
        textposition="bottom center",
        marker=dict(size=12, color = "blue", symbol="circle")
    ))

    fig.update_layout(
    title=title,
    xaxis_title="Time",
    yaxis_title="Temperature (°F)",
    hovermode="x unified",
    template="plotly_dark",
    height=500,
    margin=dict(l=40, r=40, t=70, b=40),
    showlegend=True
)

    fig.update_xaxes(
        tickformat="%b %d\n%I:%M %p"
    )

    return fig

st.title("Camping Temperature Dashboard") #Give it a name

with open("agent_state.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data["history"])
df["temperature_F"] = df["temperature"] * 9/5 + 32

# Convert time column to datetime
df["time"] = pd.to_datetime(df["time"])
df["time"] = df["time"].dt.tz_localize("UTC").dt.tz_convert("America/Los_Angeles")

# Find latest timestamp
latest_time = df["time"].max()

# Filter last 24 hours
last_24h = df[df["time"] >= latest_time - pd.Timedelta(hours=24)]
last_week = df[df["time"] >= latest_time - pd.Timedelta(days=7)]

st.subheader("Last 24 Hours")
daily_fig = make_temp_chart(last_24h, "Daily Temperature Trend")
st.plotly_chart(daily_fig, use_container_width=True)

st.subheader("Last 7 Days")
weekly_fig = make_temp_chart(last_week, "Weekly Temperature Trend")
st.plotly_chart(weekly_fig, use_container_width=True)


# Find peak and lowest temperatures
max_temp = last_24h["temperature"].max()
min_temp = last_24h["temperature"].min()

# Find when they happened
max_row = last_24h[last_24h["temperature"] == max_temp]
min_row = last_24h[last_24h["temperature"] == min_temp]


