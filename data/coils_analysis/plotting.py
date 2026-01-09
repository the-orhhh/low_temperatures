import matplotlib.pyplot as plt


def plot_voltages(outer_voltages, inner_voltages, title='Coil Voltages: Inner vs Outer', ylabel='Inner Voltage'):
    """Plot inner voltages as a function of outer voltages."""
    # Sort by outer voltage to show relationship clearly
    sorted_data = sorted(zip(outer_voltages, inner_voltages))
    outer_sorted, inner_sorted = zip(*sorted_data)
    
    plt.figure()
    plt.scatter(outer_sorted, inner_sorted, color='blue', alpha=0.6)
    plt.xlabel('Outer Voltage')
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True, alpha=0.3)
    
    plt.show()
