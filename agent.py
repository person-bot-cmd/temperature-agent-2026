import requests
import json
from datetime import datetime

url = "https://api.open-meteo.com/v1/forecast?latitude=37.5&longitude=-122.0&current_weather=true"

STATE_FILE = "agent_state.json"

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {"history": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def get_temperature():
    response = requests.get(url)
    data = response.json()
    return data["current_weather"]["temperature"]

def main():
    state = load_state()

    current_temp = get_temperature()
    current_time = datetime.utcnow().isoformat()

    print(f"Current temperature: {current_temp}")

    # Create new record
    new_entry = {
        "time": current_time,
        "temperature": current_temp
    }

    # Append to history
    state["history"].append(new_entry)

    print(f"Added new entry: {new_entry}")
    print(f"Total records: {len(state['history'])}")

    save_state(state)

if __name__ == "__main__":
    main()
