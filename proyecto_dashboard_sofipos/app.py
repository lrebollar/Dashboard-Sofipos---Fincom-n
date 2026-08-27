import streamlit as st

st.set_page_config(
    page_title="Dashboard Sector SOFIPOS - Fincomún",
    page_icon="📊",
    layout="wide"
)

pg = st.navigation([
    st.Page("pages/1_Cartera_de_credito.py",
             title="Información de Cartera", icon="📈")
])

pg.run()