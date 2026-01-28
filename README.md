# Growth Rate vs Warming Rate Analysis

Analyzes the relationship between economic growth rates and climate warming scenarios across income groups.

## Quick Start

```bash
pip install -r requirements.txt
python create_plots_xlsx.py
```

## Output

Running `create_plots_xlsx.py` generates:

- `data/output/growth_rates.xlsx` - Fractional annual growth rates (4 sheets by income group)
- `data/output/panel_plot.png` - 2x2 panel visualization with numerical labels (%/yr, °C/century)
- `data/output/panel_plot_scenario.png` - 2x2 panel visualization with scenario labels (SSP1-5, RCP2.6-8.5)

## Input Data

The input file `data/input/figure_data.txt` contains projected per-capita GDP values for:
- 4 income groups (All-country, High, Middle, Low)
- 6 economic scenarios (No growth, SSP1-SSP5)
- 5 warming scenarios (No warming, 2.6, 4.5, 7.0, 8.5 W/m²)

Growth rates are computed by normalizing to the "No growth, No warming" baseline, taking the 80th root, and subtracting 1.
