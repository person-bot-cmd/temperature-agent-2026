import requests

# API endpoint
url = "https://api.open-meteo.com/v1/forecast?latitude=37.5&longitude=-122.0&current_weather=true"

def get_temperature():
    response = requests.get(url)
    data = response.json()
    
    # Extract temperature
    temperature = data["current_weather"]["temperature"]
    
    return temperature

def main():
    temp = get_temperature()
    print(f"Current temperature: {temp}°C")

if __name__ == "__main__":
    main()
