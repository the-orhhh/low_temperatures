import os
import numpy as np
from scipy.integrate import cumulative_trapezoid


def import_files(t):
    return [f for f in os.listdir('data/csv/coils') if f.endswith(f'-{t}.csv')]


def type1(file):
    with open(f'data/csv/coils/{file}', 'r') as f:
        data = f.readlines()[1:]  # skip header
        data = [line for line in data if float(line.strip().split(',')[1]) > 0.1]

    times = []
    inner = []
    outer = []

    for line in data:
        cols = line.strip().split(',')
        times.append(float(cols[0]))
        outer.append(float(cols[1]))
        inner.append(float(cols[3]))

    times = np.array(times)
    outer = np.array(outer)
    inner = np.array(inner)

    max_idx = np.argmax(outer)
    times_asc = times[:max_idx+1]
    outer_asc = outer[:max_idx+1]
    inner_asc = inner[:max_idx+1]

    M = - cumulative_trapezoid(inner_asc, times_asc, initial=0.0)

    # Convert outer voltage to magnetic field in Gauss
    Bfield = (outer_asc - np.min(outer_asc)) * 600

    # Filter to linear response region
    mask = (Bfield >= 20) & (np.abs(Bfield) < np.min(Bfield) + 600)
    Bfield_filt = Bfield[mask]
    M_filt = M[mask]

    dM_dB = np.gradient(M_filt, Bfield_filt)

    # Find peak of |dM/dB| (phase transition)
    critical_idx = np.argmax(np.abs(dM_dB))

    return {
        "critical_B": Bfield_filt[critical_idx],
        "critical_M": M_filt[critical_idx],
    }


def smooth(x, window=11):
    if window < 3:
        return x
    kernel = np.ones(window) / window
    return np.convolve(x, kernel, mode='same')


def load_coil_data(file):
    """Load coil data from CSV file."""
    with open(f'data/csv/coils/{file}', 'r') as f:
        data = f.readlines()[1:]  # skip header

    times, outer, inner = [], [], []
    for line in data:
        cols = line.strip().split(',')
        times.append(float(cols[0]))
        outer.append(float(cols[1]))
        inner.append(float(cols[3]))

    return np.array(times), np.array(outer), np.array(inner)


def filter_data(times, outer, inner, min_field=5/600, max_field_offset=5/600):
    """Filter data by field strength boundaries."""
    mask = (outer > min_field) & (outer < np.max(outer) - max_field_offset)
    return times[mask], outer[mask], inner[mask]


def compute_critical_field(times, outer, inner):
    """Compute critical field from magnetization gradient."""
    M = cumulative_trapezoid(inner, times, initial=0.0)
    Bfield = (outer - np.min(outer)) * 600
    #dM_dB = np.gradient(M, Bfield)
    
    critical_idx = np.argmin(M)
    return Bfield[critical_idx]


def type2(file):
    times, outer, inner = load_coil_data(file)

    # Find peak and split at maximum outer field
    max_idx = np.argmax(outer)
    
    # Split into ascending and descending branches
    times_asc, outer_asc, inner_asc = (times[:max_idx+1], outer[:max_idx+1], inner[:max_idx+1])
    times_dec, outer_dec, inner_dec = (times[max_idx:], outer[max_idx:], inner[max_idx:])

    # Filter both branches
    times_asc, outer_asc, inner_asc = filter_data(times_asc, outer_asc, inner_asc)
    times_dec, outer_dec, inner_dec = filter_data(times_dec, outer_dec, inner_dec)

    # Compute critical fields
    hc1_asc = compute_critical_field(times_asc, outer_asc, inner_asc)
    hc1_dec = compute_critical_field(times_dec, outer_dec, inner_dec)

    return {
        "Hc1_asc": (hc1_asc,),
        "Hc1_dec": (hc1_dec,),
    }


def main():
    results = []
    for t in [1, 2]:
        files = import_files(t)
        for file in files:
            if t == 1:
                results.append((file, type1(file)))
            else:
                results.append((file, type2(file)))
    
    results.sort(key=lambda x: x[0])  # Sort by filename for consistent output
    results_1 = [r for r in results if 'critical_B' in r[0]]
    results_2 = [r for r in results if r not in results_1]

    for filename, result in results:
        if 'critical_B' in result:
            print(f"{filename[:3].strip('.')},{result['critical_B']:.2f}")
    print()
    for filename, result in results:
            if 'critical_B' not in result:
                print(f"{filename[:4].strip('.-')},{result['Hc1_asc'][0]:.2f}")
    print()
    for filename, result in results:
            if 'critical_B' not in result:
                print(f"{filename[:4].strip('.-')},{result['Hc1_dec'][0]:.2f}")


if __name__ == "__main__":
    main()