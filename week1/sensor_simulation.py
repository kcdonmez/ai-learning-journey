import random
from datetime import datetime

def get_temperature():
    return round(random.uniform(18, 35), 2)

def get_humidity():
    return round(random.uniform(30, 90), 2)

def get_soil_moisture():
    return round(random.uniform(10, 60), 2)

def main():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    temp = get_temperature()
    hum = get_humidity()
    soil = get_soil_moisture()

    print(f"Time: {now}")
    print(f"Temperature: {temp} °C")
    print(f"Humidity: {hum} %")
    print(f"Soil moisture: {soil} %")

if __name__ == "__main__":
    main()
