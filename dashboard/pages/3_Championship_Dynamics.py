import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data

st.set_page_config(page_title="Championship Dynamics", page_icon="⚔️")

st.header("⚔️ Championship Dynamics")

results, _, _ = load_data()

if results is not None:
    # Select Year
    years = sorted(results['year'].unique(), reverse=True)
    selected_year = st.selectbox("Select Season", years, index=0 if 2021 not in years else years.index(2021))
    
    st.subheader(f"{selected_year} Title Battle")
    
    season_data = results[results['year'] == selected_year].copy()
    
    # Identify top 3 contenders
    top_drivers = season_data.groupby('driverId')['points'].sum().sort_values(ascending=False).head(3).index
    battle_data = season_data[season_data['driverId'].isin(top_drivers)].copy()
    
    # Sort by round
    battle_data = battle_data.sort_values('round')
    
    # Cumulative points
    battle_data['cumulative_points'] = battle_data.groupby('driverId')['points'].cumsum()
    
    # Helper to get driver name (if missing from merge issues, but should be there)
    # result csv has driver_name
    
    fig_battle = px.line(
        battle_data, 
        x='round', 
        y='cumulative_points', 
        color='driver_name', 
        markers=True,
        title=f"Points Progression: Top 3 Contenders ({selected_year})",
        labels={'cumulative_points': 'Total Points', 'round': 'Race Round'}
    )
    st.plotly_chart(fig_battle, use_container_width=True)
    
    # Gap Analysis
    st.markdown("### Momentum Swings")
    # Pivot for gap calculation if only 2 top drivers
    if len(top_drivers) >= 2:
        pivot = battle_data[battle_data['driverId'].isin(top_drivers[:2])]
        # Group by round, pivot driver names to columns
        # Pivot table: Index=round, Columns=driver_name, Values=cumulative_points
        try:
            gap_pivot = pivot.pivot(index='round', columns='driver_name', values='cumulative_points')
            d1 = gap_pivot.columns[0]
            d2 = gap_pivot.columns[1]
            gap_pivot['Gap'] = gap_pivot[d1] - gap_pivot[d2]
            
            fig_gap = px.bar(
                gap_pivot, 
                x=gap_pivot.index, 
                y='Gap',
                title=f"Points Gap: {d1} vs {d2}",
                color='Gap',
                color_continuous_scale='RdBu'
            )
            st.plotly_chart(fig_gap, use_container_width=True)
        except Exception as e:
            st.info("Could not generate gap chart (data shape complexity).")
