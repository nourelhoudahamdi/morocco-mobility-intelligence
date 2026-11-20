import requests
import csv
import os


def get_weather():

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": 35.7595,
        "longitude": -5.8340,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

    except requests.exceptions.RequestException as error:
        print("Weather API error:", error)
        return None

    current_weather = data["current"]

    weather_data = {
        "measurement_time": current_weather["time"],
        "temperature": current_weather["temperature_2m"],
        "humidity": current_weather["relative_humidity_2m"],
        "wind_speed": current_weather["wind_speed_10m"]
    }

    return weather_data


def save_weather_data(weather_data):

    file_path = "data/raw/weather.csv"

    file_exists = os.path.exists(file_path)

    try:
        with open(file_path, mode="a", newline="", encoding="utf-8") as file:

            writer = csv.DictWriter(file, fieldnames=weather_data.keys())

            if not file_exists:
                writer.writeheader()

            writer.writerow(weather_data)

        print("Weather data saved successfully!")
        return True

    except OSError as error:
        print("CSV saving error:", error)
        return False


weather_data = get_weather()

if weather_data is not None:

    print("Weather data collected successfully!")
    print(weather_data)

    save_weather_data(weather_data)

else:
    print("Weather data collection failed.")