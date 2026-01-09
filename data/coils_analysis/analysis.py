from scipy.integrate import cumulative_trapezoid
from data_loader import load_coil_data, parse_file
from plotting import plot_voltages

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
    plot_voltages(outer, magnetization, title='Magnetization vs Outer Voltage', ylabel='Magnetization')

def main():
    file_path = "/Users/orharpazi/Files/Laboratory/low_temperatures/data/csv/coils/3125-1.csv"
    time, outer_voltages, inner_voltages = parse_file(load_coil_data(file_path))
    #plot_voltages(outer_voltages, inner_voltages)
    #plot_voltages(*split(time, outer_voltages, inner_voltages, cut=0)[1:])
    #plot_voltages(*split(time, outer_voltages, inner_voltages, cut=1)[1:])
    plot_magnetization(time, outer_voltages, inner_voltages)

if __name__ == "__main__":
    main()