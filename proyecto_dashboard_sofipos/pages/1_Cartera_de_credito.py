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
st.subheader("Cartera de Crédito")

# Importar datos
dir_dict_sofipos = r'proyecto_dashboard_sofipos/data/dict_sofipos_sector.pkl'

with open(dir_dict_sofipos, 'rb') as archivo:
    dict_sofipos = pickle.load(archivo)


## Cartera de crédito 
df_cartera = dict_sofipos['fintech']['Inf_cartera']
### Formato de fecha
df_cartera['periodo'] = pd.to_datetime(df_cartera['periodo'], format='%Y-%m')


#################################################################################
#### Deslizantes - Cartera ####
#################################################################################
##### Periodo ####
var_cartera_i100 = 'Cartera de crédito_i_b100'
var_cartera_pch = 'Cartera de crédito_pct_YoY'
titulo_eje_i100 = 'Cartera Total de Crédito (2023-01 = 100)'
titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

periodo_cartera, df_filtrado_cartera = desl_2var(df = df_cartera,
                                 var1= var_cartera_i100,
                                 label1= titulo_eje_i100,
                                 var2= var_cartera_pch,
                                 label2= titulo_eje_pch,
                                 key_prefix="cartera_total"
                                 )

#################################################################################
#### Panel Cartera indice 100 y pch ####
#################################################################################
###### GRAFICOS ######
##### Indice base == 100
## Setup

plt_cartera_sofipo_i100 = plot_st(df = df_filtrado_cartera,
                            serie= var_cartera_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

plt_cartera_sector_i100 = plot_st(df = df_filtrado_cartera,
                            serie= var_cartera_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

##### Cambio porcentual YoY%
plt_cartera_sofipo_pch = plot_st(df = df_filtrado_cartera,
                            serie= var_cartera_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

plt_cartera_sector_pch = plot_st(df = df_filtrado_cartera,
                            serie= var_cartera_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

###### PANEL ######
panel_cartera = make_subplots(rows=2, cols=2,
                      subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                      "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                      vertical_spacing=0.08)

#### Leyendas para cada gráfico
# Traces del primer gráfico → leyenda 1
for trace in plt_cartera_sector_i100.data:
    trace.legend = "legend"
    panel_cartera.add_trace(trace, row=1, col=1)

# Traces del segundo gráfico → leyenda 2
for trace in plt_cartera_sofipo_i100.data:
    trace.legend = "legend2"
    panel_cartera.add_trace(trace, row=2, col=1)

# Traces del tercer gráfico → leyenda 3
for trace in plt_cartera_sector_pch.data:
    trace.legend = "legend3"
    panel_cartera.add_trace(trace, row=1, col=2)

# Traces del cuarto gráfico → leyenda 4
for trace in plt_cartera_sofipo_pch.data:
    trace.legend = "legend4"
    panel_cartera.add_trace(trace, row=2, col=2)

#### Formato X para cada gráfico
# Replica el formato del eje X en ambas filas
panel_cartera.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=1)
panel_cartera.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=1)
panel_cartera.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=2)
panel_cartera.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=2)

#### Formato Y para cada gráfico
panel_cartera.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=1, col=1)
panel_cartera.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=2, col=1)
panel_cartera.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=1, col=2)
panel_cartera.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=2, col=2)

# Línea horizontal en 100
panel_cartera.add_hline(y=100, line_dash="dash", line_color="black", row=1, col=1)
panel_cartera.add_hline(y=100, line_dash="dash", line_color="black", row=2, col=1)
panel_cartera.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
panel_cartera.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)

# Layout general del panel
panel_cartera.update_layout(
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

st.plotly_chart(panel_cartera, use_container_width=True)

#################################################################################
#### Segmentos de Cartera ####
#################################################################################
st.subheader("Segmento de Cartera de Crédito")

segmentos = ['Créditos comerciales', 'Créditos consumo', 'Créditos vivienda']
segmento = st.selectbox("Segmento de cartera", options= segmentos)

st.subheader(f"{segmento}")

#################################################################################
#### Deslizantes - Segmento de Cartera ####
#################################################################################

##### Periodo ####
var_segmento_i100 = f"{segmento}_i_b100"
var_segmento_pch = f"{segmento}_pct_YoY"
titulo_eje_i100 = f"Cartera Total de Crédito: {segmento} (2023-01 = 100)"
titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

periodo_segmento_cartera, df_filtrado_segmento_cartera = desl_2var(df = df_cartera,
                                 var1= var_segmento_i100,
                                 label1= titulo_eje_i100,
                                 var2= var_segmento_pch,
                                 label2= titulo_eje_pch,
                                 key_prefix=f"segmento_{segmento}"
                                 )

#################################################################################
#### Panel de Segmento de Cartera indice 100 y pch ####
#################################################################################
###### GRAFICOS ######
##### Indice base == 100
plt_segmento_cartera_sofipo_i100 = plot_st(df = df_filtrado_segmento_cartera,
                            serie= var_segmento_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

plt_segmento_cartera_sector_i100 = plot_st(df = df_filtrado_segmento_cartera,
                            serie= var_segmento_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

##### Cambio porcentual YoY%
plt_segmento_cartera_sofipo_pch = plot_st(df = df_filtrado_segmento_cartera,
                            serie= var_segmento_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

plt_segmento_cartera_sector_pch = plot_st(df = df_filtrado_segmento_cartera,
                            serie= var_segmento_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

###### PANEL ######
panel_segmento_cartera = make_subplots(rows=2, cols=2,
                            subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                            "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                            vertical_spacing=0.08)

#### Leyendas para cada gráfico
# Traces del primer gráfico → leyenda 1
for trace in plt_segmento_cartera_sector_i100.data:
    trace.legend = "legend"
    panel_segmento_cartera.add_trace(trace, row=1, col=1)

# Traces del segundo gráfico → leyenda 2
for trace in plt_segmento_cartera_sofipo_i100.data:
    trace.legend = "legend2"
    panel_segmento_cartera.add_trace(trace, row=2, col=1)

# Traces del tercer gráfico → leyenda 3
for trace in plt_segmento_cartera_sector_pch.data:
    trace.legend = "legend3"
    panel_segmento_cartera.add_trace(trace, row=1, col=2)

# Traces del cuarto gráfico → leyenda 4
for trace in plt_segmento_cartera_sofipo_pch.data:
    trace.legend = "legend4"
    panel_segmento_cartera.add_trace(trace, row=2, col=2)

#### Formato X para cada gráfico
# Replica el formato del eje X en ambas filas
panel_segmento_cartera.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=1)
panel_segmento_cartera.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=1)
panel_segmento_cartera.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=2)
panel_segmento_cartera.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=2)

#### Formato Y para cada gráfico
panel_segmento_cartera.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=1, col=1)
panel_segmento_cartera.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=2, col=1)
panel_segmento_cartera.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=1, col=2)
panel_segmento_cartera.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=2, col=2)

# Línea horizontal en 100
panel_segmento_cartera.add_hline(y=100, line_dash="dash", line_color="black", row=1, col=1)
panel_segmento_cartera.add_hline(y=100, line_dash="dash", line_color="black", row=2, col=1)
panel_segmento_cartera.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
panel_segmento_cartera.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)

# Layout general del panel
panel_segmento_cartera.update_layout(
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

st.plotly_chart(panel_segmento_cartera, use_container_width=True)

#################################################################################
#### Cartera de crédito en E1 + E2 ####
#################################################################################
df_cartera_E1E2 = dict_sofipos['fintech']['Inf_cartera_E1E2']
### Formato de fecha
df_cartera_E1E2['periodo'] = pd.to_datetime(df_cartera_E1E2['periodo'], format='%Y-%m')

st.subheader("Cartera de crédito con riesgo de crédito (E1 + E2)")

df_cartera_E1E2.columns.to_list()
#################################################################################
#### Deslizantes - Cartera de crédito en E1 + E2 ####
#################################################################################

##### Periodo ####
var_E1E2_i100 = 'Cartera de crédito con riesgo de crédito (E1 + E2)_i_b100'
var_E1E2_pch = 'Cartera de crédito con riesgo de crédito (E1 + E2)_pct_YoY'
titulo_eje_i100 = 'Cartera de crédito con riesgo de crédito (E1 + E2) (2023-01 = 100)'
titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

periodo_cartera_E1E2, df_filtrado_cartera_E1E2 = desl_2var(df = df_cartera_E1E2,
                                 var1= var_E1E2_i100,
                                 label1= titulo_eje_i100,
                                 var2= var_E1E2_pch,
                                 label2= titulo_eje_pch,
                                 key_prefix= 'cartera_E1E2'
                                 )

#################################################################################
#### Panel de Segmento de Cartera indice 100 y pch ####
#################################################################################
###### GRAFICOS ######
##### Indice base == 100
plt_cartera_E1E2_sofipo_i100 = plot_st(df = df_filtrado_cartera_E1E2,
                            serie= var_E1E2_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

plt_cartera_E1E2_sector_i100 = plot_st(df = df_filtrado_cartera_E1E2,
                            serie= var_E1E2_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

##### Cambio porcentual YoY%
plt_cartera_E1E2_sofipo_pch = plot_st(df = df_filtrado_cartera_E1E2,
                            serie= var_E1E2_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

plt_cartera_E1E2_sector_pch = plot_st(df = df_filtrado_cartera_E1E2,
                            serie= var_E1E2_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

###### PANEL ######
panel_cartera_E1E2 = make_subplots(rows=2, cols=2,
                            subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                            "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                            vertical_spacing=0.08)

#### Leyendas para cada gráfico
# Traces del primer gráfico → leyenda 1
for trace in plt_cartera_E1E2_sector_i100.data:
    trace.legend = "legend"
    panel_cartera_E1E2.add_trace(trace, row=1, col=1)

# Traces del segundo gráfico → leyenda 2
for trace in plt_cartera_E1E2_sofipo_i100.data:
    trace.legend = "legend2"
    panel_cartera_E1E2.add_trace(trace, row=2, col=1)

# Traces del tercer gráfico → leyenda 3
for trace in plt_cartera_E1E2_sector_pch.data:
    trace.legend = "legend3"
    panel_cartera_E1E2.add_trace(trace, row=1, col=2)

# Traces del cuarto gráfico → leyenda 4
for trace in plt_cartera_E1E2_sofipo_pch.data:
    trace.legend = "legend4"
    panel_cartera_E1E2.add_trace(trace, row=2, col=2)

#### Formato X para cada gráfico
# Replica el formato del eje X en ambas filas
panel_cartera_E1E2.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=1)
panel_cartera_E1E2.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=1)
panel_cartera_E1E2.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=2)
panel_cartera_E1E2.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=2)

#### Formato Y para cada gráfico
panel_cartera_E1E2.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=1, col=1)
panel_cartera_E1E2.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=2, col=1)
panel_cartera_E1E2.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=1, col=2)
panel_cartera_E1E2.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=2, col=2)

# Línea horizontal en 100
panel_cartera_E1E2.add_hline(y=100, line_dash="dash", line_color="black", row=1, col=1)
panel_cartera_E1E2.add_hline(y=100, line_dash="dash", line_color="black", row=2, col=1)
panel_cartera_E1E2.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
panel_cartera_E1E2.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)

# Layout general del panel
panel_cartera_E1E2.update_layout(
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

st.plotly_chart(panel_cartera_E1E2, use_container_width=True)

#################################################################################
#### Cartera de crédito en E1 + E2: Segmentos de Cartera ####
#################################################################################
st.subheader("Segmento de Cartera de Crédito con riesgo de crédito (E1 + E2)")

segmentos_E1E2 = ['Créditos comerciales', 'Créditos consumo', 'Créditos vivienda']
segmento_E1E2 = st.selectbox("Segmento de cartera (E1 + E2)", options= segmentos_E1E2)

st.subheader(f"{segmento_E1E2}")

#################################################################################
#### Deslizantes - Cartera de crédito en E1 + E2 ####
#################################################################################

##### Periodo ####
var_segmento_E1E2_i100 = f'{segmento_E1E2} (E1 + E2)_i_b100'
var_segmento_E1E2_pch = f'{segmento_E1E2} (E1 + E2)_pct_YoY'
titulo_eje_i100 = 'Segmento de Cartera de Crédito con riesgo de crédito (E1 + E2) (2023-01 = 100)'
titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

periodo_segmento_cartera_E1E2, df_filtrado_segmento_cartera_E1E2 = desl_2var(df = df_cartera_E1E2,
                                 var1= var_segmento_E1E2_i100,
                                 label1= titulo_eje_i100,
                                 var2= var_segmento_E1E2_pch,
                                 label2= titulo_eje_pch,
                                 key_prefix= 'segmento_cartera_E1E2'
                                 )

#################################################################################
#### Panel de Segmento de Cartera indice 100 y pch ####
#################################################################################
###### GRAFICOS ######
##### Indice base == 100
plt_segmento_cartera_E1E2_sofipo_i100 = plot_st(df = df_filtrado_segmento_cartera_E1E2,
                            serie= var_segmento_E1E2_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

plt_segmento_cartera_E1E2_sector_i100 = plot_st(df = df_filtrado_segmento_cartera_E1E2,
                            serie= var_segmento_E1E2_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

##### Cambio porcentual YoY%
plt_segmento_cartera_E1E2_sofipo_pch = plot_st(df = df_filtrado_segmento_cartera_E1E2,
                            serie= var_segmento_E1E2_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

plt_segmento_cartera_E1E2_sector_pch = plot_st(df = df_filtrado_segmento_cartera_E1E2,
                            serie= var_segmento_E1E2_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

###### PANEL ######
panel_segmento_cartera_E1E2 = make_subplots(rows=2, cols=2,
                            subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                            "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                            vertical_spacing=0.08)

#### Leyendas para cada gráfico
# Traces del primer gráfico → leyenda 1
for trace in plt_segmento_cartera_E1E2_sector_i100.data:
    trace.legend = "legend"
    panel_segmento_cartera_E1E2.add_trace(trace, row=1, col=1)

# Traces del segundo gráfico → leyenda 2
for trace in plt_segmento_cartera_E1E2_sofipo_i100.data:
    trace.legend = "legend2"
    panel_segmento_cartera_E1E2.add_trace(trace, row=2, col=1)

# Traces del tercer gráfico → leyenda 3
for trace in plt_segmento_cartera_E1E2_sector_pch.data:
    trace.legend = "legend3"
    panel_segmento_cartera_E1E2.add_trace(trace, row=1, col=2)

# Traces del cuarto gráfico → leyenda 4
for trace in plt_segmento_cartera_E1E2_sofipo_pch.data:
    trace.legend = "legend4"
    panel_segmento_cartera_E1E2.add_trace(trace, row=2, col=2)

#### Formato X para cada gráfico
# Replica el formato del eje X en ambas filas
panel_segmento_cartera_E1E2.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=1)
panel_segmento_cartera_E1E2.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=1)
panel_segmento_cartera_E1E2.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=2)
panel_segmento_cartera_E1E2.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=2)

#### Formato Y para cada gráfico
panel_segmento_cartera_E1E2.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=1, col=1)
panel_segmento_cartera_E1E2.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=2, col=1)
panel_segmento_cartera_E1E2.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=1, col=2)
panel_segmento_cartera_E1E2.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=2, col=2)

# Línea horizontal en 100
panel_segmento_cartera_E1E2.add_hline(y=100, line_dash="dash", line_color="black", row=1, col=1)
panel_segmento_cartera_E1E2.add_hline(y=100, line_dash="dash", line_color="black", row=2, col=1)
panel_segmento_cartera_E1E2.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
panel_segmento_cartera_E1E2.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)

# Layout general del panel
panel_segmento_cartera_E1E2.update_layout(
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

st.plotly_chart(panel_segmento_cartera_E1E2, use_container_width=True)

#################################################################################
#### Deslizantes - Cartera de crédito en E3 ####
#################################################################################
df_cartera_E3 = dict_sofipos['fintech']['Inf_cartera_E3']

st.subheader("Cartera de Crédito con riesgo de crédito E3")

### Formato de fecha
df_cartera_E3['periodo'] = pd.to_datetime(df_cartera_E3['periodo'], format='%Y-%m')

var_cartera_E3_i100 = 'Cartera de crédito con riesgo de crédito etapa 3_i_b100'
var_cartera_E3_pch = 'Cartera de crédito con riesgo de crédito etapa 3_pct_YoY'
titulo_eje_i100 = 'Cartera Total de Crédito riesgo de crédito etapa 3 (2023-01 = 100)'
titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

periodo_cartera_E3, df_filtrado_cartera_E3 = desl_2var(df = df_cartera_E3,
                                 var1= var_cartera_E3_i100,
                                 label1= titulo_eje_i100,
                                 var2= var_cartera_E3_pch,
                                 label2= titulo_eje_pch,
                                 key_prefix="cartera_E3_total"
                                 )

#################################################################################
#### Panel Cartera indice 100 y pch ####
#################################################################################
###### GRAFICOS ######
##### Indice base == 100
## Setup

plt_cartera_E3_sofipo_i100 = plot_st(df = df_filtrado_cartera_E3,
                            serie= var_cartera_E3_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

plt_cartera_E3_sector_i100 = plot_st(df = df_filtrado_cartera_E3,
                            serie= var_cartera_E3_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

##### Cambio porcentual YoY%
plt_cartera_E3_sofipo_pch = plot_st(df = df_filtrado_cartera_E3,
                            serie= var_cartera_E3_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

plt_cartera_E3_sector_pch = plot_st(df = df_filtrado_cartera_E3,
                            serie= var_cartera_E3_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

###### PANEL ######
panel_cartera_E3 = make_subplots(rows=2, cols=2,
                      subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                      "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                      vertical_spacing=0.08)

#### Leyendas para cada gráfico
# Traces del primer gráfico → leyenda 1
for trace in plt_cartera_E3_sector_i100.data:
    trace.legend = "legend"
    panel_cartera_E3.add_trace(trace, row=1, col=1)

# Traces del segundo gráfico → leyenda 2
for trace in plt_cartera_E3_sofipo_i100.data:
    trace.legend = "legend2"
    panel_cartera_E3.add_trace(trace, row=2, col=1)

# Traces del tercer gráfico → leyenda 3
for trace in plt_cartera_E3_sector_pch.data:
    trace.legend = "legend3"
    panel_cartera_E3.add_trace(trace, row=1, col=2)

# Traces del cuarto gráfico → leyenda 4
for trace in plt_cartera_E3_sofipo_pch.data:
    trace.legend = "legend4"
    panel_cartera_E3.add_trace(trace, row=2, col=2)

#### Formato X para cada gráfico
# Replica el formato del eje X en ambas filas
panel_cartera_E3.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=1)
panel_cartera_E3.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=1)
panel_cartera_E3.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=2)
panel_cartera_E3.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=2)

#### Formato Y para cada gráfico
panel_cartera_E3.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=1, col=1)
panel_cartera_E3.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=2, col=1)
panel_cartera_E3.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=1, col=2)
panel_cartera_E3.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=2, col=2)

# Línea horizontal en 100
panel_cartera_E3.add_hline(y=100, line_dash="dash", line_color="black", row=1, col=1)
panel_cartera_E3.add_hline(y=100, line_dash="dash", line_color="black", row=2, col=1)
panel_cartera_E3.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
panel_cartera_E3.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)

# Layout general del panel
panel_cartera_E3.update_layout(
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

st.plotly_chart(panel_cartera_E3, use_container_width=True)

#################################################################################
#### Segmentos de Cartera con Cartera de Crédito con riesgo de crédito E3 ####
#################################################################################
st.subheader("Segmento de Cartera de Crédito con riesgo de crédito etapa 3")

segmentos = ['Créditos comerciales', 'Créditos consumo', 'Créditos vivienda']
segmento = st.selectbox("Segmento de cartera con riesgo de crédito etapa 3", 
                        options= segmentos)

st.subheader(f"{segmento}")

#################################################################################
#### Deslizantes - Segmentos de Cartera con Cartera de Crédito con riesgo de crédito E3 ####
#################################################################################

##### Periodo ####
var_segmento_E3_i100 = f"{segmento}_i_b100"
var_segmento_E3_pch = f"{segmento}_pct_YoY"
titulo_eje_i100 = f"Cartera de Crédito con riesgo de crédito E3: {segmento} (2023-01 = 100)"
titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

periodo_segmento_cartera_E3, df_filtrado_segmento_cartera_E3 = desl_2var(df = df_cartera_E3,
                                 var1= var_segmento_E3_i100,
                                 label1= titulo_eje_i100,
                                 var2= var_segmento_E3_pch,
                                 label2= titulo_eje_pch,
                                 key_prefix=f"segmento_E3_{segmento}"
                                 )

#################################################################################
#### Panel de Segmento de Cartera indice 100 y pch ####
#################################################################################
###### GRAFICOS ######
##### Indice base == 100
plt_segmento_cartera_E3_sofipo_i100 = plot_st(df = df_filtrado_segmento_cartera_E3,
                            serie= var_segmento_E3_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

plt_segmento_cartera_E3_sector_i100 = plot_st(df = df_filtrado_segmento_cartera_E3,
                            serie= var_segmento_E3_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

##### Cambio porcentual YoY%
plt_segmento_cartera_E3_sofipo_pch = plot_st(df = df_filtrado_segmento_cartera_E3,
                            serie= var_segmento_E3_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

plt_segmento_cartera_E3_sector_pch = plot_st(df = df_filtrado_segmento_cartera_E3,
                            serie= var_segmento_E3_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

###### PANEL ######
panel_segmento_cartera_E3 = make_subplots(rows=2, cols=2,
                            subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                            "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                            vertical_spacing=0.08)

#### Leyendas para cada gráfico
# Traces del primer gráfico → leyenda 1
for trace in plt_segmento_cartera_E3_sector_i100.data:
    trace.legend = "legend"
    panel_segmento_cartera_E3.add_trace(trace, row=1, col=1)

# Traces del segundo gráfico → leyenda 2
for trace in plt_segmento_cartera_E3_sofipo_i100.data:
    trace.legend = "legend2"
    panel_segmento_cartera_E3.add_trace(trace, row=2, col=1)

# Traces del tercer gráfico → leyenda 3
for trace in plt_segmento_cartera_E3_sector_pch.data:
    trace.legend = "legend3"
    panel_segmento_cartera_E3.add_trace(trace, row=1, col=2)

# Traces del cuarto gráfico → leyenda 4
for trace in plt_segmento_cartera_E3_sofipo_pch.data:
    trace.legend = "legend4"
    panel_segmento_cartera_E3.add_trace(trace, row=2, col=2)

#### Formato X para cada gráfico
# Replica el formato del eje X en ambas filas
panel_segmento_cartera_E3.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=1)
panel_segmento_cartera_E3.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=1)
panel_segmento_cartera_E3.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=2)
panel_segmento_cartera_E3.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=2)

#### Formato Y para cada gráfico
panel_segmento_cartera_E3.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=1, col=1)
panel_segmento_cartera_E3.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=2, col=1)
panel_segmento_cartera_E3.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=1, col=2)
panel_segmento_cartera_E3.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=2, col=2)

# Línea horizontal en 100
panel_segmento_cartera_E3.add_hline(y=100, line_dash="dash", line_color="black", row=1, col=1)
panel_segmento_cartera_E3.add_hline(y=100, line_dash="dash", line_color="black", row=2, col=1)
panel_segmento_cartera_E3.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
panel_segmento_cartera_E3.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)

# Layout general del panel
panel_segmento_cartera_E3.update_layout(
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

st.plotly_chart(panel_segmento_cartera_E3, use_container_width=True)

#################################################################################
#### Castigos, quitas y condonaciones (Suma 12 meses) ####
#################################################################################
st.subheader("Castigos, quitas y condonaciones (Suma 12 meses)")

## Cartera de crédito 
df_castigo = dict_sofipos['fintech']['Castigos']
### Formato de fecha
df_castigo['periodo'] = pd.to_datetime(df_castigo['periodo'], format='%Y-%m')

df_castigo.columns.to_list()
#################################################################################
#### Deslizantes - Cartera ####
#################################################################################
##### Periodo ####
var_castigo_i100 = 'Castigos, quitas y condonaciones (Suma 12 meses)_i_b100'
var_castigo_pch = 'Castigos, quitas y condonaciones (Suma 12 meses)_pct_YoY'
titulo_eje_i100 = 'Castigos, quitas y condonaciones (Suma 12 meses) (2023-01 = 100)'
titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

periodo_castigo, df_filtrado_castigo = desl_2var(df = df_castigo,
                                 var1= var_castigo_i100,
                                 label1= titulo_eje_i100,
                                 var2= var_castigo_pch,
                                 label2= titulo_eje_pch,
                                 key_prefix="castigo_total"
                                 )

#################################################################################
#### Panel Cartera indice 100 y pch ####
#################################################################################
###### GRAFICOS ######
##### Indice base == 100
## Setup

plt_castigo_sofipo_i100 = plot_st(df = df_filtrado_castigo,
                            serie= var_castigo_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

plt_castigo_sector_i100 = plot_st(df = df_filtrado_castigo,
                            serie= var_castigo_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

##### Cambio porcentual YoY%
plt_castigo_sofipo_pch = plot_st(df = df_filtrado_castigo,
                            serie= var_castigo_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

plt_castigo_sector_pch = plot_st(df = df_filtrado_castigo,
                            serie= var_castigo_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

###### PANEL ######
panel_castigo = make_subplots(rows=2, cols=2,
                      subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                      "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                      vertical_spacing=0.08)

#### Leyendas para cada gráfico
# Traces del primer gráfico → leyenda 1
for trace in plt_castigo_sector_i100.data:
    trace.legend = "legend"
    panel_castigo.add_trace(trace, row=1, col=1)

# Traces del segundo gráfico → leyenda 2
for trace in plt_castigo_sofipo_i100.data:
    trace.legend = "legend2"
    panel_castigo.add_trace(trace, row=2, col=1)

# Traces del tercer gráfico → leyenda 3
for trace in plt_castigo_sector_pch.data:
    trace.legend = "legend3"
    panel_castigo.add_trace(trace, row=1, col=2)

# Traces del cuarto gráfico → leyenda 4
for trace in plt_castigo_sofipo_pch.data:
    trace.legend = "legend4"
    panel_castigo.add_trace(trace, row=2, col=2)

#### Formato X para cada gráfico
# Replica el formato del eje X en ambas filas
panel_castigo.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=1)
panel_castigo.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=1)
panel_castigo.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=2)
panel_castigo.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=2)

#### Formato Y para cada gráfico
panel_castigo.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=1, col=1)
panel_castigo.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=2, col=1)
panel_castigo.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=1, col=2)
panel_castigo.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=2, col=2)

# Línea horizontal en 100
panel_castigo.add_hline(y=100, line_dash="dash", line_color="black", row=1, col=1)
panel_castigo.add_hline(y=100, line_dash="dash", line_color="black", row=2, col=1)
panel_castigo.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
panel_castigo.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)

# Layout general del panel
panel_castigo.update_layout(
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

st.plotly_chart(panel_castigo, use_container_width=True)

#################################################################################
#### Segmentos de Cartera ####
#################################################################################
st.subheader("Segmento de Castigos, quitas y condonaciones (Suma 12 meses)")

segmentos = ['Créditos comerciales', 'Créditos consumo', 'Créditos vivienda']
segmento = st.selectbox("Segmento de castigo", options= segmentos)

st.subheader(f"{segmento}")

#################################################################################
#### Deslizantes - Segmento de Cartera ####
#################################################################################

##### Periodo ####
var_segmento_castigo_i100 = f"{segmento}_i_b100"
var_segmento_castigo_pch = f"{segmento}_pct_YoY"
titulo_eje_i100 = f"Segmento de Castigos: {segmento} (2023-01 = 100)"
titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

periodo_segmento_castigo, df_filtrado_segmento_castigo = desl_2var(df = df_castigo,
                                 var1= var_segmento_castigo_i100,
                                 label1= titulo_eje_i100,
                                 var2= var_segmento_castigo_pch,
                                 label2= titulo_eje_pch,
                                 key_prefix=f"segmento_castigo_{segmento}"
                                 )

#################################################################################
#### Panel de Segmento de Cartera indice 100 y pch ####
#################################################################################
###### GRAFICOS ######
##### Indice base == 100
plt_segmento_castigo_sofipo_i100 = plot_st(df = df_filtrado_segmento_castigo,
                            serie= var_segmento_castigo_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

plt_segmento_castigo_sector_i100 = plot_st(df = df_filtrado_segmento_castigo,
                            serie= var_segmento_castigo_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

##### Cambio porcentual YoY%
plt_segmento_castigo_sofipo_pch = plot_st(df = df_filtrado_segmento_castigo,
                            serie= var_segmento_castigo_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

plt_segmento_castigo_sector_pch = plot_st(df = df_filtrado_segmento_castigo,
                            serie= var_segmento_castigo_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

###### PANEL ######
panel_segmento_castigo = make_subplots(rows=2, cols=2,
                            subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                            "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                            vertical_spacing=0.08)

#### Leyendas para cada gráfico
# Traces del primer gráfico → leyenda 1
for trace in plt_segmento_castigo_sector_i100.data:
    trace.legend = "legend"
    panel_segmento_castigo.add_trace(trace, row=1, col=1)

# Traces del segundo gráfico → leyenda 2
for trace in plt_segmento_castigo_sofipo_i100.data:
    trace.legend = "legend2"
    panel_segmento_castigo.add_trace(trace, row=2, col=1)

# Traces del tercer gráfico → leyenda 3
for trace in plt_segmento_castigo_sector_pch.data:
    trace.legend = "legend3"
    panel_segmento_castigo.add_trace(trace, row=1, col=2)

# Traces del cuarto gráfico → leyenda 4
for trace in plt_segmento_castigo_sofipo_pch.data:
    trace.legend = "legend4"
    panel_segmento_castigo.add_trace(trace, row=2, col=2)

#### Formato X para cada gráfico
# Replica el formato del eje X en ambas filas
panel_segmento_castigo.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=1)
panel_segmento_castigo.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=1)
panel_segmento_castigo.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=2)
panel_segmento_castigo.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=2)

#### Formato Y para cada gráfico
panel_segmento_castigo.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=1, col=1)
panel_segmento_castigo.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=2, col=1)
panel_segmento_castigo.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=1, col=2)
panel_segmento_castigo.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=2, col=2)

# Línea horizontal en 100
panel_segmento_castigo.add_hline(y=100, line_dash="dash", line_color="black", row=1, col=1)
panel_segmento_castigo.add_hline(y=100, line_dash="dash", line_color="black", row=2, col=1)
panel_segmento_castigo.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
panel_segmento_castigo.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)

# Layout general del panel
panel_segmento_castigo.update_layout(
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

st.plotly_chart(panel_segmento_castigo, use_container_width=True)