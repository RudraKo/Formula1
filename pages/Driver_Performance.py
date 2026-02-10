import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from utils import load_data, get_driver_stats, inject_custom_css, format_fig

st.set_page_config(page_title="Driver Performance", page_icon="👤", layout="wide")
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
