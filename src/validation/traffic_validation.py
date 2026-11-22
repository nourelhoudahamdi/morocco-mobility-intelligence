import csv
from datetime import datetime
from pathlib import Path


# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# CSV file path
CSV_FILE = PROJECT_ROOT / "data" / "raw" / "traffic_data.csv"


# 1. Check missing values
def check_missing_values(row):
    missing_fields = []

    for field, value in row.items():
        if value is None or not str(value).strip():
            missing_fields.append(field)

    return missing_fields


# 2. Check negative or invalid speeds
def check_negative_speeds(row):
    invalid_fields = []

    try:
        current_speed = float(row["current_speed"])
        free_flow_speed = float(row["free_flow_speed"])

        if current_speed < 0:
            invalid_fields.append("current_speed")

        if free_flow_speed < 0:
            invalid_fields.append("free_flow_speed")

    except (ValueError, TypeError, KeyError):
        invalid_fields.append("speed_values")

    return invalid_fields


# 3. Check confidence
def check_confidence(row):
    invalid_fields = []

    try:
        confidence = float(row["confidence"])

        if confidence < 0 or confidence > 1:
            invalid_fields.append("confidence")

    except (ValueError, TypeError, KeyError):
        invalid_fields.append("confidence")

    return invalid_fields


# 4. Check negative or invalid travel times
def check_negative_travel_times(row):
    invalid_fields = []

    try:
        current_time = float(row["current_travel_time"])
        free_flow_time = float(row["free_flow_travel_time"])

        if current_time < 0:
            invalid_fields.append("current_travel_time")

        if free_flow_time < 0:
            invalid_fields.append("free_flow_travel_time")

    except (ValueError, TypeError, KeyError):
        invalid_fields.append("travel_time_values")

    return invalid_fields


# 5. Check dates
def check_invalid_date(row):
    invalid_fields = []

    try:
        datetime.fromisoformat(row["collected_at"])

    except (ValueError, TypeError, KeyError):
        invalid_fields.append("collected_at")

    return invalid_fields


# 6. Validate the CSV file
def validate_traffic_csv():

    total_rows = 0

    rows_with_missing_values = 0
    rows_with_invalid_speeds = 0
    rows_with_invalid_confidence = 0
    rows_with_invalid_travel_times = 0
    rows_with_invalid_dates = 0

    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        for row in reader:

            total_rows += 1

            # Check missing values
            if check_missing_values(row):
                rows_with_missing_values += 1

            # Check speeds
            if check_negative_speeds(row):
                rows_with_invalid_speeds += 1

            # Check confidence
            if check_confidence(row):
                rows_with_invalid_confidence += 1

            # Check travel times
            if check_negative_travel_times(row):
                rows_with_invalid_travel_times += 1

            # Check dates
            if check_invalid_date(row):
                rows_with_invalid_dates += 1

    # Build validation report
    report = {
        "total_rows": total_rows,
        "missing_values": rows_with_missing_values,
        "invalid_speeds": rows_with_invalid_speeds,
        "invalid_confidence": rows_with_invalid_confidence,
        "invalid_travel_times": rows_with_invalid_travel_times,
        "invalid_dates": rows_with_invalid_dates
    }

    # Determine validation status
    report["status"] = (
        "PASSED"
        if all(value == 0 for key, value in report.items()
               if key != "total_rows")
        else "FAILED"
    )

    return report


# 7. Display validation report
def display_validation_report(report):

    print("\n========== VALIDATION SUMMARY ==========")

    print("Total rows checked:", report["total_rows"])

    print("Rows with missing values:", report["missing_values"])
    print("Rows with invalid speeds:", report["invalid_speeds"])
    print("Rows with invalid confidence:", report["invalid_confidence"])
    print("Rows with invalid travel times:", report["invalid_travel_times"])
    print("Rows with invalid dates:", report["invalid_dates"])

    print("\nValidation status:", report["status"])


# 8. Execute validation only when running this file directly
if __name__ == "__main__":

    validation_report = validate_traffic_csv()

    display_validation_report(validation_report)