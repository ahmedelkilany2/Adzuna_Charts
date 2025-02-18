import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Load Data from Google Sheets (Public Link)
sheet_url = "https://docs.google.com/spreadsheets/d/1VTMPy-dvropKZANZeMJMxfuRmFrAYJ2YFC1kbLznT9Q/export?format=csv&gid=553613618"
df = pd.read_csv(sheet_url)

# Step 2: Check the first few rows
print(df.head())

# Step 3: Function to Plot Bar Chart for Contract Type Distribution
def plot_contract_type_distribution(df):
    if 'contract_type' not in df.columns:
        print("Error: Column 'contract_type' not found in the dataset.")
        return

    contract_type_counts = df['contract_type'].value_counts()
    
    # Create bar chart
    ax = contract_type_counts.plot(kind='bar', figsize=(8, 6), color=['blue', 'gray', 'red'])
    plt.title('Job Postings Distribution by Contract Type')
    plt.xlabel('Contract Type')
    plt.ylabel('Number of Job Postings')
    plt.xticks(rotation=45)
    
    # Add data labels
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')

    plt.tight_layout()
    plt.show()

# Step 4: Function to Plot Pie Chart for Contract Type Distribution
def plot_contract_type_pie(df):
    if 'contract_type' not in df.columns:
        print("Error: Column 'contract_type' not found in the dataset.")
        return

    contract_type_counts = df['contract_type'].value_counts()

    # Create the pie chart
    plt.figure(figsize=(8, 6))
    plt.pie(contract_type_counts, labels=contract_type_counts.index, autopct='%1.1f%%', 
            startangle=90, colors=['blue', 'gray', 'red'])
    
    plt.title('Job Postings Distribution by Contract Type')
    plt.axis('equal')  # Ensures pie chart is a circle
    plt.tight_layout()
    plt.show()

# Step 5: Run the plots
plot_contract_type_distribution(df)
plot_contract_type_pie(df)
