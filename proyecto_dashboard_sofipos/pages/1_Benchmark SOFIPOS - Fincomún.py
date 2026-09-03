import streamlit as st
import pandas as pd
from datetime import date
import numpy as np
import os 
from utils.f_graficos import plot_st, desl_2var
import pickle
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

#### Setup dashboard ####
st.set_page_config(layout="wide")

# Importar datos
dir_dict_sofipos = r'proyecto_dashboard_sofipos/data/dict_sofipos_sector.pkl'
#dir_dict_sofipos = r'C:\Users\lrebollar.e\OneDrive - fincomun.com.mx\Documentos\GitHub\Dashboard Sofipos - Fincomún\proyecto_dashboard_sofipos\data\dict_sofipos_sector.pkl'

with open(dir_dict_sofipos, 'rb') as archivo:
    dict_sofipos = pickle.load(archivo)

## Preparación de las bases
df_indf_original = dict_sofipos['original']['Ind_financieros']
df_indf_fintech = dict_sofipos['fintech']['Ind_financieros']
segmentos = ['ROA', 'ROE', 'Liquidez', 'MIN', 'GAP / Activo', 'Capital contable / Activo',
             'IMOR cartera de crédito', 'IMORA cartera de crédito', 'ICOR cartera de crédito',
             'EPRC / Cartera de crédito', 'Tasa de interés implícita (TII) cartera de crédito E1 + E2', 
             'Tasa de interés implícita (TII) pasiva']

df_indf_fintech[segmentos] = df_indf_fintech[segmentos]*100
df_pasivos_fintech = dict_sofipos['fintech']['Capt_trad']

sele_sofipos = ['Total SOFIPOS', 'Fintech', 'Fincomún']

df_indf_fintech_s = df_indf_fintech[df_indf_fintech['sofipo'].isin(sele_sofipos)]
df_indf_fintech_s['periodo'] = pd.to_datetime(df_indf_fintech_s['periodo'], format='%Y-%m')

fecha_max = df_indf_fintech_s['periodo'].max()
fecha_limite = fecha_max - pd.DateOffset(months=6) 

df_indf_fintech_6m = df_indf_fintech_s[df_indf_fintech_s['periodo'] > fecha_limite].reset_index(drop = True)
df_indf_fintech_6m['periodo'] = df_indf_fintech_6m['periodo'].dt.strftime('%Y-%m') ## Base de trabajo

df_vars_bench = pd.DataFrame({
    'vars_bench' : ['IMOR cartera de crédito', 
                    'IMORA cartera de crédito',
                    'ICOR cartera de crédito',
                    'EPRC / Cartera de crédito'],
    'vars_s' : ['IMOR', 'IMORA', 'ICOR', 'Reservas'] 
})

df_bench = pd.DataFrame(columns=['Variable', 'sofipo', 
                                 '2026-01', '2026-02', 
                                 '2026-03', '2026-04', 
                                 '2026-05', '2026-06', 
                                 'Promedio Histórico'])

for var in df_vars_bench['vars_bench']:
    #var = 'IMOR cartera de crédito'
    var_s = df_vars_bench[df_vars_bench['vars_bench'] == var]['vars_s'].iat[0]

    df_indf_fintech_6m_pivot = df_indf_fintech_6m.pivot(index='sofipo', columns='periodo', values=var).reset_index()
    cols_periodo = df_indf_fintech_6m_pivot.columns.drop('sofipo')

    df_indf_fintech_6m_pivot[cols_periodo] =  (df_indf_fintech_6m_pivot[cols_periodo] * 100).round(2)
    df_indf_fintech_6m_pivot.insert(0, "Variable", var_s)

    # Promedio histórico contemporaneo 
    df_promedio = df_indf_fintech_s[['periodo', 'sofipo',var]]
    df_promedio = df_promedio[df_promedio['periodo'] >= '2023-01-01']
    df_promedio_gb = df_promedio.groupby('sofipo')[var].agg('mean').reset_index()
    df_promedio_gb.columns = ['sofipo', 'Promedio Histórico']
    df_promedio_gb['Promedio Histórico'] = df_promedio_gb['Promedio Histórico']*100

    df_indf_fintech_6m_pivot = pd.merge(left=df_indf_fintech_6m_pivot, right=df_promedio_gb, on='sofipo', how='left')

    df_bench = pd.concat([df_bench, df_indf_fintech_6m_pivot], ignore_index=True)

df_bench['Diferencia vs Histórico'] = df_bench['2026-06'] - df_bench['Promedio Histórico']
######################################################################################################################
# Encabezados 
st.header('Benchmark SOFIPOs - Fincomún (Ene-26 - Jun-26)')
st.subheader('Promedio Histórico: Ene-23 a Jun-26')

### Filtro Por Sofipos 
sofipos_disponibles = df_bench['sofipo'].unique().tolist()

sofipos_seleccionadas = st.multiselect(
    'Filtrar por SOFIPO',
    options=sofipos_disponibles,
    default=sofipos_disponibles  # todas seleccionadas por default
)

#### Filtro aplicado a las Series de tiempo
df_indf_series = df_indf_fintech_s[df_indf_fintech_s['sofipo'].isin(sofipos_seleccionadas)]
df_indf_series = df_indf_series[df_indf_series['periodo'] >= '2024-01-01']

#### Filtro aplicado a la tabla
df_filtrado = df_bench[df_bench['sofipo'].isin(sofipos_seleccionadas)]

vars_col = ['2026-01', '2026-02', 
            '2026-03', '2026-04', 
            '2026-05', '2026-06']

#### Tabla a desplegar: IMOR
df_filtrado_IMOR = df_filtrado[df_filtrado['Variable'] == 'IMOR']
df_filtrado_IMOR = df_filtrado_IMOR.drop(columns='Variable')

st.subheader('IMOR (%)')

st.dataframe(
    data=df_filtrado_IMOR.style
        .format("{:.2f}", subset=vars_col)
        .background_gradient(cmap='OrRd', subset=vars_col, axis=1)
        .background_gradient(cmap='RdBu', subset='Diferencia vs Histórico'),
    use_container_width=True
)

#### Gráfico: IMOR
var_serie = 'IMOR cartera de crédito'
df_indf_series_IMOR = df_indf_series[['periodo', var_serie, 'sofipo']]
df_indf_series_IMOR[var_serie] = df_indf_series_IMOR[var_serie]*100

## Gráfico
mostrar_graficos_imor = st.toggle('Mostrar gráfico histórico', value=True, key='toggle_imor')

if mostrar_graficos_imor:

    fig_IMOR = px.line(
                df_indf_series_IMOR, 
                x="periodo", 
                y=var_serie,
                color='sofipo')

    fig_IMOR.update_layout(
        xaxis=dict(
            title=None,
            tickformat="%Y",
            dtick="M12",
            hoverformat="%Y-%m")
        )


    fig_IMOR.update_yaxes(
        side="right",
        showticklabels=True,
        title_text= f"{var_serie} (%)"
    )

    # Línea de referencia en y = 100
    colores_sofipo = {'Fincomún': 'blue', 'Fintech': 'red', 'Total SOFIPOS': 'black'}
    posiciones = {'Fincomún': 'top left', 'Fintech': 'bottom left', 'Total SOFIPOS': 'top right'}

    for sofipo, color in colores_sofipo.items():
        df_sofipo = df_filtrado[df_filtrado['sofipo'] == sofipo]
        if not df_sofipo.empty:  
            hl_valor = df_sofipo[df_sofipo['Variable'] == 'IMOR']['Promedio Histórico'].iat[0]
            fig_IMOR.add_hline(
                y=hl_valor, 
                line_dash="dash", 
                line_color=color,
                annotation_text=f"{sofipo}: {hl_valor:.2f}",
                annotation_position=posiciones[sofipo],
                annotation_font_color=color
            )


    # Leyenda dentro del gráfico, esquina superior izquierda
    fig_IMOR.update_layout(
        legend=dict(
            title=dict(text="SOFIPO"),
            x=0.01,
            y=0.60,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.6)"
        )
    )

    # Agrega el último valor y fecha a la leyenda de cada serie
    def actualizar_leyenda(trace):
        x_vals = trace.x
        y_vals = trace.y

        if len(x_vals) == 0:
            return

        ultimo_x = pd.to_datetime(x_vals[-1]).strftime('%Y-%m')
        ultimo_y = y_vals[-1]

        trace.update(name=f"{trace.name} | {ultimo_y:.2f} ({ultimo_x})")

    fig_IMOR.for_each_trace(actualizar_leyenda)

    st.plotly_chart(fig_IMOR, use_container_width=True)

#############################################################################################


#### Tabla a desplegar: IMORA
st.subheader('IMORA (%)')

df_filtrado_IMORA = df_filtrado[df_filtrado['Variable'] == 'IMORA']
df_filtrado_IMORA = df_filtrado_IMORA.drop(columns='Variable')

st.dataframe(
    data=df_filtrado_IMORA.style
        .format("{:.2f}", subset=vars_col)
        .background_gradient(cmap='OrRd', subset=vars_col, axis=1)
        .background_gradient(cmap='RdBu', subset='Diferencia vs Histórico'),
    use_container_width=True
)

#### Gráfico: IMORA
var_serie = 'IMORA cartera de crédito'
df_indf_series_IMORA = df_indf_series[['periodo', var_serie, 'sofipo']]
df_indf_series_IMORA[var_serie] = df_indf_series_IMORA[var_serie]*100

## Gráfico
mostrar_graficos_imora = st.toggle('Mostrar gráfico histórico', value=True, key='toggle_imora')

if mostrar_graficos_imora:
    
    fig_IMORA = px.line(
                df_indf_series_IMORA, 
                x="periodo", 
                y=var_serie,
                color='sofipo')

    fig_IMORA.update_layout(
        xaxis=dict(
            title=None,
            tickformat="%Y",
            dtick="M12",
            hoverformat="%Y-%m")
        )


    fig_IMORA.update_yaxes(
        side="right",
        showticklabels=True,
        title_text= f"{var_serie} (%)"
    )

    # Línea de referencia en y = 100
    colores_sofipo = {'Fincomún': 'blue', 'Fintech': 'red', 'Total SOFIPOS': 'black'}
    posiciones = {'Fincomún': 'top left', 'Fintech': 'bottom left', 'Total SOFIPOS': 'top right'}

    for sofipo, color in colores_sofipo.items():
        df_sofipo = df_filtrado[df_filtrado['sofipo'] == sofipo]
        if not df_sofipo.empty:
            hl_valor = df_sofipo[df_sofipo['Variable'] == 'IMORA']['Promedio Histórico'].iat[0]
            fig_IMORA.add_hline(
                y=hl_valor, 
                line_dash="dash", 
                line_color=color,
                annotation_text=f"{sofipo}: {hl_valor:.2f}",
                annotation_position=posiciones[sofipo],
                annotation_font_color=color
            )


    # Leyenda dentro del gráfico, esquina superior izquierda
    fig_IMORA.update_layout(
        legend=dict(
            title=dict(text="SOFIPO"),
            x=0.01,
            y=0.99,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.6)"
        )
    )

    # Agrega el último valor y fecha a la leyenda de cada serie
    def actualizar_leyenda(trace):
        x_vals = trace.x
        y_vals = trace.y

        if len(x_vals) == 0:
            return

        ultimo_x = pd.to_datetime(x_vals[-1]).strftime('%Y-%m')
        ultimo_y = y_vals[-1]

        trace.update(name=f"{trace.name} | {ultimo_y:.2f} ({ultimo_x})")

    fig_IMORA.for_each_trace(actualizar_leyenda)

    st.plotly_chart(fig_IMORA, use_container_width=True)

#############################################################################################

#### Tabla a desplegar: ICOR
st.subheader('ICOR (%)')

df_filtrado_ICOR = df_filtrado[df_filtrado['Variable'] == 'ICOR']
df_filtrado_ICOR = df_filtrado_ICOR.drop(columns='Variable')

st.dataframe(
    data=df_filtrado_ICOR.style
        .format("{:.2f}", subset=vars_col)
        .background_gradient(cmap='OrRd', subset=vars_col, axis=1)
        .background_gradient(cmap='RdBu', subset='Diferencia vs Histórico'),
    use_container_width=True
)

#### Gráfico: ICOR
var_serie = 'ICOR cartera de crédito'
df_indf_series_ICOR = df_indf_series[['periodo', var_serie, 'sofipo']]
df_indf_series_ICOR[var_serie] = df_indf_series_ICOR[var_serie]*100

## Gráfico
mostrar_graficos_icor = st.toggle('Mostrar gráfico histórico', value=True, key='toggle_icor')

if mostrar_graficos_icor:
    
    fig_ICOR = px.line(
                df_indf_series_ICOR, 
                x="periodo", 
                y=var_serie,
                color='sofipo')

    fig_ICOR.update_layout(
        xaxis=dict(
            title=None,
            tickformat="%Y",
            dtick="M12",
            hoverformat="%Y-%m")
        )


    fig_ICOR.update_yaxes(
        side="right",
        showticklabels=True,
        title_text= f"{var_serie} (%)"
    )

    # Línea de referencia en y = 100
    colores_sofipo = {'Fincomún': 'blue', 'Fintech': 'red', 'Total SOFIPOS': 'black'}
    posiciones = {'Fincomún': 'top left', 'Fintech': 'bottom left', 'Total SOFIPOS': 'top right'}

    for sofipo, color in colores_sofipo.items():
        df_sofipo = df_filtrado[df_filtrado['sofipo'] == sofipo]
        if not df_sofipo.empty:
            hl_valor = df_sofipo[df_sofipo['Variable'] == 'ICOR']['Promedio Histórico'].iat[0]
            fig_ICOR.add_hline(
                y=hl_valor, 
                line_dash="dash", 
                line_color=color,
                annotation_text=f"{sofipo}: {hl_valor:.2f}",
                annotation_position=posiciones[sofipo],
                annotation_font_color=color
            )


    # Leyenda dentro del gráfico, esquina superior izquierda
    fig_ICOR.update_layout(
        legend=dict(
            title=dict(text="SOFIPO"),
            x=0.01,
            y=0.99,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.6)"
        )
    )

    # Agrega el último valor y fecha a la leyenda de cada serie
    def actualizar_leyenda(trace):
        x_vals = trace.x
        y_vals = trace.y

        if len(x_vals) == 0:
            return

        ultimo_x = pd.to_datetime(x_vals[-1]).strftime('%Y-%m')
        ultimo_y = y_vals[-1]

        trace.update(name=f"{trace.name} | {ultimo_y:.2f} ({ultimo_x})")

    fig_ICOR.for_each_trace(actualizar_leyenda)

    st.plotly_chart(fig_ICOR, use_container_width=True)

#############################################################################################

#### Tabla a desplegar: Reservas
st.subheader('Reservas (%)')

df_filtrado_Reservas = df_filtrado[df_filtrado['Variable'] == 'Reservas']
df_filtrado_Reservas = df_filtrado_Reservas.drop(columns='Variable')

st.dataframe(
    data=df_filtrado_Reservas.style
        .format("{:.2f}", subset=vars_col)
        .background_gradient(cmap='OrRd', subset=vars_col, axis=1)
        .background_gradient(cmap='RdBu', subset='Diferencia vs Histórico'),
    use_container_width=True
)

#### Gráfico: Reservas
var_serie = 'EPRC / Cartera de crédito'
df_indf_series_RESERVAS = df_indf_series[['periodo', var_serie, 'sofipo']]
df_indf_series_RESERVAS[var_serie] = df_indf_series_RESERVAS[var_serie]*100

## Gráfico
mostrar_graficos_reservas = st.toggle('Mostrar gráfico histórico', value=True, key='toggle_reservas')

if mostrar_graficos_reservas:
    
    fig_RESERVAS = px.line(
                df_indf_series_RESERVAS, 
                x="periodo", 
                y=var_serie,
                color='sofipo')

    fig_RESERVAS.update_layout(
        xaxis=dict(
            title=None,
            tickformat="%Y",
            dtick="M12",
            hoverformat="%Y-%m")
        )


    fig_RESERVAS.update_yaxes(
        side="right",
        showticklabels=True,
        title_text= f"{var_serie} (%)"
    )

    # Línea de referencia en y = 100
    colores_sofipo = {'Fincomún': 'blue', 'Fintech': 'red', 'Total SOFIPOS': 'black'}
    posiciones = {'Fincomún': 'top left', 'Fintech': 'bottom left', 'Total SOFIPOS': 'top right'}

    for sofipo, color in colores_sofipo.items():
        df_sofipo = df_filtrado[df_filtrado['sofipo'] == sofipo]
        if not df_sofipo.empty:
            hl_valor = df_sofipo[df_sofipo['Variable'] == 'Reservas']['Promedio Histórico'].iat[0]
            fig_RESERVAS.add_hline(
                y=hl_valor, 
                line_dash="dash", 
                line_color=color,
                annotation_text=f"{sofipo}: {hl_valor:.2f}",
                annotation_position=posiciones[sofipo],
                annotation_font_color=color
            )


    # Leyenda dentro del gráfico, esquina superior izquierda
    fig_RESERVAS.update_layout(
        legend=dict(
            title=dict(text="SOFIPO"),
            x=0.01,
            y=0.60,
            xanchor="left",
            yanchor="top",
            bgcolor="rgba(255,255,255,0.6)"
        )
    )

    # Agrega el último valor y fecha a la leyenda de cada serie
    def actualizar_leyenda(trace):
        x_vals = trace.x
        y_vals = trace.y

        if len(x_vals) == 0:
            return

        ultimo_x = pd.to_datetime(x_vals[-1]).strftime('%Y-%m')
        ultimo_y = y_vals[-1]

        trace.update(name=f"{trace.name} | {ultimo_y:.2f} ({ultimo_x})")

    fig_RESERVAS.for_each_trace(actualizar_leyenda)

    st.plotly_chart(fig_RESERVAS, use_container_width=True)

#############################################################################################
#### Gráfico Indicadores Financieros ########################################################

df_indf_fintech_p = df_indf_fintech.copy()
### Formato de fecha
df_indf_fintech_p['periodo'] = pd.to_datetime(df_indf_fintech_p['periodo'], format='%Y-%m')
df_indf_fintech_p = df_indf_fintech_p[df_indf_fintech_p['periodo'] >= '2024-01-01']

### Selector
segmento = st.selectbox("Segmento de CT", options= segmentos)
st.subheader(f"{segmento}")

### Base seleccionada
df_segmento = df_indf_fintech_p[['periodo', segmento, 'sofipo']] 

v_periodo = df_segmento[df_segmento['sofipo'] == 'Fincomún']['periodo']
v_segmento_finco = df_segmento[df_segmento['sofipo'] == 'Fincomún'][segmento]
v_segmento_sofipos = df_segmento[df_segmento['sofipo'] == 'Total SOFIPOS'][segmento]

fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Scatter(
        x=v_periodo,
        y=v_segmento_finco,
        mode="lines+markers",
        name=f"Fincomun ({v_segmento_finco.iloc[-1]:.1f}%)",
        line=dict(color="blue", width=2)
    ),
    secondary_y=True
)

fig.add_trace(
    go.Scatter(
        x=v_periodo,
        y=v_segmento_sofipos,
        mode="lines+markers",
        name=f"SOFIPOS ({v_segmento_sofipos.iloc[-1]:.1f}%)",
        line=dict(color="black", width=2)
    ),
    secondary_y=True
)


fig.update_layout(
    barmode="group",
    title=f"{segmento} (%)",
    xaxis_title="Fecha",
    legend=dict(
        x=0.01,
        y=0.99,
        xanchor="left",
        yanchor="top",
        bgcolor="rgba(255,255,255,0.6)",
        bordercolor="rgba(0,0,0,0.2)",
        borderwidth=1
    ),
    template="plotly_white"
)

fig.update_xaxes(tickformat="%b %Y")
fig.update_yaxes(title_text=f"{segmento} (%)", secondary_y=True)

st.plotly_chart(fig, use_container_width=True)

#############################################################################################
#### Panel Pasivo / Captación ###############################################################
df_pasivo = df_pasivos_fintech[['periodo', 'Pasivo', 'Captación tradicional', 'sofipo']]
df_pasivo['periodo'] = pd.to_datetime(df_pasivo['periodo'], format='%Y-%m')
df_pasivo = df_pasivo[df_pasivo['periodo'] >= '2024-01-01']

df_pasivo['Pasivo'] = df_pasivo['Pasivo']/1000000
df_pasivo['Captación tradicional'] = df_pasivo['Captación tradicional']/1000000

# --- Datos: Total SOFIPOS ---
v_periodo_1 = df_pasivo[df_pasivo['sofipo'] == 'Total SOFIPOS']['periodo']
v_captacion_1 = df_pasivo[df_pasivo['sofipo'] == 'Total SOFIPOS']['Captación tradicional']
v_pasivo_1 = df_pasivo[df_pasivo['sofipo'] == 'Total SOFIPOS']['Pasivo']
v_ind_1 = (v_pasivo_1 / v_captacion_1) * 100

# --- Datos: Fincomún ---
v_periodo_2 = df_pasivo[df_pasivo['sofipo'] == 'Fincomún']['periodo']
v_captacion_2 = df_pasivo[df_pasivo['sofipo'] == 'Fincomún']['Captación tradicional']
v_pasivo_2 = df_pasivo[df_pasivo['sofipo'] == 'Fincomún']['Pasivo']
v_ind_2 = (v_pasivo_2 / v_captacion_2) * 100

fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"secondary_y": True}, {"secondary_y": True}]],
    subplot_titles=("Total SOFIPOS", "Fincomún"),
    horizontal_spacing=0.1
)

# ---- Columna 1: Total SOFIPOS ----
fig.add_trace(go.Bar(
    x=v_periodo_1, y=v_captacion_1,
    name=f"Captación Tradicional ({v_captacion_1.iloc[-1]:,.1f})",
    marker_color="#636EFA",
    legend="legend"
), row=1, col=1, secondary_y=False)

fig.add_trace(go.Bar(
    x=v_periodo_1, y=v_pasivo_1,
    name=f"Pasivo ({v_pasivo_1.iloc[-1]:,.1f})",
    marker_color="#EF553B",
    legend="legend"
), row=1, col=1, secondary_y=False)

fig.add_trace(go.Scatter(
    x=v_periodo_1, y=v_ind_1,
    name=f"Pasivo / Captación ({v_ind_1.iloc[-1]:.1f}%)",
    mode="lines+markers", line=dict(color="black", width=2),
    legend="legend"
), row=1, col=1, secondary_y=True)

# ---- Columna 2: Fincomún ----
fig.add_trace(go.Bar(
    x=v_periodo_2, y=v_captacion_2,
    name=f"Captación Tradicional ({v_captacion_2.iloc[-1]:,.1f})",
    marker_color="#636EFA",
    legend="legend2"
), row=1, col=2, secondary_y=False)

fig.add_trace(go.Bar(
    x=v_periodo_2, y=v_pasivo_2,
    name=f"Pasivo ({v_pasivo_2.iloc[-1]:,.1f})",
    marker_color="#EF553B",
    legend="legend2"
), row=1, col=2, secondary_y=False)

fig.add_trace(go.Scatter(
    x=v_periodo_2, y=v_ind_2,
    name=f"Pasivo / Captación ({v_ind_2.iloc[-1]:.1f}%)",
    mode="lines+markers", line=dict(color="black", width=2),
    legend="legend2"
), row=1, col=2, secondary_y=True)

# ---- Layout general ----
fig.update_layout(
    barmode="group",
    title="Captación/Pasivo - SOFIPOS",
    template="plotly_white",
    height=500,
    width=1200,
    legend=dict(
        x=0.01, y=0.99, xanchor="left", yanchor="top",
        bgcolor="rgba(255,255,255,0.6)", bordercolor="rgba(0,0,0,0.2)", borderwidth=1
    ),
    legend2=dict(
        x=0.55, y=0.99, xanchor="left", yanchor="top",
        bgcolor="rgba(255,255,255,0.6)", bordercolor="rgba(0,0,0,0.2)", borderwidth=1
    )
)

fig.update_xaxes(tickformat="%b %Y")
fig.update_yaxes(title_text="Monto en MDP ($)", row=1, col=1, secondary_y=False)
fig.update_yaxes(title_text="Pasivo / Captación (%)", row=1, col=1, secondary_y=True)
fig.update_yaxes(title_text="Monto en MDP ($)", row=1, col=2, secondary_y=False)
fig.update_yaxes(title_text="Pasivo / Captación (%)", row=1, col=2, secondary_y=True)

st.plotly_chart(fig, use_container_width=True)

#############################################################################################
#### ROA - ROE ###############################################################

'ROA', 'ROE'
# --- Datos: Total SOFIPOS ---
v_periodo_1 = df_indf_fintech_p[df_indf_fintech_p['sofipo'] == 'Total SOFIPOS']['periodo']
v_ROA_1 = df_indf_fintech_p[df_indf_fintech_p['sofipo'] == 'Total SOFIPOS']['ROA']
v_ROE_1 = df_indf_fintech_p[df_indf_fintech_p['sofipo'] == 'Total SOFIPOS']['ROE']

# --- Datos: Fincomún ---
v_periodo_2 = df_indf_fintech_p[df_indf_fintech_p['sofipo'] == 'Fincomún']['periodo']
v_ROA_2 = df_indf_fintech_p[df_indf_fintech_p['sofipo'] == 'Fincomún']['ROA']
v_ROE_2 = df_indf_fintech_p[df_indf_fintech_p['sofipo'] == 'Fincomún']['ROE']

fig = make_subplots(
    rows=1, cols=2,
    specs=[[{"secondary_y": True}, {"secondary_y": True}]],
    subplot_titles=("Total SOFIPOS", "Fincomún"),
    horizontal_spacing=0.1
)

# ---- Columna 1: Total SOFIPOS ----
fig.add_trace(go.Scatter(
    x=v_periodo_1, y=v_ROA_1,
    name=f"ROA ({v_ROA_1.iloc[-1]:.1f}%)",
    mode="lines+markers", line=dict(color="gold", width=2),
    legend="legend"
), row=1, col=1, secondary_y=True)

fig.add_trace(go.Scatter(
    x=v_periodo_1, y=v_ROE_1,
    name=f"ROE ({v_ROE_1.iloc[-1]:.1f}%)",
    mode="lines+markers", line=dict(color="blue", width=2),
    legend="legend"
), row=1, col=1, secondary_y=True)

# ---- Columna 2: Fincomún ----
fig.add_trace(go.Scatter(
    x=v_periodo_2, y=v_ROA_2,
    name=f"ROA ({v_ROA_2.iloc[-1]:.1f}%)",
    mode="lines+markers", line=dict(color="gold", width=2),
    legend="legend"
), row=1, col=2, secondary_y=True)

fig.add_trace(go.Scatter(
    x=v_periodo_2, y=v_ROE_2,
    name=f"ROE ({v_ROE_2.iloc[-1]:.1f}%)",
    mode="lines+markers", line=dict(color="blue", width=2),
    legend="legend"
), row=1, col=2, secondary_y=True)

# ---- Layout general ----
fig.update_layout(
    barmode="group",
    title="ROA - ROE",
    template="plotly_white",
    height=500,
    width=1200,
    legend=dict(
        x=0.01, y=0.99, xanchor="left", yanchor="top",
        bgcolor="rgba(255,255,255,0.6)", bordercolor="rgba(0,0,0,0.2)", borderwidth=1
    ),
    legend2=dict(
        x=0.55, y=0.99, xanchor="left", yanchor="top",
        bgcolor="rgba(255,255,255,0.6)", bordercolor="rgba(0,0,0,0.2)", borderwidth=1
    )
)

fig.update_xaxes(tickformat="%b %Y")
fig.update_yaxes(title_text="(%)", row=1, col=1, secondary_y=True)
fig.update_yaxes(title_text="(%)", row=1, col=2, secondary_y=True)

st.plotly_chart(fig, use_container_width=True)