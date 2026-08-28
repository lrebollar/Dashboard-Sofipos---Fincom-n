import streamlit as st

st.title("Dashboard Sector SOFIPOS - Fincomún")
st.write("Selecciona una sección para comenzar:")

st.page_link("pages/1_Cartera_de_credito.py", label="📈 Información de Cartera de Crédito", icon="📈")
st.page_link("pages/2_EPRC.py", label="Estimaciones Preventivas de Riesgo Crediticio")
st.page_link("pages/3_Captacion.py", label="Captación tradicional")
st.page_link("pages/4_Ingresos_por_intereses.py", label="Ingresos por intereses")
st.page_link("pages/5_Indicadores_financieros.py", label="Indicadores Financieros")