# Football Player Analysis
# This script provides analysis capabilities for football player data from Transfermarkt.

# Import required libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set style for visualizations
plt.style.use('seaborn')
sns.set_palette('husl')

# Load data
def load_player_data():
    data_path = 'Data/'
    try:
        # Try to load the data file
        # You may need to adjust the file name and path based on your actual data
        df = pd.read_csv(os.path.join(data_path, 'players.csv'))
        print(f"Successfully loaded data with {len(df)} rows")
        return df
    except FileNotFoundError:
        print("Data file not found. Please ensure the data file exists in the Data directory.")
        return None

# Load the data
df = load_player_data()

# Basic data exploration
if df is not None:
    print("\nData Overview:")
    print(df.info())
    print("\nFirst few rows:")
    print(df.head())
    print("\nBasic statistics:")
    print(df.describe())

# Example visualization function
def plot_player_value_distribution(df):
    if df is not None and 'market_value' in df.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x='market_value', bins=30)
        plt.title('Distribution of Player Market Values')
        plt.xlabel('Market Value')
        plt.ylabel('Count')
        plt.show()
    else:
        print("Market value data not available")

# Call the visualization function
plot_player_value_distribution(df)

# Analysis Functions
def analyze_player_position(df, position_col='position'):
    if df is not None and position_col in df.columns:
        position_counts = df[position_col].value_counts()
        plt.figure(figsize=(12, 6))
        sns.barplot(x=position_counts.index, y=position_counts.values)
        plt.title('Player Distribution by Position')
        plt.xlabel('Position')
        plt.ylabel('Number of Players')
        plt.xticks(rotation=45)
        plt.show()
    else:
        print(f"Position data ({position_col}) not available")

def analyze_age_distribution(df, age_col='age'):
    if df is not None and age_col in df.columns:
        plt.figure(figsize=(10, 6))
        sns.histplot(data=df, x=age_col, bins=20)
        plt.title('Age Distribution of Players')
        plt.xlabel('Age')
        plt.ylabel('Count')
        plt.show()
    else:
        print(f"Age data ({age_col}) not available")

# Example usage
if __name__ == "__main__":
    # Load data
    df = load_player_data()
    
    # Run analyses
    if df is not None:
        analyze_player_position(df)
        analyze_age_distribution(df) 