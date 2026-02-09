# F1 Analysis Notebooks

This folder contains Jupyter notebooks for comprehensive Formula 1 data analysis (1950-2020).

## Notebooks Overview

### 1. `data_prep.ipynb` - Data Preparation Pipeline

**Run this first!**

#### What it does:

- Downloads F1 dataset from Kaggle
- Cleans and standardizes 8 key tables
- Merges related information
- Exports clean CSV files to `../data/`

#### Outputs:

- `../data/clean_results.csv` (~26,000 rows)
- `../data/clean_lap_times.csv` (~500,000+ rows)
- `../data/clean_pit_stops.csv` (~9,000+ rows)

#### Key Sections:

1. Load raw data from Kaggle
2. Clean and standardize data
3. Merge related tables
4. Export analysis-ready files

---

### 2. `driver_analytics.ipynb` - Driver Performance Analysis

**Requires data from `data_prep.ipynb`**

#### What it analyzes:

- Career statistics for all F1 drivers
- Win rates and podium frequencies
- Consistency and reliability metrics
- DNF (Did Not Finish) patterns

#### Outputs:

- 4 visualizations in `charts/`:
  - Top 10 drivers by career points
  - Consistency analysis (boxplot)
  - Win rate vs DNF rate scatter
  - Podium frequency rankings
- Intelligence report: `../reports/driver_intelligence_report.md`

#### Key Sections:

1. Load prepared data
2. Feature engineering (create performance metrics)
3. Compute career statistics
4. Generate visualizations
5. Create intelligence report

---

### 3. `strategy_analytics.ipynb` - Race Strategy Analysis

**Requires data from `data_prep.ipynb`**

#### What it analyzes:

- Lap-by-lap pace evolution (tire degradation)
- Pit stop performance by team
- Circuit overtaking potential
- Championship battle dynamics

#### Outputs:

- 4 visualizations in `charts/`:
  - Lap pace evolution trace
  - Team pit stop performance comparison
  - Circuit overtaking rankings
  - Championship points progression
- Strategy report: `../reports/strategy_intelligence_report.md`

#### Key Sections:

1. Load prepared data
2. Analyze lap pace evolution
3. Evaluate pit stop performance
4. Rank circuit overtaking potential
5. Visualize championship battles

---

## Getting Started

### Prerequisites

```bash
# Install required packages
pip install pandas numpy matplotlib seaborn kagglehub
```

### Running the Notebooks

1. **First time setup:**

   ```bash
   # Open data preparation notebook
   jupyter notebook data_prep.ipynb
   # Run all cells to download and prepare data
   ```

2. **Run analysis:**

   ```bash
   # Open driver analytics
   jupyter notebook driver_analytics.ipynb

   # Or open strategy analytics
   jupyter notebook strategy_analytics.ipynb
   ```

3. **View results:**
   - Charts: `../charts/` folder
   - Reports: `../reports/` folder

---

## Descriptive Features

Each notebook includes:

### Detailed Markdown Explanations

- Overview of what each section does
- Why certain approaches are used
- What to look for in the results

### Key Metrics Explained

- Formulas and calculations documented
- Interpretation guidelines
- Strategic insights

### Visualization Context

- What each chart shows
- How to read the visualizations
- What patterns to look for

### Summary Sections

- What was accomplished
- Key outputs and their locations
- Next steps and further analysis ideas

---

## Project Structure

```
F1Project/
│
├── notebooks/               ← You are here
│   ├── data_prep.ipynb
│   ├── driver_analytics.ipynb
│   └── strategy_analytics.ipynb
│
├── data/                    ← Clean datasets
│   ├── clean_results.csv
│   ├── clean_lap_times.csv
│   └── clean_pit_stops.csv
│
├── charts/                  ← Generated visualizations
│
├── reports/                 ← Markdown reports
│
└── dashboard/              ← Streamlit web dashboard
```

---

## Tips for Use

1. **Run notebooks in order:** `data_prep.ipynb` → analysis notebooks
2. **Read markdown cells:** They explain what's happening and why
3. **Modify parameters:** Change years, drivers, circuits to explore different aspects
4. **Experiment:** Add your own analysis cells to explore further

---

## Learning Features

Each notebook is designed to be:

- **Educational**: Detailed explanations of concepts
- **Reproducible**: Clear step-by-step process
- **Extensible**: Easy to add your own analysis
- **Professional**: Industry-standard practices

Perfect for:

- Data science students
- F1 enthusiasts learning data analysis
- Analytics portfolio projects
- Understanding sports analytics workflows
