import pandas as pd

CSV_PATH = "sensor_data.csv"

def irrigation_advice(last_soil_moisture: float) -> str:
    # Basit kural: %25 altı = sulama öner
    if last_soil_moisture < 25:
        return "Irrigation recommended (soil moisture is low)."
    return "No irrigation needed for now."

def main():
    df = pd.read_csv(CSV_PATH)

    # Son 10 kayıt üzerinden hızlı özet
    recent = df.tail(10)

    avg_temp = recent["temperature_c"].mean()
    avg_hum = recent["humidity_pct"].mean()
    avg_soil = recent["soil_moisture_pct"].mean()

    last_soil = float(df.iloc[-1]["soil_moisture_pct"])

    print("Last 10 records summary")
    print("----------------------")
    print(f"Avg temperature (C): {avg_temp:.2f}")
    print(f"Avg humidity (%):    {avg_hum:.2f}")
    print(f"Avg soil (%):        {avg_soil:.2f}")
    print()
    print("Decision")
    print("--------")
    print(irrigation_advice(last_soil))

if __name__ == "__main__":
    main()
