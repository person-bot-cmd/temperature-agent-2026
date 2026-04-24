import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(layout="wide")

def make_temp_chart(data, title, y_range=None):
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
    title={
        "text": title,
        "x": 0.5,
        "xanchor": "center",
         "font": {"size": 30}
    },
        yaxis=dict(
    title="Temperature (°F)",
    range=y_range
),
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

#st.title("Camping Temperature Dashboard")
st.markdown(
    "<h1 style='text-align: center; margin-bottom: 30px;'>Camping Temperature Dashboard</h1>",
    unsafe_allow_html=True
)

with open("agent_state.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data["history"])

df["temperature_F"] = df["temperature"] * 9/5 + 32
df["time"] = pd.to_datetime(df["time"])
df["time"] = df["time"].dt.tz_localize("UTC").dt.tz_convert("America/Los_Angeles")

display_df = df[["time", "temperature_F"]].copy()

display_df["Time"] = display_df["time"].dt.strftime("%b %d, %I:%M %p")
display_df["Temp (°F)"] = display_df["temperature_F"].round(1)

display_df = display_df[["Time", "Temp (°F)"]]


latest_time = df["time"].max()
last_24h = df[df["time"] >= latest_time - pd.Timedelta(hours=24)]
last_week = df[df["time"] >= latest_time - pd.Timedelta(days=7)]

y_min = last_week["temperature_F"].min()
y_max = last_week["temperature_F"].max()

padding = 2

shared_y_range = [y_min - padding, y_max + padding]

daily_fig = make_temp_chart(last_24h, "Daily Temperature Trend", shared_y_range)
weekly_fig = make_temp_chart(last_week, "Weekly Temperature Trend", shared_y_range)


col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(weekly_fig, use_container_width=True)

with col2:
    st.plotly_chart(daily_fig, use_container_width=True)

html_table = "<table style='width:100%; text-align:center; border-collapse: collapse;'>"
html_table += "<tr><th style='border-bottom: 1px solid white;'>Time</th><th style='border-bottom: 1px solid white;'>Temp (°F)</th></tr>"

for _, row in display_df.iterrows():
    html_table += f"<tr><td>{row['Time']}</td><td>{row['Temp (°F)']}</td></tr>"

html_table += "</table>"

st.markdown("### Last 24 Hours (Readable Table)")
st.markdown(html_table, unsafe_allow_html=True)


