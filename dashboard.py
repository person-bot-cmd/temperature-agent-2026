import streamlit as st #For live data presentation
import json
import pandas as pd

st.title("Camping Temperature Dashboard") #Give it a name

with open("agent_state.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data["history"])
df["temperature_F"] = df["temperature"] * 9/5 + 32

# Convert time column to datetime
df["time"] = pd.to_datetime(df["time"])

# Find latest timestamp
latest_time = df["time"].max()

# Filter last 24 hours
last_24h = df[df["time"] >= latest_time - pd.Timedelta(hours=24)]
last_week = df[df["time"] >= latest_time - pd.Timedelta(days=7)]

st.subheader("Temperature Over the Last 24 Hours")
st.line_chart(last_24h.set_index("time")["temperature_F"])

st.subheader("Temperature Over the Last 7 Days")
st.line_chart(last_week.set_index("time")["temperature_F"])


# Find peak and lowest temperatures
max_temp = last_24h["temperature"].max()
min_temp = last_24h["temperature"].min()

# Find when they happened
max_row = last_24h[last_24h["temperature"] == max_temp]
min_row = last_24h[last_24h["temperature"] == min_temp]

st.subheader("Key Insights (Last 24 Hours)")

st.write(f"Highest temperature: {max_temp}")
st.write(f"Occurred at: {max_row['time'].values[0]}")

st.write(f"Lowest temperature: {min_temp}")
st.write(f"Occurred at: {min_row['time'].values[0]}")

st.write("Last 24 hours of data")
st.dataframe(last_24h)

st.write("Raw data preview")
st.dataframe(df)
