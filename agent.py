import requests
import json
from datetime import datetime

# API endpoint
url = "https://api.open-meteo.com/v1/forecast?latitude=37.5&longitude=-122.0&current_weather=true"

STATE_FILE = "agent_state.json"

def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except:
        return {
            "previous_temperature": None,
            "max_temperature": None,
            "last_checked": None
        }

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
    previous_temp = state["previous_temperature"]
    max_temp = state["max_temperature"]

    print(f"Current temperature: {current_temp}")
    print(f"Previous temperature: {previous_temp}")
    print(f"Max temperature: {max_temp}")

    # Compare
    if previous_temp is not None:
        change = current_temp - previous_temp
        print(f"Change since last check: {change}")

    if max_temp is None or current_temp > max_temp:
        print("New maximum temperature!")
        state["max_temperature"] = current_temp

    # Update memory
    state["previous_temperature"] = current_temp
    state["last_checked"] = datetime.utcnow().isoformat()

    save_state(state)

if __name__ == "__main__":
    main()
