import streamlit as st
import plotly.express as px
import pandas as pd
from utils import load_data, inject_custom_css, format_fig

st.set_page_config(page_title="Championship Dynamics", layout="wide")
inject_custom_css()

st.title("Championship Dynamics")

results, _, _ = load_data()

if results is not None:
    # Select Year
    years = sorted(results['year'].unique(), reverse=True)
    selected_year = st.selectbox("Select Season", years, index=0 if 2021 not in years else years.index(2021))
    
    st.subheader(f"Title Fight Trajectory ({selected_year})")
    
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
        title=f"Points Accumulation: Top 3 Contenders",
        labels={'cumulative_points': 'Total Points', 'round': 'Race Round'}
    )
    fig_battle = format_fig(fig_battle, "Championship Progression")
    st.plotly_chart(fig_battle, use_container_width=True)
    
    # Gap Analysis
    st.subheader("Momentum Analysis")
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
                title=f"Points Delta: {d1} vs {d2}",
                color='Gap',
                color_continuous_scale='RdBu'
            )
            fig_gap = format_fig(fig_gap, "Points Delta")
            st.plotly_chart(fig_gap, use_container_width=True)
        except Exception as e:
            st.info("Could not generate gap chart (data shape complexity).")
    
    st.markdown("---")
    
    # Detailed Analytical Description
    st.markdown("""
    ### Championship Dynamics - Methodology & Insights
    
    #### What We Are Doing
    We analyze the temporal evolution of Formula 1 championship battles by tracking points accumulation and momentum shifts throughout a season. This module reveals how title fights develop, identifying critical turning points and competitive dynamics between championship contenders.
    
    #### What We Are Analyzing
    **Championship Metrics:**
    - **Cumulative Points Progression**: Race-by-race points accumulation for top contenders
    - **Points Gap Evolution**: Delta between leading drivers across the season
    - **Momentum Analysis**: Swing patterns and lead changes throughout the championship
    - **Top 3 Contender Identification**: Automatic identification of championship protagonists
    - **Race-by-Race Impact**: How individual race results influence overall standings
    - **Comparative Performance**: Side-by-side championship trajectories
    
    #### How We Are Doing It
    **Analytical Techniques:**
    1. **Season Filtering**: Select specific seasons to analyze historical championship battles
    2. **Contender Identification**: Automatically identify top 3 drivers by total season points
    3. **Cumulative Summation**: Calculate running total of points after each race round
    4. **Line Chart Visualization**: Plot championship progression with markers for each race
    5. **Gap Analysis**: Compute points delta between top 2 contenders using pivot tables
    6. **Diverging Color Scale**: Use Red-Blue color scheme to show lead changes in gap chart
    
    #### What It Helps In
    **Strategic Applications:**
    - **Championship Prediction**: Identify momentum patterns that predict eventual champions
    - **Critical Race Identification**: Pinpoint races where championship lead changed hands
    - **Pressure Analysis**: Understand how gaps affect driver psychology and team strategies
    - **Historical Comparison**: Compare current title fights with legendary past battles
    - **Strategic Planning**: Inform risk-reward decisions based on championship position
    - **Media Narrative**: Provide data-driven storylines for championship coverage
    
    **Key Insights:**
    - **Steep Upward Slopes**: Indicate dominant winning streaks
    - **Flat Sections**: Represent periods of poor performance or DNFs
    - **Crossing Lines**: Mark pivotal moments where championship lead changed
    - **Widening Gaps**: Show one driver pulling away (dominance)
    - **Narrowing Gaps**: Indicate tightening championship battle (excitement)
    - **Bar Color Changes**: Red/Blue bars show gap direction (who's ahead)
    
    **Notable Examples**: 2021 Verstappen-Hamilton, 2008 Massa-Hamilton, 2007 Raikkonen-Hamilton-Alonso
    """)
