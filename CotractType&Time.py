import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import gspread
from google.oauth2.service_account import Credentials

# Streamlit Title
st.title("Job Postings Analysis")

# Cache Google Sheets Data
@st.cache_data
def fetch_data():
    try:
        # Google Sheets API Credentials
        creds = Credentials.from_service_account_file(
            'mesmerizing-app-448406-v3-7e9711d82c46.json',  # Replace with your file
            scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
        )
        
        # Authorize and Open Google Sheet
        gc = gspread.authorize(creds)
        spreadsheet = gc.open_by_key('1VTMPy-dvropKZANZeMJMxfuRmFrAYJ2YFC1kbLznT9Q')
        worksheet = spreadsheet.sheet1

        # Convert Sheet Data to Pandas DataFrame
        data = worksheet.get_all_values()
        df = pd.DataFrame(data[1:], columns=data[0])
        
        return df

    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Fetch Data
df = fetch_data()

# Check if data loaded
if df is not None:
    
    # Convert contract_type column to lowercase for consistency
    df['contract_type'] = df['contract_type'].str.lower()

    # Plot 1: Bar Chart (Contract Type Distribution)
    st.subheader("Job Postings by Contract Type (Bar Chart)")
    def plot_contract_type_bar_chart(df):
        contract_type_counts = df['contract_type'].value_counts()
        
        fig, ax = plt.subplots(figsize=(8, 6))
        contract_type_counts.plot(kind='bar', color=['blue', 'gray', 'red'], ax=ax)
        
        plt.title('Job Postings Distribution by Contract Type')
        plt.xlabel('Contract Type')
        plt.ylabel('Number of Job Postings')
        plt.xticks(rotation=45)

        # Add labels on top of bars
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                        ha='center', va='center', xytext=(0, 10), textcoords='offset points')

        st.pyplot(fig)

    plot_contract_type_bar_chart(df)

    # Plot 2: Pie Chart (Contract Type Distribution)
    st.subheader("Job Postings by Contract Type (Pie Chart)")
    def plot_contract_type_pie_chart(df):
        contract_type_counts = df['contract_type'].value_counts()

        fig, ax = plt.subplots(figsize=(8, 6))
        ax.pie(contract_type_counts, labels=contract_type_counts.index, autopct='%1.1f%%',
               startangle=90, colors=['blue', 'gray', 'red'])
        
        plt.title('Job Postings Distribution by Contract Type')
        plt.axis('equal')

        st.pyplot(fig)

    plot_contract_type_pie_chart(df)

else:
    st.warning("No data available. Check your Google Sheets connection.")
