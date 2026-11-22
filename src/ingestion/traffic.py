import os
import csv
import requests
from dotenv import load_dotenv
from datetime import datetime, timezone

# Load environment variables
load_dotenv()

API_KEY = os.getenv("TOMTOM_API_KEY")

if not API_KEY:
    raise ValueError("TomTom API key not found")


def get_traffic_data(city, latitude, longitude):
    """
    Collect traffic data from TomTom API for a GPS location.
    """

    url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/json"

    params = {
        "key": API_KEY,
        "point": f"{latitude},{longitude}"
    }

    response = requests.get(url, params=params, timeout=30)
    print("HTTP Status:", response.status_code)
    response.raise_for_status()

    data = response.json()

    flow = data.get("flowSegmentData")

    if not flow:
        raise ValueError("Traffic data not found in API response")

    traffic_info = {
        "city": city,
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "current_speed": flow["currentSpeed"],
        "free_flow_speed": flow["freeFlowSpeed"],
        "current_travel_time": flow["currentTravelTime"],
        "free_flow_travel_time": flow["freeFlowTravelTime"],
        "confidence": flow["confidence"],
        "road_closure": flow["roadClosure"]
    }

    return traffic_info


if __name__ == "__main__":

    cities = [
        {"city": "Tangier", "latitude": 35.7595, "longitude": -5.8340},
        {"city": "Rabat", "latitude": 34.0209, "longitude": -6.8416},
        {"city": "Casablanca", "latitude": 33.5731, "longitude": -7.5898}
    ]

    traffic_data = []

    for city in cities:
        try:
            traffic = get_traffic_data(
                city["city"],
                city["latitude"],
                city["longitude"]
            )

            traffic_data.append(traffic)

        except requests.exceptions.RequestException as error:
            print(f"Error collecting data for {city['city']}: {error}")

    output_file = "data/raw/traffic_data.csv"

    file_exists = os.path.exists(output_file)

    if traffic_data:
        with open(output_file, mode="a", newline="", encoding="utf-8") as file:

            fieldnames = traffic_data[0].keys()

            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()

            writer.writerows(traffic_data)

        print(f"{len(traffic_data)} traffic records saved successfully.")
    else:
        print("No traffic data collected.")