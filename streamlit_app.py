import streamlit as st

# --- PAGE SETUP ---
resort_statistics= st.Page(
    page="views/resort_statistics.py",
    title="Resort Statistics für Spiegel",
    default=True
)

artikel_tabelle= st.Page(
    page="views/spiegel_dataframe.py",
    title='Spiegel-Artikel filterbare Tabelle'
 
)

# - - - PAGE SETUP - - -
pg=st.navigation({'Pages':[resort_statistics,artikel_tabelle]})
pg.run()