import streamlit as st #For live data presentation
import json
import pandas as pd

st.title("Camping Temperature Dashboard") #Give it a name

with open("agent_state.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data["agent_state"])

# Convert time column to datetime
df["time"] = pd.to_datetime(df["time"])

# Find latest timestamp
latest_time = df["time"].max()

# Filter last 24 hours
last_24h = df[df["time"] >= latest_time - pd.Timedelta(hours=24)]

st.write("Last 24 hours of data")
st.dataframe(last_24h)

st.write("Raw data preview")
st.dataframe(df)
