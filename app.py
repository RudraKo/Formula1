import streamlit as st
import pandas as pd
from utils import load_data, inject_custom_css

st.set_page_config(
    page_title="F1 Analytics Hub",
    layout="wide"
)

inject_custom_css()

st.title("Formula 1 Strategic Intelligence")

st.markdown("""
<div style="background-color: rgba(22, 26, 37, 0.8); backdrop-filter: blur(10px); padding:30px; border-radius:20px; border-left:8px solid #FF1801; margin-bottom: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.3);">
    <h3 style="margin-top:0;">Championship Analytics Platform</h3>
    <p style="color:#FAFAFA; font-size:16px;">
    Advanced telemetry analysis for Formula 1 data (1950-2020). 
    Explore driver efficiency, pit stop strategy, and championship dynamics through interactive dashboards.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

results, laps, pits = load_data()

if results is not None:
    total_races = results['raceId'].nunique()
    total_drivers = results['driverId'].nunique()
    total_laps = len(laps)

    col1.metric("Races Analyzed", total_races)
    col2.metric("Drivers Tracked", total_drivers)
    col3.metric("Data Points (Laps)", f"{total_laps:,}")

st.markdown("---")
st.subheader("Analytics Modules")

m1, m2 = st.columns(2)
with m1:
    st.markdown("""
    #### Driver Performance
    Career trajectory, consistency profiling, and reliability analysis.
    """)
    st.info("Select specific drivers to view their career metrics.")

with m2:
    st.markdown("""
    #### Strategy Analytics
    Pit stop efficiency variance and circuit-specific overtaking characteristics.
    """)
    st.info("Compare constructor performance in the Hybrid Era.")

st.markdown("---")

# Detailed Analytical Description
st.markdown("""
### About This Analytics Platform

#### What We Are Doing
This platform provides comprehensive data-driven analysis of Formula 1 racing, covering historical race data from 1950 to 2020. We transform raw telemetry and race results into actionable intelligence for understanding driver performance, team strategies, and championship dynamics.

#### What We Are Analyzing
Our analysis encompasses multiple dimensions of F1 racing:
- **Driver Metrics**: Career trajectories, consistency profiles, win rates, podium percentages, and reliability indicators
- **Team Performance**: Constructor pit stop efficiency, operational excellence, and strategic decision-making
- **Race Dynamics**: Lap-by-lap pace evolution, tire strategy effectiveness, and position changes
- **Championship Battles**: Points accumulation patterns, momentum shifts, and title fight trajectories
- **Circuit Intelligence**: Track-specific overtaking potential and racing characteristics

#### How We Are Doing It
Our methodology combines statistical analysis with data visualization:
1. **Data Processing**: Clean and normalize race results, lap times, and pit stop data from official F1 records
2. **Feature Engineering**: Calculate derived metrics like position gain, DNF rates, consistency scores, and rolling averages
3. **Aggregation**: Group data by driver, constructor, circuit, and season to identify patterns
4. **Visualization**: Use interactive Plotly charts for exploratory analysis with hover details and dynamic filtering
5. **Comparative Analysis**: Enable side-by-side comparisons across drivers, teams, and eras

#### What It Helps In
This platform enables:
- **Performance Benchmarking**: Identify top performers and quantify their advantages
- **Strategic Insights**: Understand pit stop timing, tire strategies, and operational efficiency
- **Talent Evaluation**: Assess driver consistency, reliability, and risk-taking profiles
- **Historical Context**: Compare performance across different F1 eras and regulations
- **Predictive Intelligence**: Recognize patterns that correlate with championship success
- **Fan Engagement**: Provide data-backed narratives for deeper appreciation of the sport

**Data Coverage**: 70+ years of F1 history with over 1,000 races and millions of lap time data points.
""")
