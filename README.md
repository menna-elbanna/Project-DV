# ⚽ FIFA Global Football Analytics Hub

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Dash](https://img.shields.io/badge/Plotly_Dash-2.0%2B-00B4CC?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data_Processing-150458?style=for-the-badge&logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**An interactive, multi-tab data visualization dashboard built with Plotly Dash for exploring FIFA player statistics across clubs, nationalities, and positions.**

[Features](#-features) • [Screenshots](#-dashboard-preview) • [Installation](#-installation) • [Usage](#-usage) • [Project Structure](#-project-structure) • [Data Setup](#-data-setup)

</div>

---

## 📌 Overview

The **FIFA Global Football Analytics Hub** is a fully interactive web dashboard that enables deep exploration of FIFA player data. With 13 visualization modules spread across 4 analytical tabs, users can compare clubs, analyze player distributions, explore relationships between age and performance, and track trends over player career stages — all with dynamic filtering and real-time updates.

The dashboard is styled with a sleek dark holographic stadium theme, built using CSS animations and a custom design system.

---

## ✨ Features

### 🧮 4 Analytical Tabs

| Tab | Description |
|-----|-------------|
| **Comparison** | Compare top clubs and players using column, bar, stacked, and clustered charts |
| **Relationship** | Explore correlations between age, overall rating, market value, and potential |
| **Distribution** | Analyze age, wage, and rating distributions via histograms, box plots, and violin charts |
| **Time Series** | Track how player ratings and position compositions evolve across age groups |

### 📊 13 Visualization Modules

- **Column Chart** —> Top N clubs by average overall rating (winner highlighted, leftmost)
- **Horizontal Bar Chart** —> Top N elite players ranked by overall rating
- **Stacked Column Chart** —> Position depth per club (Forward / Midfielder / Defender / GK)
- **Stacked Bar Chart** —> Nationality mix across top clubs
- **Clustered Column Chart** —> Players by position group and rating band
- **Clustered Bar Chart** —> Average wage vs average overall rating (normalized comparison)
- **Scatter Chart** —> Age vs Overall Rating with outlier detection and player labeling
- **Bubble Chart** —> Age vs Potential, bubble size = market value (€)
- **Histogram** —> Age distribution by position group
- **Box Plot** —> Wage distribution across all player positions
- **Violin Chart** —> Overall rating or wage density by position group with median annotations
- **Line Chart** —> Mean overall rating across age with optional 5-age and 10-age moving averages
- **Area Chart (simple + stacked)** —> Player count volume and position composition by age

### ⚙️ Interactive Controls

- **Top N Slider** — Adjust how many clubs/players appear in comparison charts (5–20)
- **Filter by Club or Country** — Scope relationship and time series views to a specific team or nation
- **Age Range Slider** — Narrow analysis to a specific player career window
- **Position Group Filter** — Focus distribution charts on Forwards, Midfielders, Defenders, or Goalkeepers
- **Moving Average Toggle** — Switch between raw data, 5-age MA, 10-age MA, or both
- **Metric Selector** — Toggle between Overall Rating and Wage (€) in distribution views

---

## 🖥️ Dashboard Preview

> The dashboard features a dark holographic stadium background with animated radar sweeps, a pitch grid overlay, and glowing KPI cards. Charts follow a consistent design system: black borders, zero-baseline Y-axes, horizontal labels, and legends inside the top-right corner.

### KPI Header
- **Total players loaded** from the dataset
- **Age window** (min–max)
- **Number of position groups** analyzed

---

## 🗂️ Project Structure

```
Project-DV/
├── dashboard (3).py       # Main Dash application — all tabs, charts, and callbacks
├── requirements.txt       # Python dependencies
├── assets/
│   └── style.css          # Custom dark theme with stadium hologram animations
└── data/                  # (Not included — see Data Setup below)
    ├── cleaned_data.csv    # Full preprocessed dataset (primary)
    └── sample_cleaned_data.csv  # Lightweight fallback sample
```

---

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- pip

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/your-username/fifa-analytics-dashboard.git
cd fifa-analytics-dashboard

# 2. (Optional) Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

**`requirements.txt`**
```
pandas
plotly
dash
nbformat>=4.2.0
ipykernel
```

---

## 🗄️ Data Setup

> ⚠️ The data files are **not included** in this repository due to their large size. Follow these steps to prepare your local data.

### Option A — Full Dataset (Recommended)

1. Download the FIFA dataset (the raw `male_players.csv` file).
2. Place it in the `data/` folder:
   ```
   Project-DV/data/male_players.csv
   ```
3. Run the preprocessing notebook to generate the cleaned file:
   ```bash
   jupyter notebook preprocessing.ipynb
   ```
4. This produces `data/cleaned_data.csv`, which the dashboard will load automatically.

### Option B — Sample Dataset (Quick Start)

If you only want to test the dashboard without the full dataset, place a smaller CSV named `sample_cleaned_data.csv` in the `data/` folder. The app will fall back to it automatically when `cleaned_data.csv` is not found.

### Required Columns

The CSV must contain these columns:

| Column | Type | Description |
|--------|------|-------------|
| `short_name` | string | Player display name |
| `age` | int | Player age |
| `nationality_name` | string | Player nationality |
| `overall` | int | Overall rating (0–100) |
| `potential` | int | Potential rating (0–100) |
| `club_name` | string | Current club |
| `player_positions` | string | Comma-separated positions (e.g., `ST, CF`) |
| `wage_eur` | float | Weekly wage in EUR |
| `value_eur` | float | Market value in EUR |

> The app automatically derives `position_group` (Forward / Midfielder / Defender / Goalkeeper) from `player_positions` at load time.

---

## 🚀 Usage

```bash
# Run the dashboard
python "dashboard (3).py"
```

Then open your browser and navigate to:
```
http://127.0.0.1:8050/
```

### Environment Variable

You can control the maximum number of rows loaded (default: 500,000):

```bash
# Linux / macOS
export FIFA_DASH_MAX_ROWS=200000
python "dashboard (3).py"

# Windows
set FIFA_DASH_MAX_ROWS=200000
python "dashboard (3).py"
```

---

## 🏗️ Architecture

### Data Loading Pipeline

```
male_players.csv
      │
      ▼
Chunk-based reading (200k rows/chunk)
      │
      ▼
Column filtering → 9 essential columns
      │
      ▼
Type casting + null handling
      │
      ▼
Position mapping (ST/LW/CF → Forward, etc.)
      │
      ├──► Full DataFrame (DF)         — used for aggregation & comparison
      └──► Sampled DataFrame (5,000)   — used for scatter / violin / box plots
```

### Callback Architecture

Each tab has independent Dash callbacks triggered by its own set of controls:

- **Tab 1 (Comparison):** `cmp-topn` + `cmp-metric` → 6 chart outputs
- **Tab 2 (Relationship):** `rel-ftype` + `rel-fval` + `rel-age` → 2 chart outputs
- **Tab 3 (Distribution):** `dist-pos` + `dist-metric` → 3 chart outputs
- **Tab 4 (Time Series):** `ts-ftype` + `ts-fval` + `ts-age` + `ts-ma-type` → 3 chart outputs

---

## 🎨 Design System

All charts follow a consistent set of visual rules:

| Rule | Implementation |
|------|---------------|
| Black border frame | `shapes` rect overlay on every figure |
| Y-axis starts at 0 | `rangemode="tozero"` |
| Horizontal axis labels | `tickangle=0` |
| Magnitudes outside bars | `textposition="outside"` |
| Legend inside top-right | `x=0.98, y=0.98, xanchor="right"` |
| Winner/highest highlighted | `lightgreen` marker on top-performing bar |
| Consistent palette | Monochromatic teals, blues, oranges, purples per chart family |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-chart`
3. Commit your changes: `git commit -m "Add: new correlation chart for Tab 2"`
4. Push to the branch: `git push origin feature/new-chart`
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

## 🙏 Acknowledgements

- **[Plotly Dash](https://dash.plotly.com/)** — reactive web framework for Python
- **[Plotly Express & Graph Objects](https://plotly.com/python/)** — interactive chart library
- **[Pandas](https://pandas.pydata.org/)** — data manipulation and analysis
- FIFA dataset sourced from public sports data repositories

---

<div align="center">
  <sub>Built with ⚽ and Python</sub>
</div>
