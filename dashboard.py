import json

with open("agent_state.json", "r") as f: #Open history.json to read and call it 'f'
    data = json.load(f) #load 'f' using JSON and call it data

print(data) #print data
