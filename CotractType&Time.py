import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Replace this with your actual Google Sheet ID
SHEET_ID = "https://docs.google.com/spreadsheets/d/1VTMPy-dvropKZANZeMJMxfuRmFrAYJ2YFC1kbLznT9Q/edit?gid=553613618#gid=553613618"
SHEET_NAME = "Adzuna_job_listings"

@st.cache_data(ttl=14400)  # Cache for 4 hours
def load_data():
    """Load data from Google Sheets"""
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
        df = pd.read_csv(url)
        return df, None
    except Exception as e:
        return None, f"Error loading data: {str(e)}"

def plot_contract_distribution(df):
    """Create visualizations for contract type distribution"""
    colors = {'Permanent': '#1f77b4', 'Contract': '#7f7f7f', 'Temporary': '#d62728'}
    
    # Bar Chart
    contract_counts = df['contract_type'].value_counts()
    fig_bar = px.bar(
        x=contract_counts.index,
        y=contract_counts.values,
        title='Job Postings Distribution by Contract Type',
        labels={'x': 'Contract Type', 'y': 'Number of Job Postings'},
        text=contract_counts.values,
        color=contract_counts.index,
        color_discrete_map=colors
    )
    
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(showlegend=False)
    
    # Pie Chart
    fig_pie = px.pie(
        values=contract_counts.values,
        names=contract_counts.index,
        title='Contract Type Distribution (%)',
        color=contract_counts.index,
        color_discrete_map=colors
    )
    
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    
    return fig_bar, fig_pie

def main():
    st.set_page_config(page_title="Job Market Analysis", layout="wide")
    
    st.title('Job Market Analysis Dashboard')
    st.write('Analysis of job postings by contract type')
    
    # Add refresh time indicator
    st.sidebar.write(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    st.sidebar.write("Data refreshes automatically every 4 hours")
    
    # Load data
    df, error = load_data()
    
    if error:
        st.error(error)
        return
        
    if df is None or df.empty:
        st.warning("No data available")
        return
    
    # Display summary metrics
    total_jobs = len(df)
    contract_distribution = df['contract_type'].value_counts()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Job Postings", total_jobs)
    with col2:
        st.metric("Most Common Type", contract_distribution.index[0])
    with col3:
        percentage = (contract_distribution.iloc[0] / total_jobs * 100).round(1)
        st.metric("% of Most Common Type", f"{percentage}%")
    
    # Create visualizations
    st.subheader("Contract Type Distribution")
    viz_col1, viz_col2 = st.columns(2)
    
    bar_fig, pie_fig = plot_contract_distribution(df)
    
    with viz_col1:
        st.plotly_chart(bar_fig, use_container_width=True)
    
    with viz_col2:
        st.plotly_chart(pie_fig, use_container_width=True)
    
    # Display data table
    st.subheader("Raw Data")
    st.dataframe(df, use_container_width=True)

if __name__ == '__main__':
    main()
