# main.py
import pandas as pd
import data_processing
from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime, timedelta
import requests

now = datetime.now()
delta = now - timedelta(days=30)

url = "http://127.0.0.1:8000/fuel-rate"  # Endpoint API Anda


def main():
    imei = '352016705784205'

    # Mengambil data dari sumber eksternal
    df = pd.read_json(
        "http://34.101.106.147:56002/api/datalog/352016705784205?limit=99999999")

    # Filter data berdasarkan timestamp
    df = df[(df["timestamp"] > f"{delta}") & (df["timestamp"] < f"{now}")]

    # Pemrosesan data sesuai kebutuhan
    dt_arrray = df.to_numpy()[::-1]
    adjusted_data = data_processing.remove_idle_data(dt_arrray)
    x = adjusted_data[:, 7]
    y = adjusted_data[:, 8]

    # Aplikasi filter median dan siklus data
    y_median = data_processing.median_filter(y)
    data_cycle = data_processing.define_cycle(x, y_median)
    data_reg = data_processing.regression(data_cycle)

    # Kalkulasi akhir dan membentuk data yang akan dikirim
    final_data = data_processing.fuel_calculation(df, data_reg)

    print(f"{final_data}\n")  # Cetak hasil pemrosesan untuk debug

    # Mengonversi DataFrame menjadi list of dictionaries agar siap dikirim sebagai JSON
    dict_final_data = final_data.to_dict(orient='records')
    headers = {'Content-Type': 'application/json'}

    # Mengirim data ke API menggunakan requests
    response = requests.post(url, json=dict_final_data, headers=headers)

    if response.status_code == 201:
        print("Data berhasil terkirim ke API dan disimpan ke database PostgreSQL")
    else:
        print(f"Data gagal terkirim, status: {response.status_code}")
        print(f"Response: ", response.text)


# Menggunakan scheduler untuk menjalankan `main` pada interval tertentu
scheduler = BackgroundScheduler()

# Menambahkan pekerjaan dengan interval 15 detik (atau ubah sesuai kebutuhan)
scheduler.add_job(main, 'interval', seconds=15)

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
