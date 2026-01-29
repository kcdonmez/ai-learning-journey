import csv
import random
from datetime import datetime
from pathlib import Path

CSV_PATH = Path("sensor_data.csv")

def generate_sensor_row() -> dict:
    return {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature_c": round(random.uniform(18, 35), 2),
        "humidity_pct": round(random.uniform(30, 90), 2),
        "soil_moisture_pct": round(random.uniform(10, 60), 2),
    }

def append_row_to_csv(row: dict, csv_path: Path) -> None:
    file_exists = csv_path.exists()

    with csv_path.open(mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["time", "temperature_c", "humidity_pct", "soil_moisture_pct"]
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

def main():
    row = generate_sensor_row()
    append_row_to_csv(row, CSV_PATH)
    print("Saved:", row)

if __name__ == "__main__":
    main()
