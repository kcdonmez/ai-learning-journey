import json
import pandas as pd

CSV_PATH = "sensor_data.csv"
PROFILE_PATH = "crop_profile.json"

def load_profile(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def status_range(value: float, vmin: float, vmax: float) -> str:
    if value < vmin:
        return "LOW"
    if value > vmax:
        return "HIGH"
    return "OK"

def irrigation_advice(last_soil: float, threshold: float) -> str:
    if last_soil < threshold:
        return f"Irrigation recommended (soil moisture {last_soil:.2f}% < {threshold}%)."
    return f"No irrigation needed (soil moisture {last_soil:.2f}% >= {threshold}%)."

def main():
    profile = load_profile(PROFILE_PATH)
    targets = profile["targets"]
    threshold = profile["rules"]["irrigate_below_soil_moisture_pct"]

    df = pd.read_csv(CSV_PATH)
    recent = df.tail(10)

    avg_temp = recent["temperature_c"].mean()
    avg_hum = recent["humidity_pct"].mean()
    avg_soil = recent["soil_moisture_pct"].mean()

    last = df.iloc[-1]
    last_temp = float(last["temperature_c"])
    last_hum = float(last["humidity_pct"])
    last_soil = float(last["soil_moisture_pct"])

    print(f"Crop profile: {profile['crop']}")
    print()
    print("Last 10 records summary")
    print("----------------------")
    print(f"Avg temperature (C): {avg_temp:.2f}")
    print(f"Avg humidity (%):    {avg_hum:.2f}")
    print(f"Avg soil (%):        {avg_soil:.2f}")
    print()
    print("Latest reading status vs targets")
    print("-------------------------------")
    print(f"Temperature: {last_temp:.2f} °C -> {status_range(last_temp, targets['temperature_c_min'], targets['temperature_c_max'])}")
    print(f"Humidity:    {last_hum:.2f} %  -> {status_range(last_hum, targets['humidity_pct_min'], targets['humidity_pct_max'])}")
    print(f"Soil:        {last_soil:.2f} %  -> {status_range(last_soil, targets['soil_moisture_pct_min'], targets['soil_moisture_pct_max'])}")
    print()
    print("Decision")
    print("--------")
    print(irrigation_advice(last_soil, threshold))

if __name__ == "__main__":
    main()
