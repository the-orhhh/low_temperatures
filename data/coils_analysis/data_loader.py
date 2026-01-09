import csv
import numpy as np


def load_coil_data(file_path):
    """Load CSV data from file and return as numpy array."""
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append([x for x in row])
    return np.array(data)


def parse_file(data):
    """Parse raw coil data into time and voltage arrays."""
    time, outer_voltages, inner_voltages = [], [], []
    for n in data[1:]:
        time.append(float(n[0]))
        outer_voltages.append(float(n[1]))
        inner_voltages.append(float(n[3]))
    return time, outer_voltages, inner_voltages
