import pandas as pd
import numpy as np
import data_processing
from apscheduler.schedulers.background import BackgroundScheduler
import time
from datetime import datetime, timedelta
import requests


now = datetime.now()
delta = now - timedelta(days=30)


def main():
    imei = '352016705784205'
    df = pd.read_json(
        "http://34.101.106.147:56002/api/datalog/352016705784205?limit=99999999")
    df = df[(df["timestamp"] > f"{delta}") &
            (df["timestamp"] < f"{now}")]
    # df = df[(df["timestamp"] > f"{delta}") &
    #         (df["timestamp"] < f"{now}")]
    # df = df[(df["power_status"] == True) & (df["speed"] > 8)]

    dt_arrray = df.to_numpy()[::-1]
    final_data = data_processing.remove_idle_data(dt_arrray)
    x = final_data[:, 7]
    y = final_data[:, 8]

    y_median = data_processing.median_filter(y)

    data_cycle = data_processing.define_cycle(x, y_median)

    data_reg = data_processing.regression(data_cycle)

    final_data = data_processing.fuel_calculation(df, data_reg)
    print(final_data)


main()
