import csv
from datetime import datetime


# 1. Vérifier les valeurs manquantes
def check_missing_values(row):
    missing_fields = []

    for field, value in row.items():
        if not value or not value.strip():
            missing_fields.append(field)

    return missing_fields


# 2. Vérifier les vitesses négatives
def check_negative_speeds(row):
    invalid_fields = []

    try:
        current_speed = float(row["current_speed"])
        free_flow_speed = float(row["free_flow_speed"])

        if current_speed < 0:
            invalid_fields.append("current_speed")

        if free_flow_speed < 0:
            invalid_fields.append("free_flow_speed")

    except (ValueError, TypeError):
        invalid_fields.append("speed_values")

    return invalid_fields


# 3. Vérifier la confiance
def check_confidence(row):
    invalid_fields = []

    try:
        confidence = float(row["confidence"])

        if confidence < 0 or confidence > 1:
            invalid_fields.append("confidence")

    except (ValueError, TypeError):
        invalid_fields.append("confidence")

    return invalid_fields


# 4. Vérifier les temps de trajet négatifs
def check_negative_travel_times(row):
    invalid_fields = []

    try:
        current_time = float(row["current_travel_time"])
        free_flow_time = float(row["free_flow_travel_time"])

        if current_time < 0:
            invalid_fields.append("current_travel_time")

        if free_flow_time < 0:
            invalid_fields.append("free_flow_travel_time")

    except (ValueError, TypeError):
        invalid_fields.append("travel_time_values")

    return invalid_fields


# 5. Vérifier les dates
def check_invalid_date(row):
    invalid_fields = []

    try:
        datetime.fromisoformat(row["collected_at"])

    except (ValueError, TypeError):
        invalid_fields.append("collected_at")

    return invalid_fields


# 6. Initialiser les compteurs
total_rows = 0

rows_with_missing_values = 0
rows_with_invalid_speeds = 0
rows_with_invalid_confidence = 0
rows_with_invalid_travel_times = 0
rows_with_invalid_dates = 0


# 7. Lire et valider le CSV
with open("data/raw/traffic_data.csv", newline="", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        total_rows += 1

        # Vérifier les valeurs manquantes
        missing_fields = check_missing_values(row)

        if missing_fields:
            rows_with_missing_values += 1

        # Vérifier les vitesses
        invalid_speeds = check_negative_speeds(row)

        if invalid_speeds:
            rows_with_invalid_speeds += 1

        # Vérifier la confiance
        invalid_confidence = check_confidence(row)

        if invalid_confidence:
            rows_with_invalid_confidence += 1

        # Vérifier les temps de trajet
        invalid_travel_times = check_negative_travel_times(row)

        if invalid_travel_times:
            rows_with_invalid_travel_times += 1

        # Vérifier les dates
        invalid_dates = check_invalid_date(row)

        if invalid_dates:
            rows_with_invalid_dates += 1


# 8. Afficher le rapport final
print("\n========== VALIDATION SUMMARY ==========")

print("Total rows checked:", total_rows)

print("Rows with missing values:", rows_with_missing_values)
print("Rows with invalid speeds:", rows_with_invalid_speeds)
print("Rows with invalid confidence:", rows_with_invalid_confidence)
print("Rows with invalid travel times:", rows_with_invalid_travel_times)
print("Rows with invalid dates:", rows_with_invalid_dates)


# 9. Déterminer le statut final
if (
    rows_with_missing_values == 0
    and rows_with_invalid_speeds == 0
    and rows_with_invalid_confidence == 0
    and rows_with_invalid_travel_times == 0
    and rows_with_invalid_dates == 0
):
    print("\nValidation status: PASSED")

else:
    print("\nValidation status: FAILED")