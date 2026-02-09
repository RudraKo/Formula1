import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Configure Plot Style
plt.style.use('ggplot') # Try a built-in style first to avoid seaborn dependency issues if any
sns.set_theme(style="whitegrid")

OUTPUT_DIR = "images"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

def load_data():
    print("Loading datasets...")
    results = pd.read_csv("data/clean_results.csv")
    laps = pd.read_csv("data/clean_lap_times.csv")
    pits = pd.read_csv("data/clean_pit_stops.csv")
    
    # Load status.csv (hardcoded path based on previous find command or relative assuming standard structure if we copied it, but better use absolute for now or try to find it)
    # The previous turn found it at:
    # /Users/punarvashu/.cache/kagglehub/datasets/rohanrao/formula-1-world-championship-1950-2020/versions/24/status.csv
    # We'll try to use that path or a fallback
    status_path = "data/status.csv"
    if os.path.exists(status_path):
        status = pd.read_csv(status_path)
    else:
        # Fallback: check if it's in the current directory or data folder if copied
        # For now, we assume it's there or we might fail. 
        # Let's try to load it from the same place as others if the user moved it, but likely not.
        print("WARNING: status.csv not found at expected path. Trying local directory.")
        try:
            status = pd.read_csv("status.csv")
        except FileNotFoundError:
            print("ERROR: status.csv not found. DNF analysis will be limited.")
            status = pd.DataFrame(columns=['statusId', 'status'])
            
    print(f"Loaded Results: {results.shape}")
    print(f"Loaded Laps: {laps.shape}")
    print(f"Loaded Pits: {pits.shape}")
    
    return results, laps, pits, status

def feature_engineering(results, laps, pits, status):
    print("\n--- Feature Engineering ---")
    
    # 1. Position Gain
    # If grid is 0 (pit lane start often), treat as last or handle carefully. 
    # But usually 0 means pit lane. Let's assume gain is valid if grid > 0.
    results['position_gain'] = np.where(results['grid'] > 0, results['grid'] - results['positionOrder'], 0)
    
    # 2. Key Flags
    results['win_flag'] = (results['positionOrder'] == 1).astype(int)
    results['podium_flag'] = (results['positionOrder'] <= 3).astype(int)
    
    # 3. DNF Flag
    # Map statusId to status descriptions
    results = pd.merge(results, status, on='statusId', how='left')
    
    # Common "Finished" statuses: 1 (Finished), 11 (+1 Lap), 12 (+2 Laps), etc.
    # We can perform a simpler check: if status is NOT 'Finished' and NOT '+N Laps' -> DNF?
    # Or typically statusId 1 is Finished.
    # Let's list IDs that represent finishing:
    # 1: Finished
    # 11-19: +X Laps
    # We can check the string content too.
    finished_mask = results['status'].str.contains('Finished|Lag|\+.*Lap', case=False, regex=True, na=False)
    results['dnf_flag'] = (~finished_mask).astype(int)
    
    # 4. Pit Stop Metrics (Aggregated per driver-race)
    pit_agg = pits.groupby(['raceId', 'driverId']).agg(
        pit_stop_count=('stop', 'max'),
        avg_pit_duration=('milliseconds', 'mean')
    ).reset_index()
    
    results = pd.merge(results, pit_agg, on=['raceId', 'driverId'], how='left')
    results['pit_stop_count'] = results['pit_stop_count'].fillna(0)
    
    # 5. Lap Time Metrics (Aggregated per driver-race)
    # We can calculate consistency here: std dev of lap times per race
    lap_agg = laps.groupby(['raceId', 'driverId']).agg(
        avg_race_lap_time=('milliseconds', 'mean'),
        lap_time_std=('milliseconds', 'std')
    ).reset_index()
    
    results = pd.merge(results, lap_agg, on=['raceId', 'driverId'], how='left')
    
    print("Features added: position_gain, win_flag, podium_flag, dnf_flag, pit metrics, lap metrics.")
    return results

def compute_driver_analytics(df):
    print("\n--- Computing Driver Analytics ---")
    
    # Group by Driver
    driver_stats = df.groupby(['driverId', 'driver_name']).agg(
        total_races=('raceId', 'count'),
        total_points=('points', 'sum'),
        total_wins=('win_flag', 'sum'),
        total_podiums=('podium_flag', 'sum'),
        total_dnfs=('dnf_flag', 'sum'),
        avg_finish_pos=('positionOrder', 'mean'),
        global_consistency=('positionOrder', 'std'), # Lower is better
        avg_position_gain=('position_gain', 'mean')
    ).reset_index()
    
    # Derived Metrics
    driver_stats['points_per_race'] = driver_stats['total_points'] / driver_stats['total_races']
    driver_stats['win_rate'] = driver_stats['total_wins'] / driver_stats['total_races']
    driver_stats['podium_rate'] = driver_stats['total_podiums'] / driver_stats['total_races']
    driver_stats['dnf_rate'] = driver_stats['total_dnfs'] / driver_stats['total_races']
    
    return driver_stats

def visualize_analytics(driver_stats, results):
    print("\n--- Generating Visualizations ---")
    
    # Filter for drivers with significant experience (e.g., > 50 races) to avoid noise
    active_drivers = driver_stats[driver_stats['total_races'] > 50].sort_values('total_points', ascending=False)
    top_10 = active_drivers.head(10)
    
    # 1. Top 10 Drivers by Total Points
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_10, x='total_points', y='driver_name', palette='viridis')
    plt.title('Top 10 Drivers by Career Points (>50 Races)')
    plt.xlabel('Total Points')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/top_10_drivers_points.png")
    plt.close()
    
    # 2. Consistency Analysis (Boxplot of Finish Positions for Top 10)
    top_10_ids = top_10['driverId'].unique()
    top_10_races = results[results['driverId'].isin(top_10_ids)]
    
    plt.figure(figsize=(14, 8))
    sns.boxplot(data=top_10_races, x='driver_name', y='positionOrder', order=top_10['driver_name'])
    plt.title('Finish Position Distribution (Consistency) for Top 10 Drivers')
    plt.xticks(rotation=45)
    plt.ylabel('Finish Position')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/driver_consistency_boxplot.png")
    plt.close()
    
    # 3. DNF Rate vs Win Rate Scatter
    plt.figure(figsize=(10, 8))
    sns.scatterplot(data=active_drivers, x='dnf_rate', y='win_rate', size='total_races', sizes=(20, 500), alpha=0.7)
    
    # Label top drivers
    for i, row in active_drivers.head(5).iterrows():
        plt.text(row['dnf_rate']+0.002, row['win_rate'], row['driver_name'], fontsize=9)
        
    plt.title('Win Rate vs DNF Rate (>50 Races)')
    plt.xlabel('DNF Rate')
    plt.ylabel('Win Rate')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/win_vs_dnf_scatter.png")
    plt.close()
    
    # 4. Podium Frequency Bar Chart
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_10, x='podium_rate', y='driver_name', palette='magma')
    plt.title('Podium Frequency Rate (Top 10 Drivers)')
    plt.xlabel('Podium Rate (Podiums / Races)')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/top_10_podium_rate.png")
    plt.close()

    print(f"Charts saved to {OUTPUT_DIR}")

def generate_report(driver_stats):
    print("\n--- Generating Report ---")
    
    top_points = driver_stats.sort_values('total_points', ascending=False).head(5)
    most_consistent = driver_stats[driver_stats['total_races'] > 50].sort_values('global_consistency').head(5)
    highest_win_rate = driver_stats[driver_stats['total_races'] > 50].sort_values('win_rate', ascending=False).head(5)
    
    report = f"""# F1 Driver Performance Intelligence Report

## Overview
This report analyzes driver performance across F1 history (1950-2020 dataset), creating a comprehensive view of wins, consistency, and reliability.

## 1. Top Performers (Career Points)
The following drivers have accumulated the most points in their careers (among those with >50 races):

| Driver | Races | Total Points | Wins | Podiums |
| :--- | :--- | :--- | :--- | :--- |
"""
    for _, row in top_points.iterrows():
        report += f"| {row['driver_name']} | {row['total_races']} | {row['total_points']:.1f} | {row['total_wins']} | {row['total_podiums']} |\n"
        
    report += """
## 2. Consistency Analysis
Consistency is measured by the standard deviation of finishing positions. Lower score = More consistent.

| Driver | Races | Consistency Score | Avg Finish | DNF Rate |
| :--- | :--- | :--- | :--- | :--- |
"""
    for _, row in most_consistent.iterrows():
        report += f"| {row['driver_name']} | {row['total_races']} | {row['global_consistency']:.2f} | {row['avg_finish_pos']:.1f} | {row['dnf_rate']:.2%} |\n"

    report += """
## 3. Win Efficiency
Drivers with the highest conversion rate of race starts to wins (>50 races):

| Driver | Win Rate | Wins | Races | Points/Race |
| :--- | :--- | :--- | :--- | :--- |
"""
    for _, row in highest_win_rate.iterrows():
        report += f"| {row['driver_name']} | {row['win_rate']:.2%} | {row['total_wins']} | {row['total_races']} | {row['points_per_race']:.2f} |\n"

    report += """
## 4. Visualizations

### Career Points Leaders
![Top 10 Points](../images/top_10_drivers_points.png)

### Consistency Profile
The boxplot shows the spread of finishing positions. A tighter box indicates higher consistency.
![Consistency Boxplot](../images/driver_consistency_boxplot.png)

### Reliability vs Success
Mapping DNF rates against Win rates to see the tradeoff between aggression/reliability and victory.
![Win vs DNF](../images/win_vs_dnf_scatter.png)

### Podium Frequency
Percentage of races finished on the podium.
![Podium Rate](../images/top_10_podium_rate.png)
"""
    
    with open("reports/driver_intelligence_report.md", "w") as f:
        f.write(report)
    print("Report generated: reports/driver_intelligence_report.md")

if __name__ == "__main__":
    results, laps, pits, status = load_data()
    
    # Process
    results_enriched = feature_engineering(results, laps, pits, status)
    driver_stats = compute_driver_analytics(results_enriched)
    
    # Visualize
    visualize_analytics(driver_stats, results_enriched)
    
    # Report
    generate_report(driver_stats)
