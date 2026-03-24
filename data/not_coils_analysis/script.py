import csv
import os
from pathlib import Path
import numpy as np
from scipy.signal import savgol_filter

def process_file_with_filter(csv_path):
    """
    Process CSV file with filtering algorithm and calculate highest dR/dV
    """
    data = np.genfromtxt(csv_path, delimiter=",", skip_header=1)
    time = data[:, 0]
    voltage = data[:, 1]
    resistance = data[:, 2]
    
    # Filter: keep only data from max resistance onwards
    max_resistance_index = np.argmax(resistance)
    data = data[max_resistance_index+10:-20]
    time = data[:, 0]
    voltage = data[:, 1]
    resistance = data[:, 2]
    
    # Calculate derivative dR/dV
    dR_dV = np.gradient(resistance, voltage)
    
    # Smooth the derivative with at least 6 points using Savitzky-Golay filter
    if len(dR_dV) >= 7:
        # Use window length of 7 (must be odd) with polynomial order 3
        dR_dV_smoothed = savgol_filter(dR_dV, window_length=7, polyorder=3)
    else:
        # If not enough points, use a smaller window
        dR_dV_smoothed = dR_dV
    
    # Find the highest derivative
    max_derivative_index = np.argmax(dR_dV_smoothed)
    max_derivative_value = dR_dV_smoothed[max_derivative_index]
    voltage_at_max_derivative = voltage[max_derivative_index]
    resistance_at_max_derivative = resistance[max_derivative_index]
    
    return {
        'max_dR_dV': max_derivative_value,
        'voltage': voltage_at_max_derivative,
        'resistance': resistance_at_max_derivative,
        'index': max_derivative_index
    }

# Load CSV files from data/csv directory
csv_dir = '/Users/orharpazi/Files/Laboratory/low_temperatures/data/csv'
output_file = '/Users/orharpazi/Files/Laboratory/low_temperatures/data/not_coils_analysis/results.csv'

# Sort filenames numerically if possible
filenames = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
try:
    # Try to sort numerically (e.g., 320.csv, 325.csv)
    filenames = sorted(filenames, key=lambda x: float(x.replace('.csv', '')))
except ValueError:
    # Fall back to alphabetical sorting
    filenames = sorted(filenames)

print(f"Processing {len(filenames)} files...\n")

# Prepare output CSV
results = []

for filename in filenames:
    if filename[0].isdigit():  # Process only files starting with a digit
        filepath = os.path.join(csv_dir, filename)
        
        try:
            result = process_file_with_filter(filepath)
            
            print(f"File: {filename}")
            print(f"  Highest dR/dV: {result['max_dR_dV']:.6f}")
            print(f"  Voltage: {result['voltage']:.4f}")
            print(f"  Resistance: {result['resistance']:.4f}")
            print()
            
            # Store result for CSV
            results.append({
                'filename': filename,
                'voltage': result['voltage'],
                'resistance': result['resistance'],
                'max_dR_dV': result['max_dR_dV'],
                'index-max_index': result['index']
            })
        except Exception as e:
            print(f"Error processing {filename}: {e}\n")

# Write results to CSV
with open(output_file, 'w', newline='') as f:
    writer = csv.DictWriter(f, fieldnames=['filename', 'voltage', 'resistance', 'max_dR_dV', 'index-max_index'])
    writer.writeheader()
    writer.writerows(results)

print(f"Results saved to {output_file}")