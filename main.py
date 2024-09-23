import pandas as pd
import numpy as np
import data_processing
from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime, timedelta
import requests
import json

now = datetime.now()
delta = now - timedelta(days=3)

url = "http://127.0.0.1:8000/fuel-rate"


def main():
    imei = '352016705784205'
    df = pd.read_json(
        "http://34.101.106.147:56002/api/datalog/352016705784205?limit=50000")
    print(type(df["timestamp"]))
    df = df[(df["timestamp"] > f"{delta}") &
            (df["timestamp"] < f"{now}")]
    df = df[(df["power_status"] == True) & (df["speed"] > 8)]

    x = np.array(df["distance_total"])
    y = np.array(df["fuel"])

    x = x[::-1]  # OPTIONAL KARENA DATA DI API TERBALIK
    y = y[::-1]  # OPTIONAL KARENA DATA DI API TERBALIK

    y_median = data_processing.median_filter(y)

    data_reg = data_processing.regression(x, y_median)

    final_data = data_processing.fuel_calculation(df, data_reg)

    print(f"{final_data}\n")

    dict_final_data = final_data.to_dict(orient='records')

    response = requests.post(url, json=dict_final_data)

    if response.status_code == 201:
        print("Data terkirim")
    else:
        print(f"Data gagal terkirim, status: {response.status_code}")
        print(f"Response: ", response.text)


scheduler = BackgroundScheduler()

# Menambahkan pekerjaan dengan interval-based (setiap 5 detik)
# scheduler.add_job(main, 'interval', minutes=30)
scheduler.add_job(main, 'interval', seconds=5)

# Memulai scheduler
scheduler.start()

try:
    # Menjaga program tetap berjalan
    while True:
        time.sleep(1)
except (SystemExit):
    # Menghentikan scheduler jika program dihentikan
    scheduler.shutdown()
    print("Scheduler telah dihentikan.")
