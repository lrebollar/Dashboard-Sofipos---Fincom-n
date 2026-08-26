import pandas as pd
import numpy as np
import os
import streamlit as st

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

df_act = df[((df['periodo'] == max(df['periodo'])) & (df['descripcion'] == 'Activo'))]
df_act = df_act[df_act['nombre_entidad'] != 'Total SOFIPOS']

df_act = df_act.sort_values(by='valor')

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

categorias = df_act['nombre_entidad']
valores = round(df_act['valor']/1000000, 2)

# Color especial para Fincomún, color base para las demás
color_base = '#4C72B0'
color_destacado = '#DD8452'
colores = [color_destacado if cat == 'Fincomún' else color_base for cat in categorias]

fig, ax = plt.subplots(figsize=(5, 7))
ax.barh(categorias, valores, color=colores, height=0.6)

# Quitar el recuadro (spines)
for spine in ax.spines.values():
    spine.set_visible(False)

# Ocultar el eje X por completo
ax.xaxis.set_visible(False)

ax.set_xlabel('Activo en MDP')

# Formato con comas en el eje X
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))

# Formato con comas en las etiquetas al final de cada barra
for i, v in enumerate(valores):
    ax.text(v + max(valores)*0.01, i, f'{v:,.0f}', va='center')

# Esta es la única línea nueva que necesitas
st.pyplot(fig)