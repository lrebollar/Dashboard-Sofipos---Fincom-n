import streamlit as st
import pandas as pd
from datetime import date
import numpy as np
import os 
from utils.f_graficos import plot_st, desl_2var
import pickle
from plotly.subplots import make_subplots
import plotly.graph_objects as go

#### Setup dashboard ####
st.set_page_config(layout="wide")
st.title("Dashboard Sector SOFIPOS - Fincomún")
st.subheader("Indicadores Financieros")

# Importar datos
dir_dict_sofipos = r'proyecto_dashboard_sofipos/data/dict_sofipos_sector.pkl' #Cambiar al final

with open(dir_dict_sofipos, 'rb') as archivo:
    dict_sofipos = pickle.load(archivo)

dict_sofipos['fintech'].keys()

## CT de crédito 
df_Ind = dict_sofipos['fintech']['Ind_financieros']
df_Ind.columns.to_list()
### Formato de fecha
df_Ind['periodo'] = pd.to_datetime(df_Ind['periodo'], format='%Y-%m')

#################################################################################
#### Indicadores Financieros ####
#################################################################################
segmentos = ['ROA', 'ROE', 'Liquidez', 'MIN', 'GAP / Activo', 'Capital contable / Activo',
             'IMOR cartera de crédito', 'IMORA cartera de crédito', 'ICOR cartera de crédito',
             'EPRC / Cartera de crédito', 'Tasa de interés implícita (TII) cartera de crédito E1 + E2', 
             'Tasa de interés implícita (TII) pasiva']

segmento = st.selectbox("Segmento de CT", options= segmentos)

st.subheader(f"{segmento}")

#################################################################################
#### Deslizantes - Segmento de CT ####
#################################################################################

##### Periodo ####
var_Ind_segmento_i100 = f"{segmento}"
var_Ind_segmento_pch = f"{segmento}_pct_YoY"
titulo_eje_i100 = f"{segmento}"
titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

periodo_segmento_Ind, df_filtrado_segmento_Ind = desl_2var(df = df_Ind,
                                 var1= var_Ind_segmento_i100,
                                 label1= titulo_eje_i100,
                                 var2= var_Ind_segmento_pch,
                                 label2= titulo_eje_pch,
                                 key_prefix=f"segmento_{segmento}"
                                 )

#################################################################################
#### Panel de Segmento de CT indice 100 y pch ####
#################################################################################
###### GRAFICOS ######
##### Indice base == 100
plt_segmento_Ind_sofipo_i100 = plot_st(df = df_filtrado_segmento_Ind,
                            serie= var_Ind_segmento_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

plt_segmento_Ind_sector_i100 = plot_st(df = df_filtrado_segmento_Ind,
                            serie= var_Ind_segmento_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

##### Cambio porcentual YoY%
plt_segmento_Ind_sofipo_pch = plot_st(df = df_filtrado_segmento_Ind,
                            serie= var_Ind_segmento_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

plt_segmento_Ind_sector_pch = plot_st(df = df_filtrado_segmento_Ind,
                            serie= var_Ind_segmento_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

###### PANEL ######
panel_segmento_Ind = make_subplots(rows=2, cols=2,
                            subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                            "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                            vertical_spacing=0.08)

#### Leyendas para cada gráfico
# Traces del primer gráfico → leyenda 1
for trace in plt_segmento_Ind_sector_i100.data:
    trace.legend = "legend"
    panel_segmento_Ind.add_trace(trace, row=1, col=1)

# Traces del segundo gráfico → leyenda 2
for trace in plt_segmento_Ind_sofipo_i100.data:
    trace.legend = "legend2"
    panel_segmento_Ind.add_trace(trace, row=2, col=1)

# Traces del tercer gráfico → leyenda 3
for trace in plt_segmento_Ind_sector_pch.data:
    trace.legend = "legend3"
    panel_segmento_Ind.add_trace(trace, row=1, col=2)

# Traces del cuarto gráfico → leyenda 4
for trace in plt_segmento_Ind_sofipo_pch.data:
    trace.legend = "legend4"
    panel_segmento_Ind.add_trace(trace, row=2, col=2)

#### Formato X para cada gráfico
# Replica el formato del eje X en ambas filas
panel_segmento_Ind.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=1)
panel_segmento_Ind.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=1)
panel_segmento_Ind.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=2)
panel_segmento_Ind.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=2)

#### Formato Y para cada gráfico
panel_segmento_Ind.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=1, col=1)
panel_segmento_Ind.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=2, col=1)
panel_segmento_Ind.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=1, col=2)
panel_segmento_Ind.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=2, col=2)


# Layout general del panel
panel_segmento_Ind.update_layout(
    height=900,
    legend=dict(
        title=dict(text="SOFIPO"),
        x=0.01, y=0.99,
        xanchor="left", yanchor="top",
        bgcolor="rgba(255,255,255,0.6)",
        tracegroupgap=1 
    ),
    legend2=dict(
        title=dict(text="SOFIPO"),
        x=0.01, y=0.45,   # ajusta 'y' para que caiga junto al segundo subplot
        xanchor="left", yanchor="top",
        bgcolor="rgba(255,255,255,0.6)",
        tracegroupgap=1 
    ),
    legend3=dict(
        title=dict(text="SOFIPO"),
        x=0.55, y=0.99,   # ajusta 'y' para que caiga junto al segundo subplot
        xanchor="left", yanchor="top",
        bgcolor="rgba(255,255,255,0.6)",
        tracegroupgap=1 
    ),
    legend4=dict(
        title=dict(text="SOFIPO"),
        x=0.55, y=0.45,   # ajusta 'y' para que caiga junto al segundo subplot
        xanchor="left", yanchor="top",
        bgcolor="rgba(255,255,255,0.6)",
        tracegroupgap=1 
    ),
)

st.plotly_chart(panel_segmento_Ind, use_container_width=True)
