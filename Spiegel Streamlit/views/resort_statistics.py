import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Spiegel Mining Dashboard",
                   page_icon=":bar_chart:",
                   layout='wide')


# Initialize Data
df = pd.read_csv('spiegel_metadata.csv', sep='|')

# Convert the 'date' column to datetime format
df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce')

resort_order = df['resort'].value_counts().index

#Set Columns
col1, col2 = st.columns(2)


#FIRST COLUMN
with col1:
    fig, ax = plt.subplots(figsize=(5, 3))  # Set the figure size

    # Create the Seaborn barplot
    sns.countplot(data=df, x='resort', ax=ax, order=resort_order)

    # Rotate x-axis labels for better readability (if many resorts)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right')

    # Set plot title
    ax.set_title('Distribution of Articles by Resort')
    ax.set_xlabel('Resort')
    ax.set_ylabel('Count')

    # Display the figure in the Streamlit app
    st.pyplot(fig)

#SECOND COLUMN
with col2:
    # Convert 'date' column to datetime (handling timezone info)
    df['date'] = pd.to_datetime(df['date'])

    # Extract the hour from the 'date' column
    df['hour'] = df['date'].dt.hour

    # No need to group and collect hours as lists
    # hours_by_resort = df.groupby('resort')['hour'].apply(list).reset_index()

    # Output
    print(df)

    fig2, ax = plt.subplots(figsize=(3, 5))

    # Plotting the scatter plot
    sns.scatterplot(data=df, x='hour', y='resort', ax=ax, hue='resort', palette='deep', legend=False)

    # Set y-ticks and labels based on resort_order
    resort_names = resort_order
    y_pos = np.arange(len(resort_order))
    ax.set_yticks(y_pos)
    ax.invert_yaxis()  # Labels read top-to-bottom

    # Set x-ticks and labels
    ax.set_xticks(np.arange(0, 24, 1))  # Create ticks from 0 to 23
    ax.set_xticklabels(np.arange(0, 24, 1))  # Optionally, set labels if needed

    # Set x-axis and title
    ax.set_xlabel('Posting Hours')
    ax.set_title('Posting Times of Resorts')

    # Plotting on Streamlit
    st.pyplot(fig2)