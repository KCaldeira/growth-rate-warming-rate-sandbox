import numpy as np
import matplotlib.pyplot as plt
from read_data import read_figure_data, compute_growth_rates, TABLE_NAMES

# Numerical mappings for axes
SSP_GROWTH_RATES = {
    "SSP1": 2.00,
    "SSP2": 1.62,
    "SSP3": 0.34,
    "SSP4": 1.15,
    "SSP5": 2.73,
}
SSP_NAMES = ["SSP1", "SSP2", "SSP3", "SSP4", "SSP5"]
SSP_VALUES = [SSP_GROWTH_RATES[s] for s in SSP_NAMES]  # [2.00, 1.62, 0.34, 1.15, 2.73]

WARMING_LEVELS = {
    "2.6 W m-2": 0.87,
    "4.5 W m-2": 2.27,
    "7.0 W m-2": 3.96,
    "8.5 W m-2": 5.10,
}
WARMING_NAMES = ["2.6 W m-2", "4.5 W m-2", "7.0 W m-2", "8.5 W m-2"]
WARMING_VALUES = [WARMING_LEVELS[w] for w in WARMING_NAMES]  # [0.87, 2.27, 3.96, 5.10]

# Colors for SSP scenarios
SSP_COLORS = {
    "SSP1": "tab:blue",
    "SSP2": "tab:orange",
    "SSP3": "tab:green",
    "SSP4": "tab:red",
    "SSP5": "tab:purple",
}

# Symbols for warming scenarios
WARMING_MARKERS = {
    "2.6 W m-2": "o",
    "4.5 W m-2": "s",
    "7.0 W m-2": "^",
    "8.5 W m-2": "D",
}

# Income group indices
LOW_INCOME_IDX = 3   # "Low-income group"
HIGH_INCOME_IDX = 1  # "High-income group"


def create_panel_plot(growth_rates):
    """
    Create a 2x2 panel scatter plot.

    Layout:
        Left column: Low-income countries
        Right column: High-income countries
        Top row: Warming rate (x) vs GDP growth rate (y)
        Bottom row: Baseline growth rate (x) vs GDP growth rate (y)
    """
    fig, axes = plt.subplots(2, 2, figsize=(10, 8))

    # Extract subset: SSP1-5 (indices 1-5) and warming scenarios 1-4 (skip "No warming")
    # Shape becomes (4, 5, 4) -> (income_groups, ssp_scenarios, warming_scenarios)
    data_subset = growth_rates[:, 1:6, 1:5] * 100  # Convert to percent

    # Fixed y-axis limits for all panels
    y_min = -1
    y_max = 5.5

    # X-axis limits
    x_max_warming = 6.0  # Slightly beyond max warming of 5.10
    x_max_growth = 3.0   # Slightly beyond max baseline growth of 2.73

    income_groups = [
        (LOW_INCOME_IDX, "Low-income countries"),
        (HIGH_INCOME_IDX, "High-income countries"),
    ]

    # X values for line fits (from 0 to max)
    x_fit_warming = np.array([0, x_max_warming])
    x_fit_growth = np.array([0, x_max_growth])

    for col, (income_idx, income_label) in enumerate(income_groups):
        # Top row: Warming (x) vs Growth rate (y)
        ax_top = axes[0, col]
        for ssp_idx, ssp_name in enumerate(SSP_NAMES):
            color = SSP_COLORS[ssp_name]
            x_data = np.array(WARMING_VALUES)
            y_data = data_subset[income_idx, ssp_idx, :]

            # Add linear fit first (drawn under points)
            slope, intercept = np.polyfit(x_data, y_data, 1)
            y_fit = slope * x_fit_warming + intercept
            ax_top.plot(x_fit_warming, y_fit, color=color, linewidth=1, zorder=1)

            # Plot scatter points (drawn over lines)
            for warm_idx, warm_name in enumerate(WARMING_NAMES):
                marker = WARMING_MARKERS[warm_name]
                ax_top.scatter(x_data[warm_idx], y_data[warm_idx], c=color, marker=marker, s=60, zorder=2)

            # Add label at the end of the line (use numerical baseline growth rate)
            y_label = slope * x_max_warming + intercept
            baseline_rate = SSP_VALUES[ssp_idx]
            ax_top.text(x_max_warming + 0.1, y_label, f'{baseline_rate:.2f}', color=color,
                        fontsize=9, va='center', ha='left')

        # Add header label for the column of numbers
        ax_top.text(x_max_warming + 0.1, y_max - 0.15, '%/yr', color='black',
                    fontsize=9, va='top', ha='left')

        ax_top.set_xlim(0, x_max_warming + 1.0)  # Extra space for labels
        ax_top.set_ylim(y_min, y_max)
        ax_top.set_yticks([-1, 0, 1, 2, 3, 4, 5])
        ax_top.axhline(y=0, color='black', linewidth=0.5)
        ax_top.set_xlabel("Global mean warming (°C)")
        ax_top.set_ylabel("GDP growth rate (%/year)")
        ax_top.set_title(income_label)

        # Bottom row: Baseline growth rate (x) vs Growth rate (y)
        ax_bot = axes[1, col]

        # Add linear fits for each warming scenario first (grey lines, drawn under points)
        label_positions = []  # Store (y_position, warming_value) for label adjustment
        for warm_idx, warm_name in enumerate(WARMING_NAMES):
            # Collect points for this warming scenario across all SSPs
            x_data = np.array(SSP_VALUES)
            y_data = np.array([data_subset[income_idx, ssp_idx, warm_idx]
                              for ssp_idx in range(len(SSP_NAMES))])

            # Fit and plot line
            slope, intercept = np.polyfit(x_data, y_data, 1)
            y_fit = slope * x_fit_growth + intercept
            ax_bot.plot(x_fit_growth, y_fit, color='lightgray', linewidth=1, zorder=1)

            # Store label position with numerical warming value
            y_label = slope * x_max_growth + intercept
            warming_value = WARMING_VALUES[warm_idx]
            label_positions.append((y_label, warming_value))

        # Plot scatter points (drawn over lines)
        for ssp_idx, ssp_name in enumerate(SSP_NAMES):
            color = SSP_COLORS[ssp_name]
            x_base = SSP_VALUES[ssp_idx]
            for warm_idx, warm_name in enumerate(WARMING_NAMES):
                marker = WARMING_MARKERS[warm_name]
                y = data_subset[income_idx, ssp_idx, warm_idx]
                ax_bot.scatter(x_base, y, c=color, marker=marker, s=60, zorder=2)

        # Adjust label positions to avoid overlap (minimum spacing of 0.25)
        label_positions.sort(key=lambda x: x[0])  # Sort by y position
        min_spacing = 0.25
        adjusted_positions = []
        for i, (y_pos, val) in enumerate(label_positions):
            if i > 0 and y_pos - adjusted_positions[-1] < min_spacing:
                y_pos = adjusted_positions[-1] + min_spacing
            adjusted_positions.append(y_pos)

        # Add labels with adjusted positions (numerical warming values)
        for (orig_y, warming_value), adj_y in zip(label_positions, adjusted_positions):
            ax_bot.text(x_max_growth + 0.05, adj_y, f'{warming_value:.2f}', color='black',
                        fontsize=8, va='center', ha='left')

        # Add header label just above the highest number label
        header_y = max(adjusted_positions) + 0.35
        ax_bot.text(x_max_growth + 0.05, header_y, '°C/century', color='black',
                    fontsize=8, va='bottom', ha='left')

        ax_bot.set_xlim(0, x_max_growth + 1.2)  # Extra space for labels
        ax_bot.set_ylim(y_min, y_max)
        ax_bot.set_xticks([0, 1, 2, 3])
        ax_bot.set_yticks([-1, 0, 1, 2, 3, 4, 5])
        ax_bot.axhline(y=0, color='black', linewidth=0.5)
        ax_bot.set_xlabel("Baseline growth rate (%/year)")
        ax_bot.set_ylabel("GDP growth rate (%/year)")

    plt.tight_layout()

    return fig, axes


if __name__ == "__main__":
    # Load and transform data
    data = read_figure_data("data/input/figure_data.txt")
    growth_rates = compute_growth_rates(data)

    # Create plot
    fig, axes = create_panel_plot(growth_rates)

    # Save figure
    plt.savefig("data/output/panel_plot.png", dpi=150, bbox_inches='tight')
    print("Saved data/output/panel_plot.png")

    plt.show()
