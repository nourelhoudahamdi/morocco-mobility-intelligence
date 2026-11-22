import os
from pathlib import Path

from dotenv import load_dotenv


# Locate the project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Load environment variables
load_dotenv(PROJECT_ROOT / ".env")


# Configure Psycopg for Windows
_dll_directory = None

if os.name == "nt":
    pg_bin = Path(r"C:\Program Files\PostgreSQL\18\bin")

    if pg_bin.exists():
        _dll_directory = os.add_dll_directory(str(pg_bin))

os.environ["PSYCOPG_IMPL"] = "python"

import psycopg


def get_connection():
    """Create and return a PostgreSQL connection."""

    required_vars = [
        "DB_HOST",
        "DB_PORT",
        "DB_NAME",
        "DB_USER",
        "DB_PASSWORD"
    ]

    for var in required_vars:
        if not os.getenv(var):
            raise ValueError(f"Missing environment variable: {var}")

    connection = psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT")),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )

    return connection

def insert_traffic_data(row):
    """Insert one traffic observation into PostgreSQL."""

    query = """
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

    values = (
        row["city"],
        row["collected_at"],
        int(row["current_speed"]),
        int(row["free_flow_speed"]),
        int(row["current_travel_time"]),
        int(row["free_flow_travel_time"]),
        float(row["confidence"]),
        row["road_closure"].lower() == "true"
    )

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, values)

