import csv
from datetime import datetime

def check_missing_values(row):
    missing_fields = []

    for field, value in row.items():
        if not value or not value.strip():
            missing_fields.append(field)

    return missing_fields

test_row = {
    "city": "Tangier",
    "current_speed": "",
    "confidence": "0.99"
}

result = check_missing_values(test_row)

print("Missing fields:", result)

def check_negative_speeds(row):
    invalid_fields = []

    current_speed = float(row["current_speed"])
    free_flow_speed = float(row["free_flow_speed"])

    if current_speed < 0:
        invalid_fields.append("current_speed")

    if free_flow_speed < 0:
        invalid_fields.append("free_flow_speed")

    return invalid_fields

speed_test_row = {
    "current_speed": "-5",
    "free_flow_speed": "28"
}

result = check_negative_speeds(speed_test_row)

print("Invalid speed fields:", result)

def check_confidence(row):
    invalid_fields = []

    confidence = float(row["confidence"])

    if confidence < 0 or confidence > 1:
        invalid_fields.append("confidence")

    return invalid_fields

confidence_test_row = {
    "confidence": "1.5"
}

result = check_confidence(confidence_test_row)

print("Invalid confidence fields:", result)

def check_negative_travel_times(row):
    invalid_fields = []

    current_time = float(row["current_travel_time"])
    free_flow_time = float(row["free_flow_travel_time"])

    if current_time < 0:
        invalid_fields.append("current_travel_time")

    if free_flow_time < 0:
        invalid_fields.append("free_flow_travel_time")

    return invalid_fields

travel_test_row = {
    "current_travel_time": "-10",
    "free_flow_travel_time": "123"
}

result = check_negative_travel_times(travel_test_row)

print("Invalid travel time fields:", result)

def check_invalid_date(row):
    invalid_fields = []

    try:
        datetime.fromisoformat(row["collected_at"])
    except ValueError:
        invalid_fields.append("collected_at")
 
    return invalid_fields

date_test_row = {
    "collected_at": "2026-11-21T12:22:56.769364+00:00"
}

result = check_invalid_date(date_test_row)

print("Invalid date fields:", result)

date_test_row = {
    "collected_at": "2026-15-45"
}

result = check_invalid_date(date_test_row)

print("Invalid date fields:", result)