import streamlit as st
import pandas as pd
from utils import load_data, inject_custom_css

st.set_page_config(
    page_title="F1 Analytics Hub",
    page_icon="charts",
    layout="wide"
)

inject_custom_css()

st.title("Formula 1 Strategic Intelligence")

st.markdown("""
<div style="background-color:#161A25; padding:20px; border-radius:0px; border-left:5px solid #FF1801; margin-bottom: 20px;">
    <h3>Championship Analytics Platform</h3>
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
