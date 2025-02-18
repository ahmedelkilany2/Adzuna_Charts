import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import time
from google.oauth2.service_account import Credentials
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuration
SHEET_URL = "your_google_sheet_url"
REFRESH_INTERVAL = 14400  # 4 hours in seconds

# Set up Google Sheets credentials
@st.cache_resource
def get_google_credentials():
    credentials = {
        "type": "service_account",
        "project_id": "your-project-id",
        "private_key_id": "your-private-key-id",
        "private_key": "your-private-key",
        "client_email": "your-client-email",
        "client_id": "your-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "your-cert-url"
    }
    
    scope = [
        'https://spreadsheets.google.com/feeds',
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    
    creds = ServiceAccountCredentials.from_json_keyfile_dict(credentials, scope)
    return gspread.authorize(creds)

@st.cache_data(ttl=REFRESH_INTERVAL)
def load_data():
    """Load data from Google Sheets with caching"""
    try:
        client = get_google_credentials()
        sheet = client.open_by_url(SHEET_URL).sheet1
        data = sheet.get_all_records()
        df = pd.DataFrame(data)
        return df, None
    except Exception as e:
        return None, f"Error loading data: {str(e)}"

def plot_contract_distribution(df):
    """Create contract type distribution visualizations"""
    # Color scheme
    colors = {'Permanent': 'blue', 'Contract': 'gray', 'Temporary': 'red'}
    
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
    
    # Customize bar chart
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(
        showlegend=False,
        plot_bgcolor='white',
        title_x=0.5
    )
    
    # Pie Chart
    fig_pie = px.pie(
        values=contract_counts.values,
        names=contract_counts.index,
        title='Contract Type Distribution (%)',
        color=contract_counts.index,
        color_discrete_map=colors
    )
    
    # Customize pie chart
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(title_x=0.5)
    
    return fig_bar, fig_pie

def calculate_statistics(df):
    """Calculate key statistics from the data"""
    total_jobs = len(df)
    contract_stats = df['contract_type'].value_counts()
    contract_percentages = (contract_stats / total_jobs * 100).round(1)
    
    return {
        'total_jobs': total_jobs,
        'most_common_type': contract_stats.index[0],
        'most_common_count': contract_stats.iloc[0],
        'most_common_percentage': contract_percentages.iloc[0]
    }

def main():
    st.set_page_config(
        page_title="Job Market Analysis Dashboard",
        page_icon="📊",
        layout="wide"
    )
    
    st.title('📊 Job Market Analysis Dashboard')
    
    # Add last update time
    st.sidebar.write("Last updated:", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    st.sidebar.write("Data refreshes every 4 hours automatically")
    
    # Load data
    df, error = load_data()
    
    if error:
        st.error(error)
        return
    
    if df is None or df.empty:
        st.warning("No data available")
        return
    
    # Create metrics row
    stats = calculate_statistics(df)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Job Postings", stats['total_jobs'])
    with col2:
        st.metric("Most Common Type", stats['most_common_type'])
    with col3:
        st.metric(
            "Percentage of Most Common",
            f"{stats['most_common_percentage']}%"
        )
    
    # Create visualization row
    st.subheader("Contract Type Distribution")
    viz_col1, viz_col2 = st.columns(2)
    
    # Generate plots
    bar_fig, pie_fig = plot_contract_distribution(df)
    
    # Display plots
    with viz_col1:
        st.plotly_chart(bar_fig, use_container_width=True)
    
    with viz_col2:
        st.plotly_chart(pie_fig, use_container_width=True)
    
    # Add detailed data table
    st.subheader("Detailed Data")
    st.dataframe(
        df.style.background_gradient(subset=['salary_min', 'salary_max']),
        use_container_width=True
    )

if __name__ == '__main__':
    main()
