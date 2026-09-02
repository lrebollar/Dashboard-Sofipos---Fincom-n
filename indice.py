import pandas as pd
import numpy as np
import os
import pickle

# Catalogo de SOFIPOS
dir_sofipos = r'C:\Users\lrebollar.e\OneDrive - fincomun.com.mx\Documentos\GitHub\Dashboard Sofipos - Fincomún\cat_instituciones_27.csv'
df_sofipos = pd.read_csv(dir_sofipos, encoding='latin1')
df_sofipos = df_sofipos[['entidad', 'nombre_entidad']]

# Nomenclatura de los datos
dir_dicc = r'C:\Users\lrebollar.e\OneDrive - fincomun.com.mx\Documentos\GitHub\Dashboard Sofipos - Fincomún\cat_conceptos_27.csv'
df_dicc = pd.read_csv(dir_dicc, encoding='latin1')
df_dicc_s = df_dicc[['idconcepto', 'descripcion', 'nivel']]

# Base global SOFIPOs
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