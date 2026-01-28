# Growth Rate vs Warming Rate Analysis

This repository analyzes the relationship between economic growth rates and climate warming scenarios across different income groups.

## Overview

The analysis examines projected per-capita GDP growth rates under various combinations of:
- **Economic growth scenarios**: SSP1-SSP5 (Shared Socioeconomic Pathways)
- **Climate warming scenarios**: 2.6, 4.5, 7.0, and 8.5 W/m² radiative forcing levels

Data is analyzed for four income groups:
- All-country average
- High-income countries
- Middle-income countries
- Low-income countries

## Installation

```bash
pip install -r requirements.txt
```

Required packages:
- numpy
- matplotlib
- pandas
- openpyxl

## Usage

### Reading and transforming data

```python
from read_data import read_figure_data, compute_growth_rates, TABLE_NAMES, ROW_LABELS, COL_LABELS

# Load raw per-capita GDP data (4 x 6 x 5 array)
data = read_figure_data("data/input/figure_data.txt")

# Transform to fractional annual growth rates
growth_rates = compute_growth_rates(data)

# Convert to percentage
percent_rates = growth_rates * 100
```

The `compute_growth_rates()` function:
1. Normalizes each income group by its "No growth, No warming" baseline
2. Takes the 80th root (for 80-year projection period)
3. Subtracts 1 to get the fractional annual growth rate

### Generating the panel plot

```bash
python plot_panels.py
```

This creates a 2x2 panel figure saved to `data/output/panel_plot.png`:
- **Top row**: GDP growth rate vs global mean warming
- **Bottom row**: GDP growth rate vs baseline economic growth rate
- **Left column**: Low-income countries
- **Right column**: High-income countries

### Exporting to Excel

The growth rates can be exported to Excel format:

```python
import pandas as pd
from read_data import read_figure_data, compute_growth_rates, TABLE_NAMES, ROW_LABELS, COL_LABELS

data = read_figure_data("data/input/figure_data.txt")
growth_rates = compute_growth_rates(data)

with pd.ExcelWriter("data/output/growth_rates.xlsx", engine="openpyxl") as writer:
    for i, table_name in enumerate(TABLE_NAMES):
        df = pd.DataFrame(growth_rates[i], index=ROW_LABELS, columns=COL_LABELS)
        df.to_excel(writer, sheet_name=table_name[:31])
```

## Data Structure

### Input data (`data/input/figure_data.txt`)
- 4 tables (income groups) x 6 rows (growth scenarios) x 5 columns (warming scenarios)
- Values represent projected per-capita GDP in 2100

### Axis mappings

**Economic scenarios (baseline growth rates)**:
| Scenario | Baseline Growth (%/yr) |
|----------|------------------------|
| SSP1     | 2.00                   |
| SSP2     | 1.62                   |
| SSP3     | 0.34                   |
| SSP4     | 1.15                   |
| SSP5     | 2.73                   |

**Warming scenarios**:
| Forcing (W/m²) | Warming (°C/century) |
|----------------|----------------------|
| 2.6            | 0.87                 |
| 4.5            | 2.27                 |
| 7.0            | 3.96                 |
| 8.5            | 5.10                 |

## Output

- `data/output/panel_plot.png` - 2x2 panel visualization
- `data/output/growth_rates.xlsx` - Growth rates in Excel format (4 sheets)
