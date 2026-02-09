import streamlit as st
import pandas as pd
from utils import load_data

st.set_page_config(
    page_title="F1 Analytics Hub",
    page_icon="🏎️",
    layout="wide"
)

st.title("🏎️ Formula 1 Analytics Intelligence")

st.markdown("""
### Welcome to the F1 Strategic Intelligence Dashboard.

This application provides an internship-level analysis of Formula 1 history (1950-2020), 
focusing on driver performance, race strategy, and championship dynamics.

**Key Modules:**
- **Driver Performance**: Analyze career stats, consistency, and reliability.
- **Strategy Analytics**: Deep dive into pit stops, tire pace, and circuit characteristics.
- **Championship Dynamics**: visualize title fights and momentum swings.
- **Lap Time Trends**: Granular analysis of race pace evolution.

---
""")

col1, col2, col3 = st.columns(3)

results, laps, pits = load_data()

if results is not None:
    total_races = results['raceId'].nunique()
    total_drivers = results['driverId'].nunique()
    total_laps = len(laps)

    col1.metric("Total Races Analyzed", total_races)
    col2.metric("Drivers Tracked", total_drivers)
    col3.metric("Laps Recorded", f"{total_laps:,}")

st.markdown("### Latest Insights")
st.info("💡 Navigation: Use the sidebar to explore specific analytics modules.")
