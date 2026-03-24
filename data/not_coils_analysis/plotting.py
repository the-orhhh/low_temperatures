from matplotlib import pyplot as plt
import numpy as np
import os

csv_dir = "/Users/orharpazi/Files/Laboratory/low_temperatures/data/csv"
filename = input("Enter the CSV filename: ")+".csv"
csv_path = os.path.join(csv_dir, filename)

data = np.genfromtxt(csv_path, delimiter=",", skip_header=1)
time = data[:, 0]
voltage = data[:, 1]
resistance = data[:, 2]

max_resistance_index = np.argmax(resistance)
data = data[max_resistance_index+10:-20]
time = data[:, 0]
voltage = data[:, 1]
resistance = data[:, 2]

plt.figure(figsize=(10, 6))
plt.plot(voltage, resistance, marker="o", linestyle="-", color="b")
plt.title("Voltage vs Resistance")
plt.xlabel("Voltage (V)")
plt.ylabel("Resistance (Ω)")
plt.grid()
plt.show()