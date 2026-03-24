from scipy.integrate import cumulative_trapezoid
import numpy as np
import matplotlib.pyplot as plt
from data_loader import load_coil_data, parse_file
from plotting import plot_currents
from fit import fit_type_i, fit_type_ii, type_i_curve, type_ii_curve
import os
import pandas as pd

def split(time, outer_currents, inner_voltages, cut=0):
    outer_max = outer_currents.index(max(outer_currents))
    time_ascending, time_descending = time[:outer_max+1],  time[outer_max+1:]
    outer_ascending, outer_descending = outer_currents[:outer_max+1], outer_currents[outer_max+1:]
    inner_ascending, inner_descending = inner_voltages[:outer_max+1], inner_voltages[outer_max+1:]
    if cut == 0:
        return time_ascending, outer_ascending, inner_ascending 
    else:
        return time_descending, outer_descending, inner_descending

def critical_point(time, outer_currents, inner_voltages, cut=0):
    t, outer, inner = split(time, outer_currents, inner_voltages, cut=cut)
    Bfield = [(x - min(outer)) * 600 for x in outer]  # in Gauss, normalized to min
    magnetization = cumulative_trapezoid(inner, t, initial=0.0)
    Bfield_positive = np.array([b for b, m in zip(Bfield, magnetization) if b >= 20 and abs(b) < min(Bfield)+600])
    magnetization_positive = np.array([m for b, m in zip(Bfield, magnetization) if b >= 20 and abs(b) < min(Bfield)+600])
    dM_dB = np.abs(np.gradient(magnetization_positive, Bfield_positive))
    critical_index = np.argmax(dM_dB)
    critical_B = Bfield_positive[critical_index]
    critical_M = magnetization_positive[critical_index]
    return critical_B, critical_M

def fit_magnetization(time, Bfield, magnetization, type='i'):
    if type == 'i':
        popt, pcov = fit_type_i(Bfield, magnetization)
    elif type == 'ii':
        popt, pcov = fit_type_ii(Bfield, magnetization)
    else:
        raise ValueError("Use 'i' or 'ii'. Dumbass")
    return popt, pcov

def plot_magnetization(time, outer_currents, inner_voltages):
    """Plot raw magnetization data vs magnetic field."""
    t, outer, inner = split(time, outer_currents, inner_voltages, cut=1)
    Bfield = [(x - outer[0]) * 600 for x in outer]  # in Gauss
    magnetization = cumulative_trapezoid(inner, t, initial=0.0)
    
    plt.figure(figsize=(10, 6))
    plt.scatter(Bfield, magnetization, color='blue', alpha=0.6)
    plt.xlabel('Magnetic Field (Gauss)')
    plt.ylabel('Magnetization')
    plt.title('Magnetization vs Magnetic Field')
    plt.grid(True, alpha=0.3)
    plt.show()


def plot_magnetization_fit(time, outer_currents, inner_voltages, type='i'):
    t, outer, inner = split(time, outer_currents, inner_voltages, cut=0)
    Bfield = [(x - outer[0]) * 600 for x in outer] # in Gauss
    magnetization = cumulative_trapezoid(inner, t, initial=0.0)
    popt, pcov = fit_magnetization(t, Bfield, magnetization, type=type)
    
    # Plot magnetization and fit
    plt.figure(figsize=(10, 6))
    plt.scatter(Bfield, magnetization, label='Data', alpha=0.6)
    
    # Generate fitted curve
    Bfield_fit = np.linspace(min(Bfield), max(Bfield), 100)
    if type == 'i':
        magnetization_fit = type_i_curve(Bfield_fit, *popt)
    else:
        magnetization_fit = type_ii_curve(Bfield_fit, *popt)
    
    plt.plot(Bfield_fit, magnetization_fit, 'r-', label=f'Fit (type {type})')
    plt.xlabel('Magnetic Field (Gauss)')
    plt.ylabel('Magnetization')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.title(f'Magnetization vs Magnetic Field (Type {type.upper()})')
    plt.show()
    
    return popt, pcov


def analyze_all_coils(coils_dir="/Users/orharpazi/Files/Laboratory/low_temperatures/data/csv/coils"):
    """Analyze all coil files in the directory and return aggregated results.
    
    Returns:
        pd.DataFrame: Results with columns [filename, ascending_B, ascending_M, descending_B, descending_M]
    """
    results = []
    
    # Get all CSV files in the directory
    csv_files = sorted([f for f in os.listdir(coils_dir) if f.endswith('.csv')])
    
    for csv_file in csv_files:
        file_path = os.path.join(coils_dir, csv_file)
        try:
            time, outer_currents, inner_voltages = parse_file(load_coil_data(file_path))
            
            # Get critical points for ascending (cut=0) and descending (cut=1)
            asc_B, asc_M = critical_point(time, outer_currents, inner_voltages, cut=0)
            desc_B, desc_M = critical_point(time, outer_currents, inner_voltages, cut=1)
            
            results.append({
                'filename': csv_file,
                'ascending_B': asc_B,
                'ascending_M': asc_M,
                'descending_B': desc_B,
                'descending_M': desc_M
            })
            print(f"✓ {csv_file}")
        except Exception as e:
            print(f"✗ {csv_file}: {str(e)}")
    
    df = pd.DataFrame(results)
    return df


def main():
    file_path = "/Users/orharpazi/Files/Laboratory/low_temperatures/data/csv/coils/3125-1.csv"
    time, outer_currents, inner_voltages = parse_file(load_coil_data(file_path))
    #plot_currents(outer_currents, inner_voltages)
    #plot_currents(*split(time, outer_currents, inner_voltages, cut=0)[1:])
    #plot_currents(*split(time, outer_currents, inner_voltages, cut=1)[1:])
    print("Critical Point (cut=0):", critical_point(time, outer_currents, inner_voltages, cut=0))
    print("Critical Point (cut=1):", critical_point(time, outer_currents, inner_voltages, cut=1))
    plot_magnetization(time, outer_currents, inner_voltages)
    #plot_magnetization_fit(time, outer_currents, inner_voltages, type='i')
    
    # Analyze all coils and display results
    print("\n" + "="*80)
    print("ANALYZING ALL COILS")
    print("="*80)
    results_df = analyze_all_coils()
    print("\nResults:")
    print(results_df.to_string(index=False))
    
    return results_df

if __name__ == "__main__":
    main()