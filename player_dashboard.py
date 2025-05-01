import streamlit as st
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Add this line before importing pyplot
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Set page configuration
st.set_page_config(
    page_title="Football Player Market Value Analysis",
    page_icon="⚽",
    layout="wide"
)

# Title and description
st.title("⚽ Football Player Market Value Analysis")
st.markdown("Analysis of player market values across different countries and positions")

# Load the data
@st.cache_data
def load_data():
    try:
        return pd.read_csv('Data/players.csv')
    except FileNotFoundError:
        st.error("Could not find Data/players.csv. Please ensure the data file is in the correct location.")
        return None

players_df = load_data()

if players_df is not None:
    # Sidebar filters
    st.sidebar.header("Filters")
    
    # Country filter
    all_countries = players_df['country_of_birth'].unique()
    selected_countries = st.sidebar.multiselect(
        "Select Countries",
        options=all_countries,
        default=list(players_df.groupby('country_of_birth')['market_value_in_eur']
                    .max().sort_values(ascending=False).head(15).index)
    )
    
    # Position filter
    all_positions = players_df['position'].unique()
    selected_positions = st.sidebar.multiselect(
        "Select Positions",
        options=all_positions,
        default=list(all_positions)
    )
    
    # Filter data based on selections
    filtered_df = players_df[
        (players_df['country_of_birth'].isin(selected_countries)) &
        (players_df['position'].isin(selected_positions))
    ]
    
    # Main content
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader(" Dataset Overview")
        st.write(f"Total Players: {len(filtered_df):,}")
        st.write(f"Countries: {len(selected_countries)}")
        st.write(f"Positions: {len(selected_positions)}")
    
    with col2:
        st.subheader(" Market Value Statistics")
        st.write(f"Total Market Value: €{filtered_df['market_value_in_eur'].sum():,.2f}")
        st.write(f"Average Market Value: €{filtered_df['market_value_in_eur'].mean():,.2f}")
        st.write(f"Highest Market Value: €{filtered_df['market_value_in_eur'].max():,.2f}")
    
    # Market Value Analysis
    st.header("Market Value Analysis")
    
    tab1, tab2, tab3 = st.tabs(["Highest Values", "Average Values", "Detailed Stats"])
    
    with tab1:
        try:
            # Highest Market Value visualization
            fig1, ax1 = plt.subplots(figsize=(12, 6))
            position_max_values = filtered_df.groupby(['country_of_birth', 'position'])['market_value_in_eur'].max().unstack()
            country_order = position_max_values.max(axis=1).sort_values(ascending=False).index
            position_order = position_max_values.max().sort_values(ascending=False).index
            
            for position in position_order:
                if position in position_max_values.columns:
                    sns.barplot(x=position_max_values.loc[country_order].index,
                              y=position_max_values.loc[country_order][position],
                              label=position,
                              alpha=0.7,
                              ax=ax1)
            
            plt.title('Highest Player Market Value by Country and Position')
            plt.xlabel('Country')
            plt.ylabel('Market Value (EUR)')
            plt.xticks(rotation=45)
            plt.legend(title='Position', bbox_to_anchor=(1.05, 1))
            plt.tight_layout()
            st.pyplot(fig1)
        except Exception as e:
            st.error(f"Error in highest values visualization: {str(e)}")
    
    with tab2:
        try:
            # Average Market Value visualization
            fig2, ax2 = plt.subplots(figsize=(12, 6))
            position_avg_values = filtered_df.groupby(['country_of_birth', 'position'])['market_value_in_eur'].mean().unstack()
            country_avg_order = position_avg_values.max(axis=1).sort_values(ascending=False).index
            
            for position in position_order:
                if position in position_avg_values.columns:
                    sns.barplot(x=position_avg_values.loc[country_avg_order].index,
                              y=position_avg_values.loc[country_avg_order][position],
                              label=position,
                              alpha=0.7,
                              ax=ax2)
            
            plt.title('Average Player Market Value by Country and Position')
            plt.xlabel('Country')
            plt.ylabel('Average Market Value (EUR)')
            plt.xticks(rotation=45)
            plt.legend(title='Position', bbox_to_anchor=(1.05, 1))
            plt.tight_layout()
            st.pyplot(fig2)
        except Exception as e:
            st.error(f"Error in average values visualization: {str(e)}")
    
    with tab3:
        try:
            # Detailed statistics table
            st.subheader("Detailed Statistics by Country and Position")
            
            for country in country_order:
                country_data = filtered_df[filtered_df['country_of_birth'] == country]
                
                st.write(f"\n### {country}")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"Highest Market Value: €{country_data['market_value_in_eur'].max():,.2f}")
                with col2:
                    st.write(f"Average Market Value: €{country_data['market_value_in_eur'].mean():,.2f}")
                
                position_stats = country_data.groupby('position')['market_value_in_eur'].agg(['mean', 'max']).sort_values('max', ascending=False)
                position_stats = position_stats.round(2)
                st.dataframe(position_stats)
        except Exception as e:
            st.error(f"Error in detailed stats: {str(e)}")
    
    # Additional Analysis
    st.header("Additional Insights")
    
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            # Age Distribution
            st.subheader("Age Distribution")
            filtered_df['age'] = (pd.to_datetime('today') - pd.to_datetime(filtered_df['date_of_birth'])).dt.days / 365.25
            
            fig3, ax3 = plt.subplots(figsize=(10, 6))
            sns.histplot(data=filtered_df, x='age', bins=30, kde=True)
            plt.title('Player Age Distribution')
            plt.xlabel('Age')
            plt.ylabel('Count')
            st.pyplot(fig3)
        except Exception as e:
            st.error(f"Error in age distribution visualization: {str(e)}")
    
    with col2:
        try:
            # Position Distribution
            st.subheader("Position Distribution")
            fig4, ax4 = plt.subplots(figsize=(10, 6))
            position_counts = filtered_df['position'].value_counts()
            plt.pie(position_counts, labels=position_counts.index, autopct='%1.1f%%')
            plt.title('Distribution of Players by Position')
            st.pyplot(fig4)
        except Exception as e:
            st.error(f"Error in position distribution visualization: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Data source: Transfermarkt")