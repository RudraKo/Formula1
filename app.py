import streamlit as st
import pandas as pd
from utils import load_data, inject_custom_css

st.set_page_config(
    page_title="F1 Analytics Hub",
    page_icon="🏎️",
    layout="wide"
)

inject_custom_css()

st.title("🏎️ Formula 1 Analytics Intelligence")

st.markdown("""
<div style="background-color:#161A25; padding:20px; border-radius:10px; border-left:5px solid #FF1801; margin-bottom: 20px;">
    <h3>Welcome to the F1 Strategic Intelligence Dashboard</h3>
    <p style="color:#FAFAFA; font-size:16px;">
    An advanced analytics platform processing 70+ years of Formula 1 data. 
    Explore driver performance, race strategy, and championship dynamics through interactive telemetry-style visualizations.
    </p>
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

results, laps, pits = load_data()

if results is not None:
    total_races = results['raceId'].nunique()
    total_drivers = results['driverId'].nunique()
    total_laps = len(laps)

    col1.metric("🏁 Total Races Analyzed", total_races)
    col2.metric("🏎️ Drivers Tracked", total_drivers)
    col3.metric("⏱️ Laps Recorded", f"{total_laps:,}")

st.markdown("---")
st.subheader("📊 Analytics Modules")

m1, m2 = st.columns(2)
with m1:
    st.markdown("""
    #### 🏆 Driver Performance
    Deep dive into career stats, consistency, and reliability metrics for every driver in F1 history.
    """)
    st.info("Select specific drivers to view their career trajectory.")

with m2:
    st.markdown("""
    #### 🛠️ Strategy Analytics
    Analyze pit stop efficiency, tire degradation, and circuit characteristics to understand the winning edge.
    """)
    st.info("Compare team pit stop times in the Hybrid Era.")
