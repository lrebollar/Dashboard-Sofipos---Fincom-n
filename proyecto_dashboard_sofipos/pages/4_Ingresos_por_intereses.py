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
st.subheader("Ingresos por intereses")

# Importar datos
dir_dict_sofipos = r'proyecto_dashboard_sofipos/data/dict_sofipos_sector.pkl' #Cambiar al final

with open(dir_dict_sofipos, 'rb') as archivo:
    dict_sofipos = pickle.load(archivo)

dict_sofipos['fintech'].keys()

## CT de crédito 
df_Ing_int = dict_sofipos['fintech']['Ing_int']
df_Ing_int.columns.to_list()

### Formato de fecha
df_Ing_int['periodo'] = pd.to_datetime(df_Ing_int['periodo'], format='%Y-%m')


#################################################################################
#### Deslizantes - CT ####
#################################################################################
##### Periodo ####
var_Ing_int_i100 = 'Ingresos por intereses_i_b100'
var_Ing_int_pch = 'Ingresos por intereses_pct_YoY'
titulo_eje_i100 = 'Ingresos por intereses (2023-01 = 100)'
titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

periodo_Ing_int, df_filtrado_Ing_int = desl_2var(df = df_Ing_int,
                                 var1= var_Ing_int_i100,
                                 label1= titulo_eje_i100,
                                 var2= var_Ing_int_pch,
                                 label2= titulo_eje_pch,
                                 key_prefix="CT_total"
                                 )

#################################################################################
#### Panel CT indice 100 y pch ####
#################################################################################
###### GRAFICOS ######
##### Indice base == 100
## Setup

plt_Ing_int_sofipo_i100 = plot_st(df = df_filtrado_Ing_int,
                            serie= var_Ing_int_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

plt_Ing_int_sector_i100 = plot_st(df = df_filtrado_Ing_int,
                            serie= var_Ing_int_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

##### Cambio porcentual YoY%
plt_Ing_int_sofipo_pch = plot_st(df = df_filtrado_Ing_int,
                            serie= var_Ing_int_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

plt_Ing_int_sector_pch = plot_st(df = df_filtrado_Ing_int,
                            serie= var_Ing_int_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

###### PANEL ######
panel_Ing_int = make_subplots(rows=2, cols=2,
                      subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                      "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                      vertical_spacing=0.08)

#### Leyendas para cada gráfico
# Traces del primer gráfico → leyenda 1
for trace in plt_Ing_int_sector_i100.data:
    trace.legend = "legend"
    panel_Ing_int.add_trace(trace, row=1, col=1)

# Traces del segundo gráfico → leyenda 2
for trace in plt_Ing_int_sofipo_i100.data:
    trace.legend = "legend2"
    panel_Ing_int.add_trace(trace, row=2, col=1)

# Traces del tercer gráfico → leyenda 3
for trace in plt_Ing_int_sector_pch.data:
    trace.legend = "legend3"
    panel_Ing_int.add_trace(trace, row=1, col=2)

# Traces del cuarto gráfico → leyenda 4
for trace in plt_Ing_int_sofipo_pch.data:
    trace.legend = "legend4"
    panel_Ing_int.add_trace(trace, row=2, col=2)

#### Formato X para cada gráfico
# Replica el formato del eje X en ambas filas
panel_Ing_int.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=1)
panel_Ing_int.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=1)
panel_Ing_int.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=2)
panel_Ing_int.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=2)

#### Formato Y para cada gráfico
panel_Ing_int.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=1, col=1)
panel_Ing_int.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=2, col=1)
panel_Ing_int.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=1, col=2)
panel_Ing_int.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=2, col=2)

# Línea horizontal en 100
panel_Ing_int.add_hline(y=100, line_dash="dash", line_color="black", row=1, col=1)
panel_Ing_int.add_hline(y=100, line_dash="dash", line_color="black", row=2, col=1)
panel_Ing_int.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
panel_Ing_int.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)

# Layout general del panel
panel_Ing_int.update_layout(
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

st.plotly_chart(panel_Ing_int, use_container_width=True)

#################################################################################
#### Segmentos de CT ####
#################################################################################
st.subheader("Ingresos por intereses por concepto")

segmentos = ['Intereses de efectivo y equivalentes de efectivo', 
             'Intereses y rendimientos a favor provenientes de inversiones en instrumentos financieros', 
             'Intereses y rendimientos a favor en operaciones de reporto', 
             'Intereses de cartera de crédito con riesgo de crédito (E1 + E2)', 
             'Intereses de cartera de crédito con riesgo de crédito etapa 3', 
             'Ingresos por cartera de crédito valuada a valor razonable', 
             'Intereses por derechos de cobro adquiridos', 
             'Comisiones por el otorgamiento del crédito', 
             'Efecto por renegociación de cartera de crédito', 
             'Primas por colocación de deuda', 
             'Dividendos de instrumentos financieros que califican como instrumentos financieros de capital', 
             'Utilidad por valorización', 
             'Incremento por actualización de ingresos por intereses ']

segmento = st.selectbox("Concepto", options= segmentos)

st.subheader(f"{segmento}")

#################################################################################
#### Deslizantes - Segmento de CT ####
#################################################################################

##### Periodo ####
var_Ing_int_segmento_i100 = f"{segmento}_i_b100"
var_Ing_int_segmento_pch = f"{segmento}_pct_YoY"
titulo_eje_i100 = f"{segmento} (2023-01 = 100)"
titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

periodo_segmento_Ing_int, df_filtrado_segmento_Ing_int = desl_2var(df = df_Ing_int,
                                 var1= var_Ing_int_segmento_i100,
                                 label1= titulo_eje_i100,
                                 var2= var_Ing_int_segmento_pch,
                                 label2= titulo_eje_pch,
                                 key_prefix=f"segmento_{segmento}"
                                 )

#################################################################################
#### Panel de Segmento de CT indice 100 y pch ####
#################################################################################
###### GRAFICOS ######
##### Indice base == 100
plt_segmento_Ing_int_sofipo_i100 = plot_st(df = df_filtrado_segmento_Ing_int,
                            serie= var_Ing_int_segmento_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

plt_segmento_Ing_int_sector_i100 = plot_st(df = df_filtrado_segmento_Ing_int,
                            serie= var_Ing_int_segmento_i100,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_i100,
                            inicio= '2022-01',
                            mostrar = False)

##### Cambio porcentual YoY%
plt_segmento_Ing_int_sofipo_pch = plot_st(df = df_filtrado_segmento_Ing_int,
                            serie= var_Ing_int_segmento_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

plt_segmento_Ing_int_sector_pch = plot_st(df = df_filtrado_segmento_Ing_int,
                            serie= var_Ing_int_segmento_pch,
                            titulo= '',
                            categorias= 'sofipo',
                            sofipos= ['Total SOFIPOS', 'Fintech'],
                            doble_eje = False,
                            log=False,
                            eje = titulo_eje_pch,
                            inicio= '2022-01',
                            mostrar = False)

###### PANEL ######
panel_segmento_Ing_int = make_subplots(rows=2, cols=2,
                            subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                            "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                            vertical_spacing=0.08)

#### Leyendas para cada gráfico
# Traces del primer gráfico → leyenda 1
for trace in plt_segmento_Ing_int_sector_i100.data:
    trace.legend = "legend"
    panel_segmento_Ing_int.add_trace(trace, row=1, col=1)

# Traces del segundo gráfico → leyenda 2
for trace in plt_segmento_Ing_int_sofipo_i100.data:
    trace.legend = "legend2"
    panel_segmento_Ing_int.add_trace(trace, row=2, col=1)

# Traces del tercer gráfico → leyenda 3
for trace in plt_segmento_Ing_int_sector_pch.data:
    trace.legend = "legend3"
    panel_segmento_Ing_int.add_trace(trace, row=1, col=2)

# Traces del cuarto gráfico → leyenda 4
for trace in plt_segmento_Ing_int_sofipo_pch.data:
    trace.legend = "legend4"
    panel_segmento_Ing_int.add_trace(trace, row=2, col=2)

#### Formato X para cada gráfico
# Replica el formato del eje X en ambas filas
panel_segmento_Ing_int.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=1)
panel_segmento_Ing_int.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=1)
panel_segmento_Ing_int.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=1, col=2)
panel_segmento_Ing_int.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                    row=2, col=2)

#### Formato Y para cada gráfico
panel_segmento_Ing_int.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=1, col=1)
panel_segmento_Ing_int.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_i100,
                    row=2, col=1)
panel_segmento_Ing_int.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=1, col=2)
panel_segmento_Ing_int.update_yaxes(side="right", showticklabels=True,
                    title_text=titulo_eje_pch,
                    row=2, col=2)

# Línea horizontal en 100
panel_segmento_Ing_int.add_hline(y=100, line_dash="dash", line_color="black", row=1, col=1)
panel_segmento_Ing_int.add_hline(y=100, line_dash="dash", line_color="black", row=2, col=1)
panel_segmento_Ing_int.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
panel_segmento_Ing_int.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)

# Layout general del panel
panel_segmento_Ing_int.update_layout(
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

st.plotly_chart(panel_segmento_Ing_int, use_container_width=True)

if segmento == 'Intereses de cartera de crédito con riesgo de crédito (E1 + E2)':

    #################################################################################
    #### Segmentos de Cartera ####
    #################################################################################
    df_Ing_int_E1E2 = dict_sofipos['fintech']['Ing_int_E1E2']
    
    ### Formato de fecha
    df_Ing_int_E1E2['periodo'] = pd.to_datetime(df_Ing_int_E1E2['periodo'], format='%Y-%m')

    st.subheader("Intereses de cartera de crédito con riesgo de crédito (E1 + E2) por Segmento")

    segmentos = ['Créditos comerciales', 'Créditos consumo', 'Créditos vivienda']
    segmento = st.selectbox("Intereses de Cartera (E1 + E2) por Segmento de Ing_int", options= segmentos)

    st.subheader(f"{segmento}")

    #################################################################################
    #### Deslizantes - Segmento de Cartera ####
    #################################################################################

    ##### Periodo ####
    var_segmento_Ing_int_E1E2_i100 = f"{segmento} (E1 + E2)_i_b100"
    var_segmento_Ing_int_E1E2_pch = f"{segmento} (E1 + E2)_pct_YoY"
    titulo_eje_i100 = f"Intereses por segmento: {segmento} (2023-01 = 100)"
    titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

    periodo_segmento_Ing_int_E1E2, df_filtrado_segmento_Ing_int_E1E2 = desl_2var(df = df_Ing_int_E1E2,
                                    var1= var_segmento_Ing_int_E1E2_i100,
                                    label1= titulo_eje_i100,
                                    var2= var_segmento_Ing_int_E1E2_pch,
                                    label2= titulo_eje_pch,
                                    key_prefix=f"segmento_{segmento}"
                                    )

    #################################################################################
    #### Panel de Segmento de Cartera indice 100 y pch ####
    #################################################################################
    ###### GRAFICOS ######
    ##### Indice base == 100
    plt_segmento_Ing_int_E1E2_sofipo_i100 = plot_st(df = df_filtrado_segmento_Ing_int_E1E2,
                                serie= var_segmento_Ing_int_E1E2_i100,
                                titulo= '',
                                categorias= 'sofipo',
                                sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                                doble_eje = False,
                                log=False,
                                eje = titulo_eje_i100,
                                inicio= '2022-01',
                                mostrar = False)

    plt_segmento_Ing_int_E1E2_sector_i100 = plot_st(df = df_filtrado_segmento_Ing_int_E1E2,
                                serie= var_segmento_Ing_int_E1E2_i100,
                                titulo= '',
                                categorias= 'sofipo',
                                sofipos= ['Total SOFIPOS', 'Fintech'],
                                doble_eje = False,
                                log=False,
                                eje = titulo_eje_i100,
                                inicio= '2022-01',
                                mostrar = False)

    ##### Cambio porcentual YoY%
    plt_segmento_Ing_int_E1E2_sofipo_pch = plot_st(df = df_filtrado_segmento_Ing_int_E1E2,
                                serie= var_segmento_Ing_int_E1E2_pch,
                                titulo= '',
                                categorias= 'sofipo',
                                sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                                doble_eje = False,
                                log=False,
                                eje = titulo_eje_pch,
                                inicio= '2022-01',
                                mostrar = False)

    plt_segmento_Ing_int_E1E2_sector_pch = plot_st(df = df_filtrado_segmento_Ing_int_E1E2,
                                serie= var_segmento_Ing_int_E1E2_pch,
                                titulo= '',
                                categorias= 'sofipo',
                                sofipos= ['Total SOFIPOS', 'Fintech'],
                                doble_eje = False,
                                log=False,
                                eje = titulo_eje_pch,
                                inicio= '2022-01',
                                mostrar = False)

    ###### PANEL ######
    panel_segmento_Ing_int_E1E2 = make_subplots(rows=2, cols=2,
                                subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                                "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                                vertical_spacing=0.08)

    #### Leyendas para cada gráfico
    # Traces del primer gráfico → leyenda 1
    for trace in plt_segmento_Ing_int_E1E2_sector_i100.data:
        trace.legend = "legend"
        panel_segmento_Ing_int_E1E2.add_trace(trace, row=1, col=1)

    # Traces del segundo gráfico → leyenda 2
    for trace in plt_segmento_Ing_int_E1E2_sofipo_i100.data:
        trace.legend = "legend2"
        panel_segmento_Ing_int_E1E2.add_trace(trace, row=2, col=1)

    # Traces del tercer gráfico → leyenda 3
    for trace in plt_segmento_Ing_int_E1E2_sector_pch.data:
        trace.legend = "legend3"
        panel_segmento_Ing_int_E1E2.add_trace(trace, row=1, col=2)

    # Traces del cuarto gráfico → leyenda 4
    for trace in plt_segmento_Ing_int_E1E2_sofipo_pch.data:
        trace.legend = "legend4"
        panel_segmento_Ing_int_E1E2.add_trace(trace, row=2, col=2)

    #### Formato X para cada gráfico
    # Replica el formato del eje X en ambas filas
    panel_segmento_Ing_int_E1E2.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                        row=1, col=1)
    panel_segmento_Ing_int_E1E2.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                        row=2, col=1)
    panel_segmento_Ing_int_E1E2.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                        row=1, col=2)
    panel_segmento_Ing_int_E1E2.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                        row=2, col=2)

    #### Formato Y para cada gráfico
    panel_segmento_Ing_int_E1E2.update_yaxes(side="right", showticklabels=True,
                        title_text=titulo_eje_i100,
                        row=1, col=1)
    panel_segmento_Ing_int_E1E2.update_yaxes(side="right", showticklabels=True,
                        title_text=titulo_eje_i100,
                        row=2, col=1)
    panel_segmento_Ing_int_E1E2.update_yaxes(side="right", showticklabels=True,
                        title_text=titulo_eje_pch,
                        row=1, col=2)
    panel_segmento_Ing_int_E1E2.update_yaxes(side="right", showticklabels=True,
                        title_text=titulo_eje_pch,
                        row=2, col=2)

    # Línea horizontal en 100
    panel_segmento_Ing_int_E1E2.add_hline(y=100, line_dash="dash", line_color="black", row=1, col=1)
    panel_segmento_Ing_int_E1E2.add_hline(y=100, line_dash="dash", line_color="black", row=2, col=1)
    panel_segmento_Ing_int_E1E2.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
    panel_segmento_Ing_int_E1E2.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)

    # Layout general del panel
    panel_segmento_Ing_int_E1E2.update_layout(
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

    st.plotly_chart(panel_segmento_Ing_int_E1E2, use_container_width=True)

elif segmento == 'Intereses de cartera de crédito con riesgo de crédito etapa 3':

    #################################################################################
    #### Segmentos de Cartera ####
    #################################################################################
    df_Ing_int_E3 = dict_sofipos['fintech']['Ing_int_E3']
    
    ### Formato de fecha
    df_Ing_int_E3['periodo'] = pd.to_datetime(df_Ing_int_E3['periodo'], format='%Y-%m')

    st.subheader("Intereses de cartera de crédito con riesgo de crédito etapa 3 por Segmento")

    df_Ing_int_E3.columns.to_list()
    segmentos = ['Créditos comerciales', 'Créditos consumo', 'Créditos vivienda']
    segmento = st.selectbox("Intereses de Cartera (E3) por Segmento de Cartera", options= segmentos)

    st.subheader(f"{segmento}")

    #################################################################################
    #### Deslizantes - Segmento de Cartera ####
    #################################################################################

    ##### Periodo ####
    var_segmento_Ing_int_E3_i100 = f"{segmento}_i_b100"
    var_segmento_Ing_int_E3_pch = f"{segmento}_pct_YoY"
    titulo_eje_i100 = f"Intereses por segmento: {segmento} (2023-01 = 100)"
    titulo_eje_pch = 'Tasa de cambio mensual anual (YoY%)'

    periodo_segmento_Ing_int_E3, df_filtrado_segmento_Ing_int_E3 = desl_2var(df = df_Ing_int_E3,
                                    var1= var_segmento_Ing_int_E3_i100,
                                    label1= titulo_eje_i100,
                                    var2= var_segmento_Ing_int_E3_pch,
                                    label2= titulo_eje_pch,
                                    key_prefix=f"segmento_{segmento}"
                                    )

    #################################################################################
    #### Panel de Segmento de Cartera indice 100 y pch ####
    #################################################################################
    ###### GRAFICOS ######
    ##### Indice base == 100
    plt_segmento_Ing_int_E3_sofipo_i100 = plot_st(df = df_filtrado_segmento_Ing_int_E3,
                                serie= var_segmento_Ing_int_E3_i100,
                                titulo= '',
                                categorias= 'sofipo',
                                sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                                doble_eje = False,
                                log=False,
                                eje = titulo_eje_i100,
                                inicio= '2022-01',
                                mostrar = False)

    plt_segmento_Ing_int_E3_sector_i100 = plot_st(df = df_filtrado_segmento_Ing_int_E3,
                                serie= var_segmento_Ing_int_E3_i100,
                                titulo= '',
                                categorias= 'sofipo',
                                sofipos= ['Total SOFIPOS', 'Fintech'],
                                doble_eje = False,
                                log=False,
                                eje = titulo_eje_i100,
                                inicio= '2022-01',
                                mostrar = False)

    ##### Cambio porcentual YoY%
    plt_segmento_Ing_int_E3_sofipo_pch = plot_st(df = df_filtrado_segmento_Ing_int_E3,
                                serie= var_segmento_Ing_int_E3_pch,
                                titulo= '',
                                categorias= 'sofipo',
                                sofipos= ['Fincomún', 'Tamazula', 'Libertad', 'Crediclub'],
                                doble_eje = False,
                                log=False,
                                eje = titulo_eje_pch,
                                inicio= '2022-01',
                                mostrar = False)

    plt_segmento_Ing_int_E3_sector_pch = plot_st(df = df_filtrado_segmento_Ing_int_E3,
                                serie= var_segmento_Ing_int_E3_pch,
                                titulo= '',
                                categorias= 'sofipo',
                                sofipos= ['Total SOFIPOS', 'Fintech'],
                                doble_eje = False,
                                log=False,
                                eje = titulo_eje_pch,
                                inicio= '2022-01',
                                mostrar = False)

    ###### PANEL ######
    panel_segmento_Ing_int_E3 = make_subplots(rows=2, cols=2,
                                subplot_titles=("SECTOR: Índice Base 100", "SECTOR Tasa de Variación mensual anual (YoY%)", 
                                                "SOFIPO: Índice Base 100", "SOFIPO Tasa de Variación mensual anual (YoY%)"),
                                vertical_spacing=0.08)

    #### Leyendas para cada gráfico
    # Traces del primer gráfico → leyenda 1
    for trace in plt_segmento_Ing_int_E3_sector_i100.data:
        trace.legend = "legend"
        panel_segmento_Ing_int_E3.add_trace(trace, row=1, col=1)

    # Traces del segundo gráfico → leyenda 2
    for trace in plt_segmento_Ing_int_E3_sofipo_i100.data:
        trace.legend = "legend2"
        panel_segmento_Ing_int_E3.add_trace(trace, row=2, col=1)

    # Traces del tercer gráfico → leyenda 3
    for trace in plt_segmento_Ing_int_E3_sector_pch.data:
        trace.legend = "legend3"
        panel_segmento_Ing_int_E3.add_trace(trace, row=1, col=2)

    # Traces del cuarto gráfico → leyenda 4
    for trace in plt_segmento_Ing_int_E3_sofipo_pch.data:
        trace.legend = "legend4"
        panel_segmento_Ing_int_E3.add_trace(trace, row=2, col=2)

    #### Formato X para cada gráfico
    # Replica el formato del eje X en ambas filas
    panel_segmento_Ing_int_E3.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                        row=1, col=1)
    panel_segmento_Ing_int_E3.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                        row=2, col=1)
    panel_segmento_Ing_int_E3.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                        row=1, col=2)
    panel_segmento_Ing_int_E3.update_xaxes(title=None, tickformat="%Y", dtick="M12", hoverformat="%Y-%m",
                        row=2, col=2)

    #### Formato Y para cada gráfico
    panel_segmento_Ing_int_E3.update_yaxes(side="right", showticklabels=True,
                        title_text=titulo_eje_i100,
                        row=1, col=1)
    panel_segmento_Ing_int_E3.update_yaxes(side="right", showticklabels=True,
                        title_text=titulo_eje_i100,
                        row=2, col=1)
    panel_segmento_Ing_int_E3.update_yaxes(side="right", showticklabels=True,
                        title_text=titulo_eje_pch,
                        row=1, col=2)
    panel_segmento_Ing_int_E3.update_yaxes(side="right", showticklabels=True,
                        title_text=titulo_eje_pch,
                        row=2, col=2)

    # Línea horizontal en 100
    panel_segmento_Ing_int_E3.add_hline(y=100, line_dash="dash", line_color="black", row=1, col=1)
    panel_segmento_Ing_int_E3.add_hline(y=100, line_dash="dash", line_color="black", row=2, col=1)
    panel_segmento_Ing_int_E3.add_hline(y=0, line_dash="dash", line_color="black", row=1, col=2)
    panel_segmento_Ing_int_E3.add_hline(y=0, line_dash="dash", line_color="black", row=2, col=2)

    # Layout general del panel
    panel_segmento_Ing_int_E3.update_layout(
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

    st.plotly_chart(panel_segmento_Ing_int_E3, use_container_width=True)

