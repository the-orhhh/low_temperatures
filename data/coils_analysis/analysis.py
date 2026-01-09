import os
import csv
import numpy as np
import matplotlib.pyplot as plt

def load_coil_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append([x for x in row])
    return np.array(data)

def parse_file(data):
    outer_voltages, inner_voltages = [], []
    for n in data[1:]:
        outer_voltages.append(float(n[1]))
        inner_voltages.append(float(n[3]))
    return outer_voltages, inner_voltages

def plot_voltages(outer_voltages, inner_voltages):
    # Sort by outer voltage
    sorted_data = sorted(zip(outer_voltages, inner_voltages))
    outer_sorted, inner_sorted = zip(*sorted_data)
    
    plt.figure()
    plt.scatter(outer_sorted, inner_sorted, color='blue', alpha=0.6)
    plt.xlabel('Outer Voltages')
    plt.ylabel('Inner Voltages')
    plt.title('Coil Voltages: Inner vs Outer')
    plt.grid(True, alpha=0.3)
    
    plt.show()

def main():
    file_path = "/Users/orharpazi/Files/Laboratory/low_temperatures/data/csv/coils/3125-1.csv"
    outer_voltages, inner_voltages = parse_file(load_coil_data(file_path))
    print("1st Outer Voltage:", outer_voltages[0])
    print("1st Inner Voltage:", inner_voltages[0])
    plot_voltages(outer_voltages, inner_voltages)
if __name__ == "__main__":
    main()