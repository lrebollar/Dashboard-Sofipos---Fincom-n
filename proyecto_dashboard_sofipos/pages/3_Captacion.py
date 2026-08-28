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
st.subheader("Captación Tradicional")

# Importar datos
dir_dict_sofipos = r'proyecto_dashboard_sofipos/data/dict_sofipos_sector.pkl' #Cambiar al final

with open(dir_dict_sofipos, 'rb') as archivo:
    dict_sofipos = pickle.load(archivo)

dict_sofipos['fintech'].keys()

## CT de crédito 
df_CT = dict_sofipos['fintech']['Capt_trad']
df_CT.columns.to_list()
### Formato de fecha
df_CT['periodo'] = pd.to_datetime(df_CT['periodo'], format='%Y-%m')


#################################################################################
#### Deslizantes - CT ####
#################################################################################
##### Periodo ####
var_CT_i100 = 'Captación tradicional_i_b100'
var_CT_pch = 'Captación tradicional_pct_YoY'
titulo_eje_i100 = 'Captación tradicional (2023-01 = 100)'
titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

periodo_CT, df_filtrado_CT = desl_2var(df = df_CT,
                                 var1= var_CT_i100,
                                 label1= titulo_eje_i100,
                                 var2= var_CT_pch,
                                 label2= titulo_eje_pch,
                                 key_prefix="CT_total"
                                 )

#################################################################################
#### Panel CT indice 100 y pch ####
#################################################################################
###### GRAFICOS ######
##### Indice base == 100
## Setup

plt_CT_sofipo_i100 = plot_st(df = df_filtrado_CT,
                            serie= var_CT_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

plt_CT_sector_i100 = plot_st(df = df_filtrado_CT,
                            serie= var_CT_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

##### Cambio porcentual YoY%
plt_CT_sofipo_pch = plot_st(df = df_filtrado_CT,
                            serie= var_CT_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

plt_CT_sector_pch = plot_st(df = df_filtrado_CT,
                            serie= var_CT_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

###### PANEL ######
panel_CT = make_subplots(rows=2, cols=2,
                      subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                      "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                      vertical_spacing=0.08)

#### Leyendas para cada gráfico
# Traces del primer gráfico → leyenda 1
for trace in plt_CT_sector_i100.data:
    trace.legend = "legend"
    panel_CT.add_trace(trace, row=1, col=1)

# Traces del segundo gráfico → leyenda 2
for trace in plt_CT_sofipo_i100.data:
    trace.legend = "legend2"
    panel_CT.add_trace(trace, row=2, col=1)

# Traces del tercer gráfico → leyenda 3
for trace in plt_CT_sector_pch.data:
    trace.legend = "legend3"
    panel_CT.add_trace(trace, row=1, col=2)

# Traces del cuarto gráfico → leyenda 4
for trace in plt_CT_sofipo_pch.data:
    trace.legend = "legend4"
    panel_CT.add_trace(trace, row=2, col=2)

#### Formato X para cada gráfico
# Replica el formato del eje X en ambas filas
panel_CT.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=1)
panel_CT.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=1)
panel_CT.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=2)
panel_CT.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=2)

#### Formato Y para cada gráfico
panel_CT.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=1, col=1)
panel_CT.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=2, col=1)
panel_CT.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=1, col=2)
panel_CT.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=2, col=2)

# Línea horizontal en 100
panel_CT.add_hline(y=100, line_dash="dash", line_color="black", row=1, col=1)
panel_CT.add_hline(y=100, line_dash="dash", line_color="black", row=2, col=1)
panel_CT.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
panel_CT.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)

# Layout general del panel
panel_CT.update_layout(
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

st.plotly_chart(panel_CT, use_container_width=True)

#################################################################################
#### Segmentos de CT ####
#################################################################################
st.subheader("Captación tradicional por Segmento de Cartera de Crédito")

segmentos = ['Depósitos de exigibilidad inmediata',
             'Depósitos a plazo',
             'Títulos de crédito emitidos',
             'Cuenta global de captación sin movimientos']
segmento = st.selectbox("Segmento de CT", options= segmentos)

st.subheader(f"{segmento}")

#################################################################################
#### Deslizantes - Segmento de CT ####
#################################################################################

##### Periodo ####
var_CT_segmento_i100 = f"{segmento}_i_b100"
var_CT_segmento_pch = f"{segmento}_pct_YoY"
titulo_eje_i100 = f"CT: {segmento} (2023-01 = 100)"
titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

periodo_segmento_CT, df_filtrado_segmento_CT = desl_2var(df = df_CT,
                                 var1= var_CT_segmento_i100,
                                 label1= titulo_eje_i100,
                                 var2= var_CT_segmento_pch,
                                 label2= titulo_eje_pch,
                                 key_prefix=f"segmento_{segmento}"
                                 )

#################################################################################
#### Panel de Segmento de CT indice 100 y pch ####
#################################################################################
###### GRAFICOS ######
##### Indice base == 100
plt_segmento_CT_sofipo_i100 = plot_st(df = df_filtrado_segmento_CT,
                            serie= var_CT_segmento_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

plt_segmento_CT_sector_i100 = plot_st(df = df_filtrado_segmento_CT,
                            serie= var_CT_segmento_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

##### Cambio porcentual YoY%
plt_segmento_CT_sofipo_pch = plot_st(df = df_filtrado_segmento_CT,
                            serie= var_CT_segmento_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

plt_segmento_CT_sector_pch = plot_st(df = df_filtrado_segmento_CT,
                            serie= var_CT_segmento_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

###### PANEL ######
panel_segmento_CT = make_subplots(rows=2, cols=2,
                            subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                            "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                            vertical_spacing=0.08)

#### Leyendas para cada gráfico
# Traces del primer gráfico → leyenda 1
for trace in plt_segmento_CT_sector_i100.data:
    trace.legend = "legend"
    panel_segmento_CT.add_trace(trace, row=1, col=1)

# Traces del segundo gráfico → leyenda 2
for trace in plt_segmento_CT_sofipo_i100.data:
    trace.legend = "legend2"
    panel_segmento_CT.add_trace(trace, row=2, col=1)

# Traces del tercer gráfico → leyenda 3
for trace in plt_segmento_CT_sector_pch.data:
    trace.legend = "legend3"
    panel_segmento_CT.add_trace(trace, row=1, col=2)

# Traces del cuarto gráfico → leyenda 4
for trace in plt_segmento_CT_sofipo_pch.data:
    trace.legend = "legend4"
    panel_segmento_CT.add_trace(trace, row=2, col=2)

#### Formato X para cada gráfico
# Replica el formato del eje X en ambas filas
panel_segmento_CT.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=1)
panel_segmento_CT.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=1)
panel_segmento_CT.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=2)
panel_segmento_CT.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=2)

#### Formato Y para cada gráfico
panel_segmento_CT.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=1, col=1)
panel_segmento_CT.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=2, col=1)
panel_segmento_CT.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=1, col=2)
panel_segmento_CT.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=2, col=2)

# Línea horizontal en 100
panel_segmento_CT.add_hline(y=100, line_dash="dash", line_color="black", row=1, col=1)
panel_segmento_CT.add_hline(y=100, line_dash="dash", line_color="black", row=2, col=1)
panel_segmento_CT.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
panel_segmento_CT.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)

# Layout general del panel
panel_segmento_CT.update_layout(
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

st.plotly_chart(panel_segmento_CT, use_container_width=True)
