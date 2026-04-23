import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

def make_temp_chart(data, title):
    max_row = data.loc[data["temperature_F"].idxmax()]
    min_row = data.loc[data["temperature_F"].idxmin()]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=data["time"],
        y=data["temperature_F"],
        mode="lines",
        name="Temperature",
        line=dict(color="lightgray"),
        hovertemplate="Time: %{x}<br>Temp: %{y:.1f}°F<extra></extra>"
    ))

    fig.add_trace(go.Scatter(
        x=[max_row["time"]],
        y=[max_row["temperature_F"]],
        mode="markers+text",
        name="Highest",
        text=[f'High: {max_row["temperature_F"]:.1f}°F'],
        textposition="top center",
        marker=dict(size=12, color="red", symbol="circle")
    ))

    fig.add_trace(go.Scatter(
        x=[min_row["time"]],
        y=[min_row["temperature_F"]],
        mode="markers+text",
        name="Lowest",
        text=[f'Low: {min_row["temperature_F"]:.1f}°F'],
        textposition="bottom center",
        marker=dict(size=12, color="blue", symbol="circle")
    ))

    fig.update_layout(
        title=title,
        xaxis_title="Time",
        yaxis_title="Temperature (°F)",
        hovermode="x unified",
        template="plotly_white",
        height=500,
        margin=dict(l=40, r=40, t=70, b=40),
        showlegend=True
    )

    fig.update_xaxes(
        tickformat="%b %d\n%I:%M %p"
    )

    return fig

st.markdown("""
<style>
.stApp {
    background-color: #0e1117;
    color: white;
}
[data-testid="stDataFrame"] {
    border: 1px solid #444;
    border-radius: 10px;
    padding: 6px;
}
</style>
""", unsafe_allow_html=True)

st.title("Camping Temperature Dashboard")

with open("agent_state.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data["history"])

df["temperature_F"] = df["temperature"] * 9/5 + 32
df["time"] = pd.to_datetime(df["time"])
df["time"] = df["time"].dt.tz_localize("UTC").dt.tz_convert("America/Los_Angeles")

latest_time = df["time"].max()
last_24h = df[df["time"] >= latest_time - pd.Timedelta(hours=24)]
last_week = df[df["time"] >= latest_time - pd.Timedelta(days=7)]

weekly_fig = make_temp_chart(last_week, "Last 7 Days")
daily_fig = make_temp_chart(last_24h, "Last 24 hours")


col2, col1 = st.columns(2)

with col1:
    st.plotly_chart(daily_fig, use_container_width=True)

with col2:
    st.plotly_chart(weekly_fig, use_container_width=True)

st.subheader("Last 24 Hours Data")
st.dataframe(last_24h, use_container_width=True)


