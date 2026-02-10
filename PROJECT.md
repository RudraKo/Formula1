# Formula 1 Strategic Intelligence Platform - Project Documentation

## Project Overview

This project is a comprehensive data analytics platform for Formula 1 racing, built to demonstrate advanced data science, visualization, and web development skills. The platform transforms 70+ years of F1 historical data (1950-2020) into actionable intelligence through interactive dashboards and analytical notebooks.

**Live Platform**: Streamlit Dashboard  
**Data Coverage**: 1000+ races, millions of lap times, comprehensive pit stop records  
**Tech Stack**: Python, Streamlit, Plotly, Pandas, NumPy

---

## Table of Contents
1. [What We Built and Why](#what-we-built-and-why)
2. [Project Architecture](#project-architecture)
3. [Notebooks - Showcasing Analytical Skills](#notebooks---showcasing-analytical-skills)
4. [Dashboard Development](#dashboard-development)
5. [Problems Faced and Solutions](#problems-faced-and-solutions)
6. [Streamlit Customization Journey](#streamlit-customization-journey)
7. [Design Decisions](#design-decisions)
8. [Key Learnings](#key-learnings)

---

## What We Built and Why

### The Dual Approach

We built this project with two complementary components:

#### 1. **Analytical Notebooks** (Skill Showcase)
**Purpose**: Demonstrate data science proficiency to potential employers and collaborators

**Notebooks Created**:
- `driver_analytics.ipynb` - Driver performance profiling and career analysis
- `lap_time_analysis.ipynb` - Race pace evolution and tire strategy
- `strategy_analytics.ipynb` - Pit stop efficiency and circuit intelligence
- `data_prep.ipynb` - Data cleaning and feature engineering

**Why Notebooks?**
- Show raw analytical thinking and problem-solving approach
- Demonstrate proficiency with Pandas, NumPy, Matplotlib, Seaborn
- Provide reproducible analysis that others can learn from
- Serve as a portfolio piece for data science interviews

#### 2. **Interactive Dashboard** (Product Delivery)
**Purpose**: Deliver insights in an accessible, user-friendly format for non-technical stakeholders

**Dashboard Features**:
- Main landing page with overview metrics
- 4 specialized analysis pages (Driver Performance, Championship Dynamics, Lap Time Trends, Strategy Analytics)
- Interactive filtering, dynamic visualizations, real-time data exploration

**Why Dashboard?**
- Demonstrate full-stack data science skills (analysis + deployment)
- Show ability to translate technical work into business value
- Create a shareable, deployable product
- Practice web development and UI/UX design

---

## Project Architecture

```
F1Project/
├── app.py                      # Main dashboard entry point
├── utils.py                    # Shared utilities and styling
├── team_colors.py              # F1 team color mappings
├── requirements.txt            # Python dependencies
├── runtime.txt                 # Python version for deployment
│
├── pages/                      # Multi-page dashboard
│   ├── Driver_Performance.py
│   ├── Championship_Dynamics.py
│   ├── Lap_Time_Trends.py
│   └── Strategy_Analytics.py
│
├── notebooks/                  # Analytical notebooks
│   ├── driver_analytics.ipynb
│   ├── lap_time_analysis.ipynb
│   ├── strategy_analytics.ipynb
│   └── data_prep.ipynb
│
├── scripts/                    # Reusable analysis scripts
│   ├── driver_analytics.py
│   ├── data_prep.py
│   └── strategy_analytics.py
│
├── data/                       # Cleaned datasets
│   ├── clean_results.csv
│   ├── clean_lap_times.csv
│   └── clean_pit_stops.csv
│
├── images/                     # Generated visualizations
│   └── various .png charts
│
├── reports/                    # Generated insights
│
└── .streamlit/                 # Streamlit configuration
    └── config.toml
```

---

## Notebooks - Showcasing Analytical Skills

### Notebook Development Philosophy

Each notebook was designed to showcase specific data science competencies:

#### `driver_analytics.ipynb`
**Skills Demonstrated**:
- Groupby aggregations (sum, mean, std)
- Feature engineering (win_rate, podium_rate, DNF_rate)
- Multi-dimensional scatter plots with bubble sizing
- Box plot distributions for consistency analysis
- Statistical correlation analysis

**Key Analyses**:
- Career efficiency matrix (points vs wins)
- Consistency profiling via position variance
- Risk-reward driver categorization (DNF vs win rate)

#### `lap_time_analysis.ipynb`
**Skills Demonstrated**:
- Time-series data manipulation
- Rolling window calculations for smoothing
- Outlier detection and filtering
- Multi-driver comparative analysis
- Race strategy inference from pace patterns

**Key Analyses**:
- Lap-by-lap pace evolution
- Tire degradation quantification
- Pit stop timing optimization

#### `strategy_analytics.ipynb`
**Skills Demonstrated**:
- Box plot distributions (pit stop efficiency)
- Circuit-specific aggregations
- Team benchmarking methodologies
- Horizontal bar charts for ranked comparisons

**Key Analyses**:
- Team operational efficiency (pit stops)
- Circuit overtaking potential ranking
- Qualifying vs race importance by track

#### `data_prep.ipynb`
**Skills Demonstrated**:
- Data cleaning and validation
- Handling missing values
- Feature engineering (position_gain, is_win, is_podium, is_dnf)
- Data type conversions
- Merge operations across multiple datasets

**Process**:
- Loaded raw F1 datasets
- Cleaned race results, lap times, pit stops
- Created derived metrics
- Saved clean CSVs for dashboard consumption

---

## Dashboard Development

### Main Dashboard (`app.py`)

**Purpose**: Provide overview and navigation hub

**Features Implemented**:
- Page configuration (wide layout, custom title, emoji icon)
- Custom CSS injection for F1 theme
- Summary metrics (total races, drivers, lap data points)
- Module descriptions with info cards
- Comprehensive platform description

**Code Highlights**:
```python
st.set_page_config(
    page_title="F1 Analytics Hub",
    page_icon="🏎️",
    layout="wide"
)
inject_custom_css()  # Custom F1 racing theme
```

### Page 1: Driver Performance (`pages/Driver_Performance.py`)

**Analytics Implemented**:
- Career efficiency scatter plot (points vs wins, sized by win rate)
- Consistency box plots (finish position distribution)
- Risk-reward matrix (DNF rate vs win rate)

**Interactive Controls**:
- Minimum races slider (10-100) for filtering statistical significance
- Top N drivers selector for consistency analysis

**Visualization Techniques**:
- Bubble charts with color gradients
- Box plots with outlier detection
- Scatter plots with text labels for top performers

### Page 2: Championship Dynamics (`pages/Championship_Dynamics.py`)

**Analytics Implemented**:
- Cumulative points progression for top 3 contenders
- Points gap evolution (delta chart between top 2)

**Interactive Controls**:
- Season selector dropdown
- Automatic top 3 identification

**Technical Challenges Solved**:
- Dynamic pivot table creation for gap calculation
- Handling seasons with varying numbers of contenders
- Color-coded diverging scale for lead changes

### Page 3: Lap Time Trends (`pages/Lap_Time_Trends.py`)

**Analytics Implemented**:
- Rolling average lap pace calculation
- Multi-driver pace comparison
- Outlier filtering (pit stops)

**Interactive Controls**:
- Season selector
- Race selector (filtered by season)
- Multi-driver selector (defaults to top 5 finishers)
- Rolling window slider (1-10 laps)

**Data Processing**:
- Milliseconds to seconds conversion
- Rolling average computation
- Median-based outlier removal (>130% of median)

### Page 4: Strategy Analytics (`pages/Strategy_Analytics.py`)

**Analytics Implemented**:
- Pit stop efficiency box plots by team (2014-2020 Hybrid Era)
- Circuit overtaking index ranking

**Tab Organization**:
- Tab 1: Pit Stop Efficiency
- Tab 2: Circuit Overtaking

**Statistical Methods**:
- Box plot distributions (median, quartiles, outliers)
- Absolute position change averaging
- Minimum race frequency filtering (10+ races)

---

## Problems Faced and Solutions

### Problem 1: Background Image Upload Issues
**Issue**: JPEG background image wouldn't load properly on deployed dashboard

**Root Cause**: 
- Image not committed to Git repository
- File format compatibility issues

**Solution**:
- Converted JPEG to PNG format
- Properly committed image to Git
- Updated `utils.py` to reference new image path
- Eventually removed background completely for better text readability

**Code Change**:
```python
# Before (broken)
bin_str = get_base64_of_bin_file("images/PHOTO-2026-02-09-22-01-06.jpg")

# After (working)
bin_str = get_base64_of_bin_file("images/formula14k-1.png")

# Final (removed for clarity)
# Removed background image entirely
```

### Problem 2: Icon Rendering Bug
**Issue**: Page icons showing "keyboard_double" text instead of icons

**Root Cause**: Invalid icon string format (`page_icon="charts"`)

**Solution**: 
- Replaced invalid string with proper emoji icons
- Used Unicode emojis for cross-platform compatibility

**Code Change**:
```python
# Before
st.set_page_config(page_icon="charts")

# After - Different emojis for each page
st.set_page_config(page_icon="🏎️")  # Main page
st.set_page_config(page_icon="🏆")  # Championship
st.set_page_config(page_icon="👤")  # Driver Performance
st.set_page_config(page_icon="⏱️")  # Lap Times
st.set_page_config(page_icon="📊")  # Strategy
```

### Problem 3: Text Readability Against Background
**Issue**: Custom teal font color and background image made text hard to read

**Root Cause**: 
- Poor contrast between background and text
- Overly aggressive styling changes

**Solution**:
- Reverted all text to white (#FAFAFA)
- Removed background image
- Focused on clean, professional design
- Kept dark theme for better contrast

### Problem 4: Status DNF Calculation
**Issue**: Need to distinguish between finished and DNF results

**Root Cause**: Missing `status.csv` reference file

**Solution**:
- Created hardcoded status ID mapping in `utils.py`
- Finished races: statusId 1, 11-19
- DNF: All other statusIds
- Calculated `is_dnf` flag for reliability analysis

**Code Implementation**:
```python
finished_ids = [1] + list(range(11, 20))
results['is_dnf'] = results['statusId'].apply(
    lambda x: 0 if x in finished_ids else 1
)
```

### Problem 5: Dashboard Looking Too "Basic"
**Issue**: Initial dashboard looked plain and unengaging

**Root Cause**: Lack of visual polish and professional styling

**Solution**: Implemented comprehensive styling enhancements
- Added animated racing stripe header
- Enhanced metric card hover effects
- Gradient backgrounds and glassmorphism
- Monospace fonts for numbers
- Racing-themed color scheme

---

## Streamlit Customization Journey

### Phase 1: Basic Configuration (`.streamlit/config.toml`)

**Initial Setup**:
```toml
[theme]
primaryColor = "#FF1801"        # F1 Red
backgroundColor = "#0E1117"      # Dark background
secondaryBackgroundColor = "#161A25"
textColor = "#FAFAFA"            # Off-white
font = "sans serif"
```

**Decision Rationale**:
- F1 Red (#FF1801) as primary for brand recognition
- Dark theme for premium, modern aesthetic
- High contrast for readability

### Phase 2: Custom CSS Injection (`utils.py`)

**Typography Choices**:
- **Titillium Web**: Primary font - modern, clean, professional
- **Roboto Mono**: Numbers and metrics - technical, precise feel

**Import Decision**:
```python
@import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@400;600;700;900&display=swap');
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@500;700&display=swap');
```

### Phase 3: Racing-Themed Elements

#### Animated Racing Stripe
**Decision**: Add visual motion to convey speed and racing

```css
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, #FF1801 0%, #FF1801 50%, #FFFFFF 50%, #FFFFFF 100%);
    background-size: 40px 4px;
    animation: racing-stripe 2s linear infinite;
    z-index: 999;
}
```

**Why**: Creates dynamic, racing-inspired visual without being distracting

#### Enhanced Metric Cards
**Decision**: Add depth, interactivity, and premium feel

**Key Features**:
- Gradient backgrounds for depth
- Hover animations (lift, scale, shine effect)
- Thicker left border accent
- Backdrop blur for glassmorphism

```css
div[data-testid="metric-container"]:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 16px 48px 0 rgba(255, 24, 1, 0.3);
}
```

**Why**: Makes dashboard feel interactive and polished

#### Gradient Text for Numbers
**Decision**: Make metric values stand out visually

```css
div[data-testid="stMetricValue"] {
    font-family: 'Roboto Mono', monospace !important;
    background: linear-gradient(135deg, #FFFFFF 0%, #FF1801 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
```

**Why**: Numbers are most important - gradient draws attention

### Phase 4: Team Color System (`team_colors.py`)

**Decision**: Create reusable color mapping for future enhancements

**Purpose**:
- Enable team-colored charts
- Consistent color usage across visualizations
- Professional F1 brand alignment

**Implementation**:
```python
TEAM_COLORS = {
    'Mercedes': '#00D2BE',
    'Ferrari': '#DC0000',
    'Red Bull': '#1E41FF',
    'McLaren': '#FF8700',
    # ... 20+ teams
}
```

**Why**: Preparation for future chart enhancements with team branding

---

## Design Decisions

### Decision 1: Multi-Page vs Single-Page Dashboard
**Choice**: Multi-page architecture

**Rationale**:
- Cleaner organization (each analysis gets dedicated space)
- Better performance (load only needed data)
- Easier navigation for users
- Streamlit's native multi-page support

**Implementation**: Used `pages/` directory structure

---

### Decision 2: Plotly vs Matplotlib
**Choice**: Plotly for dashboard, both for notebooks

**Rationale**:
- Plotly: Interactive tooltips, zoom, pan (better UX)
- Matplotlib: Better for static notebook exports
- Plotly integrates seamlessly with Streamlit

**Code Pattern**:
```python
fig = px.scatter(data, x='col1', y='col2')
fig = format_fig(fig, "Title")  # Custom F1 theme
st.plotly_chart(fig, use_container_width=True)
```

---

### Decision 3: Data Caching Strategy
**Choice**: Aggressive caching with `@st.cache_data`

**Rationale**:
- CSV loading is expensive (millions of rows)
- Data doesn't change during session
- Dramatically improves performance

**Implementation**:
```python
@st.cache_data
def load_data():
    results = pd.read_csv("data/clean_results.csv")
    laps = pd.read_csv("data/clean_lap_times.csv")
    pits = pd.read_csv("data/clean_pit_stops.csv")
    return results, laps, pits
```

---

### Decision 4: Feature Engineering Location
**Choice**: Pre-compute features in notebooks, save to CSV

**Alternative Considered**: Calculate on-the-fly in dashboard

**Rationale**:
- Faster dashboard load times
- Separation of concerns (analysis vs presentation)
- Reusable clean datasets

**Features Pre-Computed**:
- `position_gain`, `is_win`, `is_podium`, `is_dnf`
- Merged driver/constructor names

---

### Decision 5: Detailed Descriptions
**Choice**: Add comprehensive methodology sections to all pages

**Rationale**:
- Educational value for users
- Demonstrates analytical thinking
- Provides context for interpretation
- Makes platform suitable for learning

**Structure**:
- What We Are Doing
- What We Are Analyzing
- How We Are Doing It
- What It Helps In

---

## Key Learnings

### Technical Learnings

1. **Streamlit Quirks**:
   - Icons must be emojis or material icon names (not arbitrary strings)
   - Custom CSS requires `unsafe_allow_html=True`
   - Multi-page apps auto-discover files in `pages/` directory
   - Page config must be first Streamlit command

2. **Data Processing**:
   - Feature engineering upfront saves computation time
   - Caching is critical for large datasets
   - Outlier filtering improves visualization clarity
   - Rolling averages smooth noisy time-series data

3. **Visualization**:
   - Color choice dramatically affects readability
   - Hover tooltips are essential for interactive charts
   - Limiting data points (top N) improves clarity
   - Consistent theming across charts creates professional look

### Design Learnings

1. **Less is More**:
   - Removed background image when it hurt readability
   - Simple white text often beats fancy gradients
   - Clean layouts > decorative elements

2. **Animation Balance**:
   - Subtle animations feel premium
   - Excessive motion is distracting
   - Hover effects should enhance, not overwhelm

3. **Context is King**:
   - Descriptions make analytics accessible
   - Users need to know WHY metrics matter
   - Interpretation guides add immense value

### Project Management Learnings

1. **Dual Strategy**:
   - Notebooks show <skill>, dashboards show ability to <deliver>
   - Both are needed for complete portfolio

2. **Iterative Refinement**:
   - First version was functional but ugly
   - Multiple styling iterations to find balance
   - User feedback led to description additions

3. **Documentation Matters**:
   - This PROJECT.md file captures entire journey
   - Future employers/collaborators need context
   - Explaining decisions is as important as making them

---

## Future Enhancements

**Potential Additions**:
1. Team-colored charts using `team_colors.py`
2. Predictive modeling (championship winner prediction)
3. Driver comparison tool (head-to-head analysis)
4. Download reports as PDF
5. Real-time data integration (post-2020 seasons)
6. Circuit map visualizations
7. Weather impact analysis
8. Race simulation tool

---

## Conclusion

This F1 Strategic Intelligence Platform represents a complete data science project lifecycle:

- **Data Engineering**: Cleaned and processed raw F1 data
- **Exploratory Analysis**: Created analytical notebooks
- **Feature Engineering**: Derived meaningful metrics
- **Visualization**: Built interactive Plotly charts
- **Web Development**: Deployed Streamlit dashboard
- **UI/UX Design**: Customized styling for premium feel
- **Documentation**: Comprehensive descriptions and methodology

**Skills Demonstrated**:
- Python (Pandas, NumPy, Plotly)
- Data cleaning and feature engineering
- Statistical analysis and visualization
- Web development (Streamlit, HTML, CSS)
- UI/UX design
- Product thinking (user needs, accessibility)
- Project documentation

**Outcome**: A portfolio-ready project showcasing both technical depth and product delivery capability.

---

**Project Repository**: https://github.com/RudraKo/Formula1  
**Live Dashboard**: https://formula1-aaolmtqkkw4kw2eusbdfav.streamlit.app/  
**Author**: Punarvashu  
**Last Updated**: February 2026
