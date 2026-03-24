from matplotlib import pyplot as plt
import numpy as np
import os

csv_dir = "/Users/orharpazi/Files/Laboratory/low_temperatures/data/csv"
filename = "set2.csv"
csv_path = os.path.join(csv_dir, filename)

data = np.genfromtxt(csv_path, delimiter=",", skip_header=1)
time = data[:, 0]
voltage = data[:, 1]
resistance = data[:, 2]

max_resistance_index = np.argmax(resistance)
#data = data[time >= time[max_resistance_index]]
time = data[:, 0]
voltage = data[:, 1]
resistance = data[:, 2]

plt.figure(figsize=(10, 6))
plt.plot(time, resistance, marker="o", linestyle="-", color="b")
plt.title("Voltage vs Resistance")
plt.xlabel("Voltage (V)")
plt.ylabel("Resistance (Ω)")
plt.grid()
plt.show()