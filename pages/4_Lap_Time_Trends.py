import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data

st.set_page_config(page_title="Lap Time Trends", page_icon="⏱️")

st.header("⏱️ Lap Time Analysis")

results, laps, _ = load_data()

if results is not None and laps is not None:
    # Select Race
    # Filter for year first to reduce list
    years = sorted(results['year'].unique(), reverse=True)
    sel_year = st.sidebar.selectbox("Select Season", years, index=years.index(2021) if 2021 in years else 0)
    
    races_in_year = results[results['year'] == sel_year][['raceId', 'race_name', 'round']].drop_duplicates().sort_values('round')
    race_options = races_in_year['race_name'].tolist()
    
    sel_race_name = st.sidebar.selectbox("Select Race", race_options)
    
    # Get Race ID
    sel_race_id = races_in_year[races_in_year['race_name'] == sel_race_name]['raceId'].values[0]
    
    st.subheader(f"Pace Analysis: {sel_race_name} {sel_year}")
    
    # Get Laps for this race
    race_laps = laps[laps['raceId'] == sel_race_id].copy()
    
    # Merge driver names
    if 'driver_name' not in race_laps.columns:
        driver_map = results[['driverId', 'driver_name']].drop_duplicates()
        race_laps = pd.merge(race_laps, driver_map, on='driverId', how='left')
    
    # Select Drivers to Compare
    # Default to Top 5 finishers
    top_5_finishers = results[(results['raceId'] == sel_race_id) & (results['positionOrder'] <= 5)]['driver_name'].unique().tolist()
    all_drivers = sorted(race_laps['driver_name'].unique().tolist())
    
    sel_drivers = st.multiselect("Select Drivers", all_drivers, default=top_5_finishers[:5])
    
    if sel_drivers:
        viz_data = race_laps[race_laps['driver_name'].isin(sel_drivers)].copy()
        
        # Calculate Rolling Avg
        window = st.slider("Rolling Window (Laps)", 1, 10, 3)
        viz_data = viz_data.sort_values(['driver_name', 'lap'])
        viz_data['seconds'] = viz_data['milliseconds'] / 1000
        viz_data['rolling_pace'] = viz_data.groupby('driver_name')['seconds'].transform(lambda x: x.rolling(window).mean())
        
        # Remove outliers (pit stops? > 100s or 110% of median??)
        # Simple cap for visuals if median is around 90s, stops are +20s.
        median_pace = viz_data['seconds'].median()
        viz_data_clean = viz_data[viz_data['rolling_pace'] < median_pace * 1.3] 
        
        fig_pace = px.line(
            viz_data_clean, 
            x='lap', 
            y='rolling_pace', 
            color='driver_name',
            title=f"Race Pace Evolution (Rolling Avg {window} Laps)",
            labels={'rolling_pace': 'Lap Time (s)', 'lap': 'Lap Number'}
        )
        st.plotly_chart(fig_pace, use_container_width=True)
    else:
        st.info("Select drivers to generate chart.")
