import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, get_driver_stats, inject_custom_css, format_fig

st.set_page_config(page_title="Driver Performance", layout="wide")
inject_custom_css()

st.title("Driver Performance Analytics")

results, _, _ = load_data()

if results is not None:
    # career stats
    stats = get_driver_stats(results)
    
    # Filter for active drivers (min races)
    min_races = st.sidebar.slider("Minimum Races", 10, 100, 50)
    active_stats = stats[stats['total_races'] >= min_races].copy()
    
    # 1. Career Points vs Wins Scatter
    st.subheader("Career Matrix: Wins vs Points")
    fig_scatter = px.scatter(
        active_stats, 
        x='total_points', 
        y='wins', 
        size='win_rate',
        hover_name='driver_name',
        color='win_rate',
        color_continuous_scale='Reds',
        title=f"Career Efficiency Projection (> {min_races} Races)",
        labels={'total_points': 'Total Points', 'wins': 'Career Wins'}
    )
    fig_scatter = format_fig(fig_scatter, "Efficiency Matrix")
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # 2. Consistency Analysis
    st.subheader("Consistency Profiling (Position Variance)")
    
    top_n = st.slider("Select Top N Drivers", 5, 20, 10)
    top_drivers = active_stats.sort_values('total_points', ascending=False).head(top_n)
    
    # Get all finish positions for these drivers
    driver_finishes = results[results['driverId'].isin(top_drivers['driverId'])]
    
    fig_box = px.box(
        driver_finishes, 
        x='driver_name', 
        y='positionOrder',
        color='driver_name',
        title=f"Finish Position Distribution (Top {top_n})",
        labels={'positionOrder': 'Finish Position'}
    )
    fig_box.update_layout(showlegend=False)
    fig_box = format_fig(fig_box, "Consistency Distribution")
    st.plotly_chart(fig_box, use_container_width=True)
    
    # 3. Win vs DNF Tradeoff
    st.subheader("Reliability Analysis")
    fig_risk = px.scatter(
        active_stats, 
        x='dnf_rate', 
        y='win_rate', 
        size='total_races',
        hover_name='driver_name',
        text='driver_name', # Labels might clutter if too many
        title="Win Rate vs DNF Rate"
    )
    # Only label top performers to avoid clutter
    fig_risk.update_traces(textposition='top center')
    fig_risk = format_fig(fig_risk, "Reliability vs Performance")
    st.plotly_chart(fig_risk, use_container_width=True)

    st.markdown("### Strategic Insights")
    st.info(f"**Consistency**: Narrower box plots indicate higher consistency (lower variance).")
    st.info(f"**Outliers**: Drivers in the top-right quadrant of the scatter plot represent high-risk, high-reward profiles.")
    
    st.markdown("---")
    
    # Detailed Analytical Description
    st.markdown("""
    ### Driver Performance Analytics - Methodology & Insights
    
    #### What We Are Doing
    We conduct comprehensive career performance profiling for Formula 1 drivers using multi-dimensional statistical analysis. This module quantifies driver excellence beyond simple win counts by examining consistency, reliability, and competitive positioning.
    
    #### What We Are Analyzing
    **Key Performance Metrics:**
    - **Career Efficiency**: Total points accumulated vs. race wins ratio to measure scoring consistency
    - **Win Rate**: Percentage of races won - the ultimate performance indicator
    - **Podium Rate**: Top-3 finish frequency - measures consistent competitiveness
    - **DNF Rate**: Did Not Finish percentage - reliability and risk management indicator
    - **Position Variance**: Standard deviation of finish positions - consistency profiling
    - **Average Finish**: Mean finishing position across all races
    - **Position Gain**: Average improvement from grid position to race finish
    
    #### How We Are Doing It
    **Analytical Techniques:**
    1. **Scatter Plot Analysis**: Correlate total points with wins, sized by win rate, to identify efficiency patterns
    2. **Box Plot Distribution**: Visualize finish position variance to assess consistency and identify outliers
    3. **Risk-Reward Matrix**: Plot DNF rate vs. win rate to categorize driving styles
    4. **Minimum Race Filtering**: Apply configurable race threshold (10-100 races) to ensure statistical significance
    5. **Aggregation Functions**: Calculate sum, mean, and standard deviation across career performances
    
    #### What It Helps In
    **Strategic Applications:**
    - **Talent Scouting**: Identify drivers with high consistency and low DNF rates for team recruitment
    - **Driver Comparison**: Benchmark current drivers against historical legends using normalized metrics
    - **Style Profiling**: Distinguish between aggressive risk-takers (high win/high DNF) vs. steady point-scorers
    - **Career Arc Analysis**: Track performance evolution by filtering different career stages
    - **Championship Potential**: Correlate consistency metrics with championship-winning profiles
    - **Contract Negotiations**: Provide objective performance data for salary and contract discussions
    
    **Interpretation Guide:**
    - **Top-Right Quadrant** (High Win/High DNF): Aggressive, high-risk drivers (e.g., Senna-style)
    - **Top-Left Quadrant** (High Win/Low DNF): Dominant, consistent champions (e.g., Schumacher-style)
    - **Bottom-Left Quadrant** (Low Win/Low DNF): Reliable point-scorers, team players
    - **Narrow Box Plots**: Highly consistent drivers who deliver predictable results
    - **Wide Box Plots**: Volatile performers with high peaks and low troughs
    """)
