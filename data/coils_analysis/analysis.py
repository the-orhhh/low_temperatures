import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

def load_coil_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append([x for x in row])
    return np.array(data)

def parse_file(data):
    time, outer_voltages, inner_voltages = [], [], []
    for n in data[1:]:
        time.append(float(n[0]))
        outer_voltages.append(float(n[1]))
        inner_voltages.append(float(n[3]))
    return time, outer_voltages, inner_voltages

def plot_voltages(outer_voltages, inner_voltages):
    # Sort by outer voltage
    sorted_data = sorted(zip(outer_voltages, inner_voltages))
    outer_sorted, inner_sorted = zip(*sorted_data)
    
    plt.figure()
    plt.plot(outer_sorted, inner_sorted, color='blue', alpha=0.6)
    plt.xlabel('Outer Voltages')
    plt.ylabel('Inner Voltages')
    plt.title('Coil Voltages: Inner vs Outer')
    plt.grid(True, alpha=0.3)
    
    plt.show()

def split(time, outer_voltages, inner_voltages, cut=0):
    outer_max = outer_voltages.index(max(outer_voltages))
    time_ascending, time_descending = time[:outer_max+1],  time[outer_max+1:]
    outer_ascending, outer_descending = outer_voltages[:outer_max+1], outer_voltages[outer_max+1:]
    inner_ascending, inner_descending = inner_voltages[:outer_max+1], inner_voltages[outer_max+1:]
    if cut == 0:
        return time_ascending, outer_ascending, inner_ascending 
    else:
        return time_descending, outer_descending, inner_descending
    
def plot_magnetization(time, outer_voltages, inner_voltages):
    t, outer, inner = split(time, outer_voltages, inner_voltages, cut=0)
    magnetization = cumulative_trapezoid(inner, t, initial=0.0)
    plot_voltages(outer, magnetization)

def main():
    file_path = "/Users/orharpazi/Files/Laboratory/low_temperatures/data/csv/coils/3125-1.csv"
    time, outer_voltages, inner_voltages = parse_file(load_coil_data(file_path))
    #plot_voltages(outer_voltages, inner_voltages)
    #plot_voltages(*split(time, outer_voltages, inner_voltages, cut=0)[1:])
    #plot_voltages(*split(time, outer_voltages, inner_voltages, cut=1)[1:])
    plot_magnetization(time, outer_voltages, inner_voltages)

if __name__ == "__main__":
    main()