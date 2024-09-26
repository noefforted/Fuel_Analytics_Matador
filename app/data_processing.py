import pandas as pd
import numpy as np
from datetime import datetime


def remove_idle_data(data: np.array, tdelay: int = 600):
    res = np.array([True for _ in range(data.shape[0])])
    f_read = False
    f_start_delay = 0
    res[0] = False
    for iter in range(1, data.shape[0]):
        if not data[iter-1, 11] and data[iter, 11]:
            f_read = True
            f_start_delay = data[iter, 1]
        elif data[iter-1, 11] and not data[iter, 11]:
            f_read = False
        if f_read and data[iter, 1] - f_start_delay > np.timedelta64(tdelay, "s"):
            res[iter] = True
        else:
            res[iter] = False
    return data[res]


def median_filter(y):
    window_size = 70  # Pilih ukuran jendela yang tepat
    y_median = pd.Series(y).rolling(window=window_size,
                                    min_periods=1, center=True).median()
    return y_median


def define_cycle(x, y_median):
    cycles_median = []
    current_cycle = []
    n = len(x)

    # Iterasi untuk mendeteksi kenaikan lebih dari 15 dalam rentang x 150
    i = 0
    while i < n - 1:
        start = i
        end = min(i + 150, n - 1)

        # Cek jika ada kenaikan lebih dari 15 dalam rentang tersebut
        if y_median[end] - y_median[start] > 15:
            if current_cycle:
                cycles_median.append(np.array(current_cycle))
                current_cycle = []
            i = end
        else:
            current_cycle.append((x[i], y_median[i]))
            i += 1

    if current_cycle:
        cycles_median.append(np.array(current_cycle))

    return cycles_median


def regression(cycles_median):
    # Plot regresi untuk setiap siklus
    regression_results = []
    for i, cycle in enumerate(cycles_median):
        if len(cycle) > 1:
            x_cycle = cycle[:, 0]
            y_cycle = cycle[:, 1]
            coeffs = np.polyfit(x_cycle, y_cycle, 1)
            poly_eq = np.poly1d(coeffs)
            y_pred = poly_eq(x_cycle)
            y_pred = np.maximum(y_pred, 0)
            regression_results.append(np.column_stack((x_cycle, y_pred)))

    return regression_results


def fuel_calculation(df, data_reg):
    # Menghitung total fuel consumed dan fuel rate untuk setiap siklus
    cycle_fuel_consumed = []
    cycle_distance = []
    fuel_rate = []
    time_initial_list = []
    time_terminal_list = []

    for cycle in data_reg:
        if len(cycle) > 1:  # Memastikan ada lebih dari satu titik dalam siklus
            x_cycle = cycle[:, 0]
            y_cycle = cycle[:, 1]

            ymax = np.max(y_cycle)
            ymin = np.min(y_cycle)

            # Menghitung total fuel consumed dan fuel rate
            total_fuel = round(ymax - ymin, 3)
            total_distance = x_cycle[np.argmin(
                y_cycle)] - x_cycle[np.argmax(y_cycle)]
            rate = round((total_distance / 1000) / (ymax - ymin), 3)

            cycle_fuel_consumed.append(total_fuel)
            fuel_rate.append(rate)
            cycle_distance.append(total_distance)

        # Mendapatkan time_initial dan time_terminal
        res_awal = df[df["distance_total"] == x_cycle[0]]
        time_initial = datetime.fromisoformat(
            str(res_awal.iloc[0]["timestamp"])).strftime("%Y-%m-%dT%H:%M:%SZ")
        res_akhir = df[df["distance_total"] == x_cycle[-1]]
        time_terminal = datetime.fromisoformat(
            str(res_akhir.iloc[0]["timestamp"])).strftime("%Y-%m-%dT%H:%M:%SZ")

        # Simpan nilai time_initial dan time_terminal untuk setiap siklus
        time_initial_list.append(time_initial)
        time_terminal_list.append(time_terminal)

    # Membuat DataFrame untuk hasilnya
    fuel_data_summary = pd.DataFrame({
        'cycle': range(1, len(cycle_fuel_consumed) + 1),
        'cycle_fuel_consumed': cycle_fuel_consumed,
        'cycle_distance': cycle_distance,
        'fuel_rate': fuel_rate,
        'time_awal': time_initial_list,
        'time_akhir': time_terminal_list
    })
    return fuel_data_summary
