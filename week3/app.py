import json
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException

app = FastAPI(title="AI Journey - Smart Agriculture API")

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "sensor_data.csv"
PROFILE_PATH = BASE_DIR / "crop_profile.json"


def load_profile() -> dict:
    if not PROFILE_PATH.exists():
        raise FileNotFoundError("crop_profile.json not found")
    return json.loads(PROFILE_PATH.read_text(encoding="utf-8"))


def status_range(value: float, vmin: float, vmax: float) -> str:
    if value < vmin:
        return "LOW"
    if value > vmax:
        return "HIGH"
    return "OK"


def irrigation_advice(last_soil: float, threshold: float) -> str:
    if last_soil < threshold:
        return "Irrigation recommended"
    return "No irrigation needed"


def compute_status() -> dict:
    if not CSV_PATH.exists():
        raise FileNotFoundError("sensor_data.csv not found. Run sensor_to_csv.py a few times first.")

    profile = load_profile()
    targets = profile["targets"]
    threshold = profile["rules"]["irrigate_below_soil_moisture_pct"]

    df = pd.read_csv(CSV_PATH)
    last = df.iloc[-1]

    temp = float(last["temperature_c"])
    hum = float(last["humidity_pct"])
    soil = float(last["soil_moisture_pct"])

    return {
        "crop": profile.get("crop", "unknown"),
        "latest": {
            "temperature_c": temp,
            "humidity_pct": hum,
            "soil_moisture_pct": soil,
        },
        "status": {
            "temperature": status_range(temp, targets["temperature_c_min"], targets["temperature_c_max"]),
            "humidity": status_range(hum, targets["humidity_pct_min"], targets["humidity_pct_max"]),
            "soil_moisture": status_range(soil, targets["soil_moisture_pct_min"], targets["soil_moisture_pct_max"]),
        },
        "decision": irrigation_advice(soil, threshold),
    }


@app.get("/")
def root():
    return {"message": "Smart Agriculture API is running. Go to /status"}


@app.get("/status")
def status():
    try:
        return compute_status()
    except FileNotFoundError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
