import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, inject_custom_css, format_fig

st.set_page_config(page_title="Lap Time Trends", layout="wide")
inject_custom_css()

st.title("Lap Time Analysis")

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
    
    st.subheader(f"Pace Evolution: {sel_race_name} {sel_year}")
    
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
        fig_pace = format_fig(fig_pace, "Race Pace Strategy")
        st.plotly_chart(fig_pace, use_container_width=True)
    else:
        st.info("Select drivers to generate chart.")
    
    st.markdown("---")
    
    # Detailed Analytical Description
    st.markdown("""
    ### Lap Time Analysis - Methodology & Insights
    
    #### What We Are Doing
    We perform granular lap-by-lap performance analysis to understand race pace evolution, tire degradation patterns, and strategic timing. This module reveals how drivers manage their pace throughout a race and how strategy decisions impact competitive positioning.
    
    #### What We Are Analyzing
    **Lap-Level Metrics:**
    - **Raw Lap Times**: Individual lap completion times in milliseconds
    - **Rolling Average Pace**: Smoothed pace trends using configurable window (1-10 laps)
    - **Pace Evolution**: How lap times change throughout race distance
    - **Driver Pace Comparison**: Side-by-side pace analysis for selected drivers
    - **Outlier Detection**: Identification and filtering of pit stop laps
    - **Tire Strategy Impact**: Pace changes correlating with pit stop timing
    
    #### How We Are Doing It
    **Analytical Techniques:**
    1. **Race & Driver Selection**: Choose specific race from any season (1950-2020) and compare multiple drivers
    2. **Lap Time Conversion**: Transform milliseconds to seconds for readability
    3. **Rolling Window Smoothing**: Apply moving average (default 3 laps) to reduce noise and reveal trends
    4. **Outlier Filtering**: Remove pit stop laps (>130% of median) to focus on racing pace
    5. **Multi-Driver Overlay**: Plot pace traces for different drivers on same chart for direct comparison
    6. **Time-Series Visualization**: Use line charts to show pace evolution across race distance
    
    #### What It Helps In
    **Strategic Applications:**
    - **Tire Strategy Validation**: Identify optimal pit stop windows by analyzing pace drop-off
    - **Pace Management**: Understand tire conservation vs. push strategies
    - **Overtaking Analysis**: Correlate pace advantages with successful passing maneuvers
    - **Fuel Load Impact**: Observe pace improvement as fuel burns off during race
    - **Driver Comparison**: Benchmark race pace between teammates or rivals
    - **Strategy Simulation**: Model alternative pit stop strategies based on pace data
    
    **Key Insights:**
    - **Downward Pace Trends**: Indicate tire degradation or fuel-saving mode
    - **Upward Pace Trends**: Show improving pace (lighter fuel load, fresh tires)
    - **Sudden Pace Drops**: Mark pit stop laps or traffic interference
    - **Pace Oscillations**: Suggest aggressive push/conserve cycles
    - **Converging Lines**: Show drivers on similar pace (DRS battles)
    - **Diverging Lines**: Indicate one driver pulling away or struggling
    
    **Typical Patterns:**
    - **Stint 1**: Fast early laps as drivers push on fresh tires with heavy fuel
    - **Mid-Stint**: Gradual pace loss as tires degrade
    - **Post-Pit**: Sudden pace improvement with fresh rubber
    - **Final Laps**: Either conservation (protecting position) or all-out attack
    """)
