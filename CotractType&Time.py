# Authenticate Google Sheets access
@st.cache_resource
def get_gspread_client():
    creds = Credentials.from_service_account_file(
        'service_account.json',  # Make sure this file is securely stored
        scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    )
    return gspread.authorize(creds)

# Load data from Google Sheets
@st.cache_data
def load_data():
    gc = get_gspread_client()
    spreadsheet = gc.open_by_key('1VTMPy-dvropKZANZeMJMxfuRmFrAYJ2YFC1kbLznT9Q')
    worksheet = spreadsheet.sheet1
    data = worksheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    return df

# Plot bar chart
def plot_bar_chart(df):
    contract_type_counts = df['contract_type'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    contract_type_counts.plot(kind='bar', ax=ax, color=['blue', 'gray', 'red'])
    ax.set_title('Job Postings Distribution by Contract Type')
    ax.set_xlabel('Contract Type')
    ax.set_ylabel('Number of Job Postings')
    ax.set_xticklabels(contract_type_counts.index, rotation=45)
    for p in ax.patches:
        ax.annotate(str(p.get_height()), (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha='center', va='center', xytext=(0, 10), textcoords='offset points')
    st.pyplot(fig)

# Plot pie chart
def plot_pie_chart(df):
    contract_type_counts = df['contract_type'].value_counts()
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.pie(contract_type_counts, labels=contract_type_counts.index, autopct='%1.1f%%',
           startangle=90, colors=['blue', 'gray', 'red'])
    ax.set_title('Job Postings Distribution by Contract Type')
    st.pyplot(fig)

# Streamlit UI
st.title("Job Postings Analysis")
df = load_data()

if not df.empty:
    st.subheader("Contract Type Distribution (Bar Chart)")
    plot_bar_chart(df)
    
    st.subheader("Contract Type Distribution (Pie Chart)")
    plot_pie_chart(df)
else:
    st.error("Failed to load data from Google Sheets.")
