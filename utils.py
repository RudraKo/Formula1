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
