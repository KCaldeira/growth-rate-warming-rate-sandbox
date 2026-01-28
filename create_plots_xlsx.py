#!/usr/bin/env python
"""
Generate growth rate analysis outputs.

This script reads economic projection data, computes growth rates,
and generates both an Excel file and a 2x2 panel visualization.

Usage:
    python create_plots_xlsx.py

Outputs:
    data/output/growth_rates.xlsx - Growth rates by income group
    data/output/panel_plot.png    - 2x2 panel visualization
"""

import os
import pandas as pd
from read_data import read_figure_data, compute_growth_rates, TABLE_NAMES, ROW_LABELS, COL_LABELS
from plot_panels import create_panel_plot
import matplotlib.pyplot as plt


def main():
    # Ensure output directory exists
    os.makedirs("data/output", exist_ok=True)

    # Load and transform data
    print("Reading data...")
    data = read_figure_data("data/input/figure_data.txt")
    growth_rates = compute_growth_rates(data)

    # Export to Excel
    print("Creating Excel file...")
    with pd.ExcelWriter("data/output/growth_rates.xlsx", engine="openpyxl") as writer:
        for i, table_name in enumerate(TABLE_NAMES):
            df = pd.DataFrame(
                growth_rates[i],
                index=ROW_LABELS,
                columns=COL_LABELS
            )
            sheet_name = table_name.replace("-", " ")[:31]
            df.to_excel(writer, sheet_name=sheet_name)
    print("  Saved data/output/growth_rates.xlsx")

    # Generate panel plot
    print("Creating panel plot...")
    fig, axes = create_panel_plot(growth_rates)
    plt.savefig("data/output/panel_plot.png", dpi=150, bbox_inches='tight')
    print("  Saved data/output/panel_plot.png")

    print("Done.")


if __name__ == "__main__":
    main()
