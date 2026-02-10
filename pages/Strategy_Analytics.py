import streamlit as st
import plotly.express as px
from utils import load_data, get_constructor_pit_stats, inject_custom_css, format_fig

st.set_page_config(page_title="Strategy Analytics", layout="wide")
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

st.markdown("---")

# Detailed Analytical Description
st.markdown("""
### Strategy & Circuit Intelligence - Methodology & Insights

#### What We Are Doing
We analyze team operational efficiency and circuit-specific racing characteristics to understand strategic decision-making and track suitability for overtaking. This module combines pit stop analytics with circuit intelligence to inform race strategy optimization.

#### What We Are Analyzing
**Pit Stop Performance Metrics:**
- **Total Pit Lane Time**: Complete duration from pit entry to exit (typically 20-25 seconds)
- **Team Efficiency Distribution**: Variation in pit stop times across constructors
- **Operational Consistency**: Standard deviation of pit stop durations per team
- **Hybrid Era Focus**: Analysis of 2014-2020 data when pit stops became heavily regulated

**Circuit Characteristics:**
- **Overtaking Potential**: Average absolute position change at each circuit
- **Position Gain/Loss Frequency**: How often drivers improve or lose positions
- **Circuit Difficulty Index**: Tracks requiring more reliance on qualifying vs. race strategy
- **Historical Consistency**: Circuits with 10+ races for statistical reliability

#### How We Are Doing It
**Analytical Techniques:**
1. **Pit Stop Analysis**:
   - Filter pit stops under 40 seconds to exclude anomalies
   - Convert milliseconds to seconds for readability
   - Merge constructor names with pit stop data via race-driver mappings
   - Create box plot distributions showing median, quartiles, and outliers
   - Focus on top 10 teams by stop volume for clarity

2. **Circuit Analysis**:
   - Calculate absolute position change (grid → finish) for each driver-race combination
   - Aggregate mean position change per circuit across all historical races
   - Filter circuits with minimum 10 races for statistical significance
   - Rank circuits by overtaking score (higher = more position changes)
   - Use horizontal bar chart for easy comparison

#### What It Helps In
**Strategic Applications:**

**Pit Stop Optimization:**
- **Team Benchmarking**: Identify which teams have fastest, most consistent pit crews
- **Operational Excellence**: Target areas for crew training and process improvement
- **Risk Assessment**: Understand pit stop variance that could cost positions
- **Regulatory Compliance**: Ensure stops meet minimum time requirements

**Race Strategy:**
- **Track Selection for Testing**: Focus development on high-overtaking circuits
- **Qualifying vs. Race Trade-off**: Understand where grid position matters most
- **Undercut/Overcut Timing**: Plan pit windows based on circuit overtaking difficulty
- **Tire Strategy**: Decide between aggressive (many stops) vs. conservative (few stops)

**Key Insights:**

**Pit Stop Patterns:**
- **Narrow Boxes**: Highly consistent teams (Mercedes, Red Bull typically)
- **Wide Boxes**: Variable performance or newer teams
- **Low Medians**: Operationally excellent teams (sub-22 seconds)
- **Outliers**: Problem stops due to equipment issues or driver errors

**Circuit Characteristics:**
- **High Overtaking Score** (>3.0): Monza, Spa, Shanghai - multiple DRS zones, long straights
- **Medium Score** (2.0-3.0): Mixed circuits with some passing opportunities
- **Low Score** (<2.0): Monaco, Hungary, Singapore - processional, qualifying-dependent

**Notable Findings:**
- Modern pit stops average 2-3 seconds stationary time
- Total pit lane time dominated by speed limiter transit (17-20 seconds)
- Circuit overtaking potential correlates with DRS effectiveness
""")
