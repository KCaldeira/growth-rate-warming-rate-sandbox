import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Labels for the data dimensions
TABLE_NAMES = ["All-country average", "High-income group", "Middle-income group", "Low-income group"]
ROW_LABELS = ["No growth", "SSP1", "SSP2", "SSP3", "SSP4", "SSP5"]
COL_LABELS = ["No warming", "2.6 W m-2", "4.5 W m-2", "7.0 W m-2", "8.5 W m-2"]


def read_figure_data(filepath):
    """
    Read the figure data from a text file into a 4x6x5 numpy array.

    Dimensions:
        - Axis 0 (4): Income groups (All-country, High, Middle, Low)
        - Axis 1 (6): Growth scenarios (No growth, SSP1-5)
        - Axis 2 (5): Warming scenarios (No warming, 2.6, 4.5, 7.0, 8.5 W m-2)

    Returns:
        numpy.ndarray: Shape (4, 6, 5) containing the data values
    """
    data = np.zeros((4, 6, 5))

    with open(filepath, 'r') as f:
        lines = f.readlines()

    table_idx = -1
    row_idx = 0

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Check if this is a table header
        if line in TABLE_NAMES:
            table_idx += 1
            row_idx = 0
            continue

        # Skip column header lines
        if line.startswith("No warming") or line.startswith("\t"):
            continue

        # Parse data rows
        parts = line.split('\t')
        if len(parts) >= 6 and parts[0] in ROW_LABELS:
            row_idx = ROW_LABELS.index(parts[0])
            values = [float(v) for v in parts[1:6]]
            data[table_idx, row_idx, :] = values

    return data


def compute_growth_rates(data, years=80):
    """
    Transform per-capita GDP data into fractional average annual growth rates.

    For each income group layer:
        1. Divide all values by the [0,0] element (No growth, No warming baseline)
        2. Take the nth root (where n = years) to get average annual multiplier
        3. Subtract 1.0 to get fractional growth rate

    Args:
        data: numpy array of shape (4, 6, 5) with per-capita GDP values
        years: number of years over which growth occurred (default 80)

    Returns:
        numpy.ndarray: Shape (4, 6, 5) containing fractional annual growth rates
    """
    growth_rates = np.zeros_like(data)

    for i in range(data.shape[0]):
        baseline = data[i, 0, 0]  # No growth, No warming value for this income group
        normalized = data[i] / baseline
        growth_rates[i] = normalized ** (1.0 / years) - 1.0

    return growth_rates


if __name__ == "__main__":
    # Read the data
    data = read_figure_data("data/input/figure_data.txt")

    print(f"Data shape: {data.shape}")
    print(f"\nTable names: {TABLE_NAMES}")
    print(f"Row labels: {ROW_LABELS}")
    print(f"Column labels: {COL_LABELS}")

    # Example: print the All-country average table
    print(f"\n{TABLE_NAMES[0]} (per-capita GDP):")
    print(data[0])

    # Compute growth rates
    growth_rates = compute_growth_rates(data)

    print(f"\n{TABLE_NAMES[0]} (fractional annual growth rates):")
    print(growth_rates[0])

    # Show as percentages for readability
    print(f"\n{TABLE_NAMES[0]} (percent annual growth rates):")
    print(growth_rates[0] * 100)
