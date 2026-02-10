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
    
    # Load background image
    try:
        bin_str = get_base64_of_bin_file("images/formula14k-1.png")
        background_image = f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{bin_str}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
        """
    except Exception:
        background_image = "" # Fallback if image missing

    st.markdown(background_image, unsafe_allow_html=True)

    st.markdown("""
    <style>
        /* F1 Font Import */
        @import url('https://fonts.googleapis.com/css2?family=Titillium+Web:wght@400;600;700&display=swap');
        
        html, body, [class*="css"]  {
            font-family: 'Titillium Web', sans-serif;
        }
        
        /* Headers */
        h1, h2, h3 {
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: #FAFAFA !important;
            font-weight: 700;
        }
        
        h1 {
            border-bottom: 3px solid #FF1801; /* Thicker accent */
            padding-bottom: 15px;
            margin-bottom: 40px;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5);
        }
        
        /* Glassmorphism Metric Cards */
        div[data-testid="metric-container"] {
            background-color: rgba(22, 26, 37, 0.7); /* Translucent */
            backdrop-filter: blur(10px); /* Glass effect */
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 25px;
            border-radius: 20px; /* Rounded Corners */
            border-left: 5px solid #FF1801;
            box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
            transition: all 0.3s ease;
        }
        
        div[data-testid="metric-container"]:hover {
            border-color: #FF1801;
            transform: translateY(-5px);
            box-shadow: 0 12px 40px 0 rgba(255, 24, 1, 0.2);
        }
        
        /* Chart Containers (Glassmorphism) */
        /* Target the parent divs of charts to give them cards */
        div[data-testid="stPlotlyChart"] {
            background-color: rgba(22, 26, 37, 0.6);
            backdrop-filter: blur(5px);
            border-radius: 20px;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.05);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
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
