import pandas as pd
import numpy as np


def median_filter(y):
    window_size = 70  # Pilih ukuran jendela yang tepat
    y_median = pd.Series(y).rolling(window=window_size,
                                    min_periods=1, center=True).median()
    return y_median


def regression(x, y_median):
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

    # Plot regresi untuk setiap siklus
    regression_results = []
    for i, cycle in enumerate(cycles_median):
        if len(cycle) > 1:
            x_cycle = cycle[:, 0]
            y_cycle = cycle[:, 1]
            coeffs = np.polyfit(x_cycle, y_cycle, 3)
            poly_eq = np.poly1d(coeffs)
            y_pred = poly_eq(x_cycle)
            regression_results.append(np.column_stack((x_cycle, y_pred)))

    return regression_results


def fuel_calculation(df, cycles_median):
    # Menghitung total fuel consumed dan fuel rate untuk setiap siklus
    fuel_consumed = []
    fuel_rate = []
    time_initial_list = []
    time_terminal_list = []

    for cycle in cycles_median:
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

            fuel_consumed.append(total_fuel)
            fuel_rate.append(rate)

            # Mendapatkan time_initial dan time_terminal
            res_awal = df[df["distance_total"] == x_cycle[0]]
            time_initial = int(res_awal.iloc[0]["timestamp"].timestamp())
            res_akhir = df[df["distance_total"] == x_cycle[-1]]
            time_terminal = int(res_akhir.iloc[0]["timestamp"].timestamp())

            # Simpan nilai time_initial dan time_terminal untuk setiap siklus
            time_initial_list.append(time_initial)
            time_terminal_list.append(time_terminal)

    # Membuat DataFrame untuk hasilnya
    fuel_data_summary = pd.DataFrame({
        'Cycle': range(1, len(fuel_consumed) + 1),
        'Fuel_Consumed': fuel_consumed,
        'Fuel_Rate': fuel_rate,
        'Time_Awal': time_initial_list,
        'Time_Akhir': time_terminal_list
    })
    return fuel_data_summary


# x, y = import_data()
# y_median = median_filter(y)
# y_regression = regression(x, y_median)
# fuel_calculation(x, y_regression)
