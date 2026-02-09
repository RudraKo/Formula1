import kagglehub
import pandas as pd
import os
import numpy as np

def load_data():
    print("Downloading dataset...")
    # This will use the cached path if already downloaded
    path = kagglehub.dataset_download("rohanrao/formula-1-world-championship-1950-2020")
    print(f"Path to dataset files: {path}")

    files = [f for f in os.listdir(path) if f.endswith('.csv')]
    
    data = {}
    # Key tables we need
    key_files = {
        'drivers': 'drivers.csv',
        'constructors': 'constructors.csv',
        'races': 'races.csv',
        'results': 'results.csv', 
        'lap_times': 'lap_times.csv', 
        'pit_stops': 'pit_stops.csv', 
        'qualifying': 'qualifying.csv', 
        'driver_standings': 'driver_standings.csv'
    }

    for name, filename in key_files.items():
        if filename in files:
            file_path = os.path.join(path, filename)
            # Handle \N as NaN explicitly for all files
            df = pd.read_csv(file_path, na_values=['\\N']) 
            data[name] = df
            print(f"Loaded {name}: {df.shape}")
        else:
            print(f"WARNING: {filename} not found!")
    
    return data

def clean_data(data):
    print("\n--- Starting Data Cleaning ---")
    
    # 1. Clean Drivers
    if 'drivers' in data:
        df = data['drivers']
        # Combine name
        df['driver_name'] = df['forename'] + ' ' + df['surname']
        # Date of birth
        df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
        # Drop url
        df.drop(columns=['url'], inplace=True, errors='ignore')
        data['drivers'] = df
        print("Cleaned drivers")

    # 2. Clean Constructors
    if 'constructors' in data:
        df = data['constructors']
        df.drop(columns=['url'], inplace=True, errors='ignore')
        data['constructors'] = df
        print("Cleaned constructors")

    # 3. Clean Races
    if 'races' in data:
        df = data['races']
        # Date to datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        # Drop url
        df.drop(columns=['url'], inplace=True, errors='ignore')
        # Filter for relevant columns to keep master table lighter
        # We assume 'time' in races is race start time, might be useful, keeping it for now
        data['races'] = df
        print("Cleaned races")

    # 4. Clean Results
    if 'results' in data:
        df = data['results']
        # numeric conversion for critical columns
        cols_to_numeric = ['number', 'grid', 'position', 'points', 'laps', 'milliseconds', 'fastestLap', 'rank', 'fastestLapSpeed']
        for col in cols_to_numeric:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # Sanity Checks
        # Filter out rows where positionOrder is < 1 (shouldn't happen but good to check)
        original_len = len(df)
        df = df[df['positionOrder'] >= 1]
        if len(df) < original_len:
            print(f"Removed {original_len - len(df)} invalid positionOrder rows in results")
        
        data['results'] = df
        print("Cleaned results")

    # 5. Clean Lap Times
    if 'lap_times' in data:
        df = data['lap_times']
        df['milliseconds'] = pd.to_numeric(df['milliseconds'], errors='coerce')
        # Sanity check: lap time > 0
        df = df[df['milliseconds'] > 0]
        data['lap_times'] = df
        print("Cleaned lap_times")

    # 6. Clean Pit Stops
    if 'pit_stops' in data:
        df = data['pit_stops']
        df['milliseconds'] = pd.to_numeric(df['milliseconds'], errors='coerce')
        df = df[df['milliseconds'] > 0]
        data['pit_stops'] = df
        print("Cleaned pit_stops")
        
    return data

def merge_data(data):
    print("\n--- Starting Data Merging ---")
    
    # Prerequisite check
    required = ['results', 'races', 'drivers', 'constructors', 'lap_times', 'pit_stops']
    for req in required:
        if req not in data:
            print(f"CRITICAL: Missing {req} table for merging.")
            return {}

    races = data['races'][['raceId', 'year', 'round', 'circuitId', 'name', 'date']]
    races = races.rename(columns={'name': 'race_name', 'date': 'race_date'})
    
    drivers = data['drivers'][['driverId', 'driver_name', 'nationality', 'code']]
    drivers = drivers.rename(columns={'nationality': 'driver_nationality'})
    
    constructors = data['constructors'][['constructorId', 'name', 'nationality']]
    constructors = constructors.rename(columns={'name': 'constructor_name', 'nationality': 'constructor_nationality'})

    # 1. Race Results Master
    print("Merging Results Master...")
    results = data['results']
    
    # Merge with Races
    res_master = pd.merge(results, races, on='raceId', how='left')
    
    # Merge with Drivers
    res_master = pd.merge(res_master, drivers, on='driverId', how='left')
    
    # Merge with Constructors
    res_master = pd.merge(res_master, constructors, on='constructorId', how='left')
    
    # 2. Lap Times Master
    print("Merging Lap Times Master...")
    laps = data['lap_times']
    
    # Merge with Races
    laps_master = pd.merge(laps, races, on='raceId', how='left')
    
    # Merge with Drivers
    laps_master = pd.merge(laps_master, drivers, on='driverId', how='left')
    
    # 3. Pit Stops Master
    print("Merging Pit Stops Master...")
    pits = data['pit_stops']
    
    # Merge with Races
    pits_master = pd.merge(pits, races, on='raceId', how='left')
    
    # Merge with Drivers
    pits_master = pd.merge(pits_master, drivers, on='driverId', how='left')
    
    return {
        'results_master': res_master,
        'lap_times_master': laps_master,
        'pit_stops_master': pits_master
    }

def export_data(merged_data):
    print("\n--- Exporting Data ---")
    for name, df in merged_data.items():
        filename = f"clean_{name.replace('_master', '')}.csv"
        # We keep the _master suffix logic or just simplify?
        # User requested: clean_results.csv, clean_lap_times.csv, clean_pit_stops.csv
        # The keys are results_master, lap_times_master...
        # Let's map strict names
        if name == 'results_master':
            filename = 'clean_results.csv'
        elif name == 'lap_times_master':
            filename = 'clean_lap_times.csv'
        elif name == 'pit_stops_master':
            filename = 'clean_pit_stops.csv'
            
        print(f"Saving {filename} (Shape: {df.shape})...")
        df.to_csv(f"data/{filename}", index=False)
        print("Saved.")

if __name__ == "__main__":
    data = load_data()
    data = clean_data(data)
    merged = merge_data(data)
    if merged:
        export_data(merged)
        print("\nPipeline Complete!")
