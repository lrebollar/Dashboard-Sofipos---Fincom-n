import pandas as pd
import numpy as np
import os
import streamlit as st
import plotly.graph_objects as go

## Llamado de datos primarios
dir_sofipos = r'C:\Users\lrebollar.e\OneDrive - fincomun.com.mx\Documentos\GitHub\Dashboard Sofipos - Fincomún\cat_instituciones_27.csv'
df_sofipos = pd.read_csv(dir_sofipos, encoding='latin1')
df_sofipos = df_sofipos[['entidad', 'nombre_entidad']]

dir_dicc = r'C:\Users\lrebollar.e\OneDrive - fincomun.com.mx\Documentos\GitHub\Dashboard Sofipos - Fincomún\cat_conceptos_27.csv'
df_dicc = pd.read_csv(dir_dicc, encoding='latin1')
df_dicc_s = df_dicc[['idconcepto', 'descripcion', 'nivel']]

dir_df = r'C:\Users\lrebollar.e\OneDrive - fincomun.com.mx\Documentos\GitHub\Dashboard Sofipos - Fincomún\sh_datos_csv_27\sh_datos_27.csv'
df = pd.read_csv(dir_df)

# Se agregan identificadores de variables
df = pd.merge(left=df, right=df_dicc_s, on ='idconcepto', how='left')

# Se agregan nombres de las SOFIPOS
df = pd.merge(left=df, right=df_sofipos, on ='entidad', how='left')

df = df[['nivel',
         'idconcepto',
         'descripcion',
         'entidad',
         'nombre_entidad',
         'periodo',
         'valor'
         ]]

df['periodo'] = pd.to_datetime(df['periodo'].astype(str), format='%Y%m').dt.to_period('M')

## Datos de Activo por SOFIPO
df_act = df[((df['periodo'] == max(df['periodo'])) & (df['descripcion'] == 'Activo'))]
df_act = df_act[df_act['nombre_entidad'] != 'Total SOFIPOS']

df_act = df_act.sort_values(by='valor', ascending=False)

#Gráfico de Barras para activo por SOFIPO
categorias = df_act['nombre_entidad']
valores = round(df_act['valor']/1000000, 2)

color_base = '#4C72B0'
color_destacado = '#DD8452'
colores = [color_destacado if cat == 'Fincomún' else color_base for cat in categorias]

fig = go.Figure(go.Bar(
    x=valores,
    y=categorias,
    orientation='h',
    marker_color=colores,
    width=0.6,
    text=[f'{v:,.0f}' for v in valores],
    textposition='outside',
    textfont=dict(size=12),
))

fig.update_layout(
    xaxis=dict(
        visible=True,
        title='Activo en MDP',
        showticklabels=False,   # oculta los números
        showgrid=False,
        showline=False,
        zeroline=False,),
    yaxis=dict(title=None, autorange='reversed'),  # reversed para mantener el mismo orden que barh
    plot_bgcolor='white',
    paper_bgcolor='white',
    height=700,
    width=500,
    margin=dict(l=10, r=50, t=20, b=40),
    showlegend=False,
)

fig.update_xaxes(range=[0, max(valores)*1.15])
fig.update_yaxes(showline=False, showgrid=False, zeroline=False)

st.plotly_chart(fig, use_container_width=False)