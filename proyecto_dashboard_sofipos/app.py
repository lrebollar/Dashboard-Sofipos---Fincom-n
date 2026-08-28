import streamlit as st

st.set_page_config(
    page_title="Dashboard Sector SOFIPOS - Fincomún",
    page_icon="📊",
    layout="wide"
)

pg = st.navigation([
    st.Page("pages/0_Inicio.py",
             title="Inicio", icon="🏠"),
    st.Page("pages/1_Cartera_de_credito.py",
             title="Información de Cartera de Crédito", icon="📈"),
    st.Page("pages/2_EPRC.py",
                title="Estimaciones Preventivas de Riesgo Crediticio", icon="📈"),
    st.Page("pages/3_Captacion.py",
                title="Captación tradicional", icon="📈"),
    st.Page("pages/4_Ingresos_por_intereses.py",
                title="Ingresos por intereses", icon="📈"),
    st.Page("pages/5_Indicadores_financieros.py",
                title="Indicadores Financieros", icon="📈")
])


pg.run()