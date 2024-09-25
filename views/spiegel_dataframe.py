import streamlit as st
import pandas as pd
from datetime import datetime, date

# Page configuration
st.set_page_config(page_title="Spiegel Mining Dashboard",
                   page_icon=":bar_chart:",
                   layout='wide')

# Initialize Data
df = pd.read_csv('spiegel_metadata.csv', sep='|')

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce')

# Show DataFrame title
st.title('Spiegel Artikel Metadata')

# -----SIDEBAR------
st.sidebar.header('Please Filter Here:')
# Resortfilter
filter_resort = st.sidebar.multiselect(
    'Resorts:',
    options=df['resort'].unique(),
)
# Authorfilter
filter_author = st.sidebar.text_input('Author')
# Keyword-Filter
filter_keywords = st.sidebar.text_input('Keyword')
# Frei-Lesbar-Filter
filter_free_readable = st.sidebar.selectbox('Verfügbarkeit:', ['Alle', 'Nur frei verfügbar', 'Nur Abo'])
# Startdatum
start_date = st.sidebar.date_input('Startdatum', value=None, min_value=date(1958, 1, 1), max_value=datetime.today())
# Enddatum
end_date = st.sidebar.date_input('Enddatum', value=None, min_value=date(1958, 1, 1), max_value=datetime.today())


# Filter function
def apply_filters():
    df_filtered = df.copy()
    global start_date, end_date
    
    # Apply filters only if the user selected them
    if filter_resort:
        df_filtered = df_filtered[df_filtered['resort'].isin(filter_resort)]
    
    if filter_author:
        df_filtered = df_filtered[df_filtered['author'].str.contains(filter_author, case=False, na=False)]
    
    if filter_keywords:
        df_filtered = df_filtered[df_filtered['keywords'].str.contains(filter_keywords, case=False, na=False)]
    
    if filter_free_readable == 'Nur frei verfügbar':
        df_filtered = df_filtered[df_filtered['free_readable'] == True]
    elif filter_free_readable == 'Nur Abo':
        df_filtered = df_filtered[df_filtered['free_readable'] == False]
    
    # Apply date filters
    if start_date:
        start_date_dt = pd.to_datetime(start_date).tz_localize('UTC')  
        df_filtered = df_filtered[df_filtered['date'] >= start_date_dt]
    
    if end_date:
        end_date_dt = pd.to_datetime(end_date).tz_localize('UTC')
        df_filtered = df_filtered[df_filtered['date'] <= end_date_dt]
    
    
    return df_filtered



# Initialize a session state variable to track filtered data
if 'filtered_data' not in st.session_state:
    st.session_state.filtered_data = df

# Apply filters and display data
if st.sidebar.button('Filter anwenden'):
    st.session_state.filtered_data = apply_filters()

if st.sidebar.button('Clear Filters'):
    st.session_state.filtered_data = df  # Reset to the original dataframe

# Display the dataframe
st.dataframe(st.session_state.filtered_data)
st.metric(label='Anzahl Artikel:', value=len(st.session_state.filtered_data))