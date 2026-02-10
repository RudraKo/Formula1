import pandas as pd
import numpy as np
import streamlit as st
import os

@st.cache_data
def load_data():
    """Load and process F1 datasets."""
    
    # Load clean CSVs
    try:
        results = pd.read_csv("data/clean_results.csv")
        laps = pd.read_csv("data/clean_lap_times.csv")
        pits = pd.read_csv("data/clean_pit_stops.csv")
        
        # Determine status.csv path (cache or local fallback)
        status_path = "status.csv"
        # Try finding it in typical cache loc if not local
        if not os.path.exists(status_path):
             # Hardcoded fallback or check previous paths
             pass 
        
        # If status.csv exists locally (we might copy it later or user has it), load it.
        # Otherwise, basic status map.
        # For this demo, let's create a minimal status map if missing.
        status_map = {
            1: "Finished",
            11: "+1 Lap",
            12: "+2 Laps",
            13: "+3 Laps",
            14: "+4 Laps",
            15: "+5 Laps",
            16: "+6 Laps",
            17: "+7 Laps",
            18: "+8 Laps",
            19: "+9 Laps"
        }
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")
        # Optional: Print traceback to logs
        import traceback
        print(traceback.format_exc())
        return None, None, None

    # Process Results Features
    results['position_gain'] = results['grid'] - results['positionOrder']
    results['is_win'] = (results['positionOrder'] == 1).astype(int)
    results['is_podium'] = (results['positionOrder'] <= 3).astype(int)
    
    # DNF Logic
    # If statusId is NOT in our "Finished" set (1, 11-19 typically), mark DNF.
    # Since we might not have status.csv here, let's rely on statusId heuristics for F1 dataset.
    # IDs 1, 11-19 are finished. Id 5 is Engine, 3 is Accident, etc.
    finished_ids = [1] + list(range(11, 20))
    results['is_dnf'] = results['statusId'].apply(lambda x: 0 if x in finished_ids else 1)
    
    return results, laps, pits

@st.cache_data
def get_driver_stats(results):
    """Aggregate driver career statistics."""
    stats = results.groupby(['driverId', 'driver_name']).agg(
        total_races=('raceId', 'count'),
        total_points=('points', 'sum'),
        wins=('is_win', 'sum'),
        podiums=('is_podium', 'sum'),
        dnfs=('is_dnf', 'sum'),
        avg_finish=('positionOrder', 'mean'),
        consistency=('positionOrder', 'std'),
        avg_gain=('position_gain', 'mean')
    ).reset_index()
    
    stats['win_rate'] = stats['wins'] / stats['total_races']
    stats['podium_rate'] = stats['podiums'] / stats['total_races']
    stats['dnf_rate'] = stats['dnfs'] / stats['total_races']
    stats['points_per_race'] = stats['total_points'] / stats['total_races']
    
    return stats

@st.cache_data
def get_constructor_pit_stats(pits, results):
    """Aggregate constructor pit stop performance."""
    # Ensure pits has constructor info
    if 'constructor_name' not in pits.columns:
        driver_team_map = results[['raceId', 'driverId', 'constructor_name']].drop_duplicates()
        pits = pd.merge(pits, driver_team_map, on=['raceId', 'driverId'], how='inner')
    
    # Filter for valid durations (< 40s) for pit stop speed analysis
    pits_clean = pits[pits['milliseconds'] < 40000].copy()
    pits_clean['seconds'] = pits_clean['milliseconds'] / 1000
    
    return pits_clean

import base64

def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def inject_custom_css():
    """Inject F1-themed CSS for Streamlit."""

    st.markdown("""
    <style>
        /* F1 Font Import */
        @import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@400;600;700;900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@500;700&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Titillium Web', sans-serif;
        }
        
        /* Animated Background Accent */
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
        
        @keyframes racing-stripe {
            0% { background-position: 0 0; }
            100% { background-position: 40px 0; }
        }
        
        /* Headers with Racing Aesthetic */
        h1, h2, h3 {
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: #FAFAFA !important;
            font-weight: 700;
            position: relative;
        }
        
        h1 {
            border-bottom: 4px solid #FF1801;
            padding-bottom: 15px;
            margin-bottom: 40px;
            text-shadow: 0 2px 8px rgba(255, 24, 1, 0.3);
            font-weight: 900;
        }
        
        h1::after {
            content: "";
            position: absolute;
            bottom: -8px;
            left: 0;
            width: 100px;
            height: 4px;
            background: #FFFFFF;
        }
        
        /* Enhanced Metric Cards with Animations */
        div[data-testid="metric-container"] {
            background: linear-gradient(135deg, rgba(22, 26, 37, 0.9) 0%, rgba(30, 35, 48, 0.8) 100%);
            backdrop-filter: blur(15px);
            border: 2px solid rgba(255, 255, 255, 0.1);
            padding: 30px;
            border-radius: 16px;
            border-left: 6px solid #FF1801;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }
        
        div[data-testid="metric-container"]::before {
            content: "";
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255, 24, 1, 0.1), transparent);
            transition: left 0.5s;
        }
        
        div[data-testid="metric-container"]:hover::before {
            left: 100%;
        }
        
        div[data-testid="metric-container"]:hover {
            border-color: #FF1801;
            border-left-width: 8px;
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 16px 48px 0 rgba(255, 24, 1, 0.3), inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }
        
        /* Metric Values - Bold Numbers */
        div[data-testid="stMetricValue"] {
            font-family: 'Roboto Mono', monospace !important;
            font-weight: 700 !important;
            font-size: 2.2rem !important;
            background: linear-gradient(135deg, #FFFFFF 0%, #FF1801 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        /* Enhanced Chart Containers */
        div[data-testid="stPlotlyChart"] {
            background: linear-gradient(135deg, rgba(22, 26, 37, 0.8) 0%, rgba(18, 22, 33, 0.9) 100%);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 20px;
            border: 2px solid rgba(255, 255, 255, 0.08);
            box-shadow: 0 8px 16px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255, 255, 255, 0.05);
            transition: all 0.3s ease;
            position: relative;
        }
        
        div[data-testid="stPlotlyChart"]:hover {
            border-color: rgba(255, 24, 1, 0.3);
            box-shadow: 0 12px 24px rgba(0,0,0,0.4), 0 0 20px rgba(255, 24, 1, 0.1);
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: rgba(14, 17, 23, 0.95);
            border-right: 1px solid #222;
        }
        
        /* Custom Input Widgets - Rounded & Aesthetic */
        .stSelectbox > div > div {
            background-color: rgba(22, 26, 37, 0.8);
            color: white;
            border: 1px solid #444;
            border-radius: 15px; /* Rounded */
        }
        
        .stMultiSelect > div > div {
            background-color: rgba(22, 26, 37, 0.8);
            border: 1px solid #444;
            border-radius: 15px; /* Rounded */
        }
        
        /* Sliders */
        .stSlider > div > div > div > div {
            background-color: #FF1801;
        }
        
        /* Buttons */
        button {
            border-radius: 25px !important; /* Fully Rounded Caps */
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.1em;
            border: 2px solid #FF1801;
            background-color: transparent;
            color: #FF1801;
            padding: 0.5rem 1rem;
            transition: all 0.3s ease;
        }
        
        button:hover {
            background-color: #FF1801;
            color: white;
            box-shadow: 0 0 15px rgba(255, 24, 1, 0.4);
        }
        
        /* Spacing Utilities */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 5rem;
        }
        
    </style>
    """, unsafe_allow_html=True)

def format_fig(fig, title=None):
    """Apply consistent F1 dark theme to Plotly charts."""
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Titillium Web", color="#FAFAFA"),
        title=dict(
            text=title.upper() if title else None,
            font=dict(size=20, color="#FF1801", family="Titillium Web")
        ),
        margin=dict(l=40, r=40, t=80, b=40), # More internal spacing
        hovermode="x unified",
        modebar=dict(orientation='v', bgcolor='rgba(0,0,0,0)')
    )
    # F1 Color Sequence (Red, White, Grey/Silver + Cool Accents)
    fig.update_traces(marker=dict(line=dict(width=0)))
    return fig
