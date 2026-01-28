#!/usr/bin/env python
"""
Generate growth rate analysis outputs.

This script reads economic projection data, computes growth rates,
and generates an Excel file and two 2x2 panel visualizations.

Usage:
    python create_plots_xlsx.py

Outputs:
    data/output/growth_rates.xlsx      - Growth rates by income group
    data/output/panel_plot.png         - Panel plot with numerical labels
    data/output/panel_plot_scenario.png - Panel plot with SSP/RCP labels
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

    # Generate panel plot with numerical labels
    print("Creating panel plots...")
    fig, axes = create_panel_plot(growth_rates, label_style='numerical')
    plt.savefig("data/output/panel_plot.png", dpi=150, bbox_inches='tight')
    print("  Saved data/output/panel_plot.png")
    plt.close(fig)

    # Generate panel plot with SSP/RCP labels
    fig, axes = create_panel_plot(growth_rates, label_style='scenario')
    plt.savefig("data/output/panel_plot_scenario.png", dpi=150, bbox_inches='tight')
    print("  Saved data/output/panel_plot_scenario.png")
    plt.close(fig)

    print("Done.")


if __name__ == "__main__":
    main()
