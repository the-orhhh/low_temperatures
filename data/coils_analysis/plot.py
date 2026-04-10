import os
import numpy as np
from matplotlib import pyplot as plt
import scienceplots
plt.style.use(['science'])

def import_files(t):
    if t != 3:
        return [f for f in os.listdir('data/csv/coils') if f.endswith(f'{t}.csv')]
    else:
        return [f for f in os.listdir('data/csv/coils')]

def plot(file, data):
    time = data[:, 0]
    outer_voltage = data[:, 1]
    inner_voltage = data[:, 3]
    inner_voltage = inner_voltage - np.mean(inner_voltage[-20:])  # Remove DC offset
    magnetisation = - np.cumsum(inner_voltage) * np.mean(np.diff(time))  # Simple integration for magnetization
    magnetic_field = (outer_voltage) * 600  #
    idx = magnetic_field > 0.99 * np.max(magnetic_field)
    p = np.polyfit(time[idx], magnetisation[idx], 1)
    magnetisation = magnetisation - (p[0]*time + p[1])
    plt.plot(magnetic_field, magnetisation, label='File: ' + file)


def main():
    t = 2
    plt.figure()
    integrate = False
    filter = False
    save_to_folder = 'output'  # Set to folder path to save plots, or None to display only
    files = import_files(t)
    files.sort()  # Sort files for consistent plotting order
    for file in files:
        with open(f'data/csv/coils/{file}', 'r') as f:
            data = np.loadtxt(f, delimiter=',', skiprows=1)
            #data = data[data[:, 1] > 10/600]  # Filter rows where outer voltage > 10
            if filter:
                max_outer_index = np.argmax(data[:, 1])
                data = data[:max_outer_index+1]
            data = data[data[:, 1] > 5/600]
            datamax = np.max(data[:, 1])
            #data = data[data[:, 1] < datamax - 5/600]  # Keep only data where outer voltage < 90% of its max
            if integrate:
                #data[:, 3] = data[:, 3] - np.mean(data[:, 3][data[:, 1] > datamax - 20/600])  # Remove DC offset using points where outer voltage > 10
                data[:, 3] = - np.cumsum(data[:, 3]) * np.mean(np.diff(data[:, 0]))  # Integrate inner voltage to get magnetization
            plot(file, data)
    plt.xlabel('Magnetic Field (Gauss)')
    plt.ylabel('Magnetization (emu)')
    plt.title('Magnetization vs Magnetic Field')
    plt.legend()
    plt.grid()
    
    if save_to_folder:
        os.makedirs(save_to_folder, exist_ok=True)
        filename = f'{save_to_folder}/plot_t{t}.png'
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f'Plot saved to {filename}')
    else:
        plt.show()

if __name__ == "__main__":    main()