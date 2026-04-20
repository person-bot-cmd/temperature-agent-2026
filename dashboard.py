import streamlit as st #For live data presentation
import json
import pandas as pd

st.title("Camping Temperature Dashboard") #Give it a name

with open("agent_state.json", "r") as f:
    data = json.load(f)

df = pd.DataFrame(data["agent_state"])

st.write("Raw data preview")
st.dataframe(df)
