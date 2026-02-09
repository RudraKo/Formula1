import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Configure Plot Style
plt.style.use('ggplot')
sns.set_theme(style="whitegrid")

OUTPUT_DIR = "images"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def load_data():
    print("Loading datasets for Strategy Analysis...")
    results = pd.read_csv("data/clean_results.csv")
    laps = pd.read_csv("data/clean_lap_times.csv")
    pits = pd.read_csv("data/clean_pit_stops.csv")
    return results, laps, pits

def analyze_lap_pace(laps, results, target_race_id=1073):
    print("\n--- Analyzing Lap Pace ---")
    
    # Filter for target race (Abu Dhabi 2021)
    target_race = results[(results['raceId'] == target_race_id)]
    
    if target_race.empty:
        # Fallback to name search
        target_race = results[(results['year'] == 2021) & (results['race_name'].str.contains('Abu Dhabi', case=False, na=False))]
        
    if target_race.empty:
        print("Target race (Abu Dhabi 2021) not found. Using first race of 2021 as fallback.")
        target_race = results[results['year'] == 2021].iloc[[0]]
        
    race_id = target_race['raceId'].values[0]
    race_name = target_race['race_name'].values[0]
    year = target_race['year'].values[0]
    print(f"Selected Race: {race_name} {year} (ID: {race_id})")
    
    # Get Laps for this race
    race_laps = laps[laps['raceId'] == race_id].copy()
    
    # Get Top 5 Finishers
    top_finishers_df = target_race[target_race['positionOrder'] <= 5]
    top_finishers_ids = top_finishers_df['driverId'].unique()
    
    race_laps_top = race_laps[race_laps['driverId'].isin(top_finishers_ids)].copy()
    
    # Check for driver_name. Created clean_lap_times.csv has it.
    if 'driver_name' not in race_laps_top.columns:
        print("Adding driver_name...")
        driver_map = results[['driverId', 'driver_name']].drop_duplicates()
        race_laps_top = pd.merge(race_laps_top, driver_map, on='driverId', how='left')

    # Calculate Rolling Average (Window=3)
    race_laps_top = race_laps_top.sort_values(['driverId', 'lap'])
    race_laps_top['rolling_lap_time'] = race_laps_top.groupby('driverId')['milliseconds'].transform(lambda x: x.rolling(window=3).mean())
    
    # Filter valid rolling times
    race_laps_top = race_laps_top.dropna(subset=['rolling_lap_time'])
    
    # Convert milliseconds to seconds for readability
    race_laps_top['seconds'] = race_laps_top['rolling_lap_time'] / 1000
    
    plt.figure(figsize=(14, 8))
    sns.lineplot(data=race_laps_top, x='lap', y='seconds', hue='driver_name', linewidth=2)
    plt.title(f"Lap Pace Evolution (Rolling Avg 3 Laps) - {race_name} {year}")
    plt.xlabel("Lap Number")
    plt.ylabel("Lap Time (s)")
    plt.legend(title='Driver')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/lap_pace_trace_{year}.png")
    plt.close()
    print(f"Saved lap_pace_trace_{year}.png")

def analyze_pit_strategy(pits, results):
    print("\n--- Analyzing Pit Stop Strategy ---")
    
    # Pit stops has raceId, driverId, year... but NOT constructor_name.
    # We need to merge constructor_name from results.
    
    # Unique driver-race-constructor mapping
    driver_team_map = results[['raceId', 'driverId', 'constructor_name']].drop_duplicates()
    
    # Determine the join keys.
    # pits has raceId, driverId.
    # Use inner join to ensure we only analyze stops where we know the constructor.
    # Note: If pits has 'year' and results has 'year', and we merge with driver_team_map (which usually shouldn't have year unless we add it), we are safe if driver_team_map is minimal.
    # I already selected minimal cols above.
    
    pits_merged = pd.merge(pits, driver_team_map, on=['raceId', 'driverId'], how='inner')
    
    # pits already has 'year' from clean_pit_stops.csv.
    # No need to merge year again.
    
    # Filter for Hybrid Era 2014+
    if 'year' in pits_merged.columns:
        pits_modern = pits_merged[pits_merged['year'] >= 2014]
    else:
        # Fallback if year was somehow lost or suffixed (unlikely now)
        print("WARNING: year column missing in pits, skipping filter.")
        pits_modern = pits_merged
    
    # Calculate Median Stop Duration by Team (Top 10 Teams by count)
    top_teams = pits_modern['constructor_name'].value_counts().head(10).index
    pits_top_teams = pits_modern[pits_modern['constructor_name'].isin(top_teams)]
    
    # Convert duration to seconds (milliseconds / 1000)
    pits_top_teams['stop_seconds'] = pits_top_teams['milliseconds'] / 1000
    
    # Remove outliers (e.g. stops > 60s, usually repairs/penalties)
    pits_clean = pits_top_teams[pits_top_teams['stop_seconds'] < 40] 

    plt.figure(figsize=(12, 6))
    order = pits_clean.groupby('constructor_name')['stop_seconds'].median().sort_values().index
    sns.boxplot(data=pits_clean, x='constructor_name', y='stop_seconds', order=order, palette='Set3')
    plt.title("Team Pit Stop Performance (2014-2020) - Distribution")
    plt.xlabel("Constructor")
    plt.ylabel("Time (s)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/team_pit_performance.png")
    plt.close()
    print("Saved team_pit_performance.png")

def analyze_circuit_intelligence(results):
    print("\n--- Analyzing Circuit Intelligence (Overtaking) ---")
    
    # Calculate Overtaking Potential: Average positions gained per race
    # We use (Grid - Finish Position).
    # Filter out DNFs? Typically overtaking stats exclude DNFs or handle them.
    # We'll map DNFs to NaN gain or exclude them for pure overtaking stats.
    # Results already has `position_gain` calculated in `driver_analytics.py` step... 
    # Wait, clean_results.csv DOES NOT have position_gain unless we explicitly saved it in previous step.
    # We calculated it in memory in `driver_analytics.py` but didn't save it back to CSV maybe.
    # Let's recalculate it.
    
    results['position_gain'] = results['grid'] - results['positionOrder']
    
    # Exclude races where grid was 0 (often pit lane start) to avoid skew
    valid_results = results[results['grid'] > 0]
    
    # Aggregate by Circuit (race_name)
    circuit_stats = valid_results.groupby('race_name').agg(
        avg_gain=('position_gain', 'mean'), # Net gain (can be negative due to drops)
        abs_gain=('position_gain', lambda x: x.abs().mean()), # Activity level (up or down)
        count=('raceId', 'nunique') # Number of races held
    ).reset_index()
    
    # Filter for active circuits (e.g. > 10 races held)
    circuit_stats = circuit_stats[circuit_stats['count'] >= 10]
    
    # Top 10 High "Action" Circuits
    top_action = circuit_stats.sort_values('abs_gain', ascending=False).head(10)
    
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_action, x='abs_gain', y='race_name', palette='coolwarm')
    plt.title("Circuit Overtaking Potential (Avg Position Change)")
    plt.xlabel("Avg Position Change (Abs Value)")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/circuit_overtaking_rank.png")
    plt.close()
    print("Saved circuit_overtaking_rank.png")

def analyze_championship_battle(results, year=2021):
    print(f"\n--- Analyzing Championship Battle ({year}) ---")
    
    season = results[results['year'] == year].copy()
    if season.empty:
        print(f"Year {year} not found. Skipping.")
        return
        
    # Get top 2 drivers by total points
    top_drivers = season.groupby('driverId')['points'].sum().sort_values(ascending=False).head(2).index
    battle = season[season['driverId'].isin(top_drivers)].copy()
    
    # Sort by round
    battle = battle.sort_values(['round'])
    
    # Calculate Cumulative Points
    battle['cumulative_points'] = battle.groupby('driverId')['points'].cumsum()
    
    # driver_name is already in results/battle, no need to merge again
    # If for some reason it's missing, we could add it, but it should be there.
    if 'driver_name' not in battle.columns:
        print("Adding driver_name for championship battle...")
        driver_map = results[['driverId', 'driver_name']].drop_duplicates()
        battle = pd.merge(battle, driver_map, on='driverId', how='left')
    
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=battle, x='round', y='cumulative_points', hue='driver_name', marker='o', linewidth=2.5)
    plt.title(f"Championship Battle {year}: Points Progression")
    plt.xlabel("Race Round")
    plt.ylabel("Cumulative Points")
    plt.legend(title='Driver')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/championship_battle_{year}.png")
    plt.close()
    print(f"Saved championship_battle_{year}.png")

def generate_report(results):
    print("\n--- Generating Strategy Report ---")
    report = """# F1 Strategy & Championship Intelligence Report

## Overview
This report analyzes advanced race dynamics, including lap pace evolution, pit crew performance, and circuit characteristics.

## 1. Pit Stop Performance (Hybrid Era 2014-2020)
Analysis of pit stop durations reveals the operational efficiency of teams.
![Team Pit Performance](../images/team_pit_performance.png)

## 2. Circuit Intelligence
Top circuits ranked by average position changes (overtaking potential). High variance tracks offer more strategic opportunities.
![Circuit Overtaking](../images/circuit_overtaking_rank.png)

## 3. Championship Dynamics (Case Study: 2021)
The visible tightening of the points gap between contenders throughout the season.
![Championship Battle](../images/championship_battle_2021.png)

## 4. Lap Pace Analysis
Rolling average lap times for the selected race showcase tire degradation and stint pace.
![Lap Pace](../images/lap_pace_trace_2021.png)
"""
    with open("reports/strategy_intelligence_report.md", "w") as f:
        f.write(report)
    print("Report generated: reports/strategy_intelligence_report.md")

if __name__ == "__main__":
    results, laps, pits = load_data()
    
    analyze_lap_pace(laps, results)
    analyze_pit_strategy(pits, results)
    analyze_circuit_intelligence(results)
    analyze_championship_battle(results, year=2021) # 2021 is iconic
    
    generate_report(results)
