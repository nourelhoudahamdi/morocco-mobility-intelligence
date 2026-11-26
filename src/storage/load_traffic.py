import csv
from pathlib import Path

from src.storage.database import get_connection

from src.validation.traffic_validation import (
    check_missing_values,
    check_negative_speeds,
    check_confidence,
    check_negative_travel_times,
    check_invalid_date
)


# 1. Project configuration

PROJECT_ROOT = Path(__file__).resolve().parents[2]

CSV_FILE = PROJECT_ROOT / "data" / "raw" / "traffic_data.csv"


# 2. SQL query

INSERT_QUERY = """
    INSERT INTO traffic_data (
        city,
        collected_at,
        current_speed,
        free_flow_speed,
        current_travel_time,
        free_flow_travel_time,
        confidence,
        road_closure
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (city, collected_at) DO NOTHING;
"""


# 3. Validate one traffic observation

def is_valid_traffic_row(row):
    """
    Check whether a traffic observation contains valid data.
    """

    missing_fields = check_missing_values(row)
    invalid_speeds = check_negative_speeds(row)
    invalid_confidence = check_confidence(row)
    invalid_travel_times = check_negative_travel_times(row)
    invalid_dates = check_invalid_date(row)

    # Check road_closure value
    invalid_road_closure = (
        row.get("road_closure", "").strip().lower()
        not in ("true", "false")
    )

    return not (
        missing_fields
        or invalid_speeds
        or invalid_confidence
        or invalid_travel_times
        or invalid_dates
        or invalid_road_closure
    )


# 4. Load CSV data into PostgreSQL

def load_traffic_data():
    """
    Read traffic observations from CSV,
    validate them and insert valid rows into PostgreSQL.
    """

    total_rows = 0
    inserted_rows = 0
    invalid_rows = 0
    duplicate_rows = 0

    # Check that the CSV file exists
    if not CSV_FILE.exists():
        raise FileNotFoundError(f"CSV file not found: {CSV_FILE}")

    # Open the CSV file
    with open(CSV_FILE, mode="r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        # Open one database connection for the entire batch
        with get_connection() as conn:

            with conn.cursor() as cursor:

                for row in reader:

                    total_rows += 1

                    # Validate the observation
                    if not is_valid_traffic_row(row):
                        invalid_rows += 1
                        continue

                    # Prepare values for PostgreSQL
                    values = (
                        row["city"],
                        row["collected_at"],
                        int(row["current_speed"]),
                        int(row["free_flow_speed"]),
                        int(row["current_travel_time"]),
                        int(row["free_flow_travel_time"]),
                        float(row["confidence"]),
                        row["road_closure"].strip().lower() == "true"
                    )

                    # Insert the observation
                    cursor.execute(INSERT_QUERY, values)

                    # Check whether the row was inserted
                    if cursor.rowcount == 1:
                        inserted_rows += 1
                    else:
                        duplicate_rows += 1

    # 5. Display loading report
    print("\n========== DATA LOADING SUMMARY ==========")

    print("Total rows:", total_rows)
    print("Inserted rows:", inserted_rows)
    print("Invalid rows:", invalid_rows)
    print("Duplicate rows:", duplicate_rows)

    print("\nData loading completed successfully!")


# 6. Execute the loader only when running this file directly

if __name__ == "__main__":
    load_traffic_data()