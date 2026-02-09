import streamlit as st
import plotly.express as px
from utils import load_data, get_constructor_pit_stats, inject_custom_css, format_fig

st.set_page_config(page_title="Strategy Analytics", page_icon="charts", layout="wide")
inject_custom_css()

st.title("Strategy & Circuit Intelligence")

results, _, pits = load_data()

if results is not None:
    tab1, tab2 = st.tabs(["Pit Stop Efficiency", "Circuit Overtaking"])
    
    with tab1:
        st.subheader("Team Operational Efficiency (2014-2020)")
        
        # Get processed pit data
        pit_stats = get_constructor_pit_stats(pits, results)
        
        # Filter by year for relevance
        pit_modern = pit_stats[pit_stats['year'] >= 2014]
        
        # Boxplot of durations by team
        # Data reflects Total Pit Lane Time (approx 20-25s), not just stationary time.
        # Utils already filters < 40s.
        pit_viz = pit_modern
        
        top_teams = pit_viz['constructor_name'].value_counts().head(10).index
        pit_viz_filtered = pit_viz[pit_viz['constructor_name'].isin(top_teams)]
        
        fig_pit = px.box(
            pit_viz_filtered, 
            x='constructor_name', 
            y='seconds', 
            color='constructor_name',
            title="Pit Lane Time Distribution (Total Time)",
            labels={'seconds': 'Total Pit Time (s)'}
        )
        fig_pit.update_layout(showlegend=False)
        fig_pit = format_fig(fig_pit, "Pit Lane Efficiency")
        st.plotly_chart(fig_pit, use_container_width=True)
        
    with tab2:
        st.subheader("Circuit Overtaking Potential")
        
        # Calculate circuit stats
        # Filter out Grid 0
        valid_res = results[results['grid'] > 0].copy()
        
        circuit_stats = valid_res.groupby('race_name').agg(
            overtaking_score=('position_gain', lambda x: x.abs().mean()),
            races_held=('raceId', 'nunique')
        ).reset_index()
        
        # Filter for established circuits
        circuit_stats = circuit_stats[circuit_stats['races_held'] >= 10]
        top_circuits = circuit_stats.sort_values('overtaking_score', ascending=False).head(15)
        
        fig_circuit = px.bar(
            top_circuits, 
            x='overtaking_score', 
            y='race_name', 
            orientation='h',
            color='overtaking_score',
            title="Circuit Overtaking Index (Avg Position Change)",
            labels={'overtaking_score': 'Avg Absolute Position Change'},
            color_continuous_scale='Reds'
        )
        fig_circuit.update_layout(yaxis={'categoryorder':'total ascending'})
        fig_circuit = format_fig(fig_circuit, "Overtaking Factor")
        st.plotly_chart(fig_circuit, use_container_width=True)
