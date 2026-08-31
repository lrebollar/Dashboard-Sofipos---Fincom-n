import pandas as pd
import numpy as np
import os
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pickle

## Llamado de base global SOFIPO
with open('dict_sofipos_sector.pkl', 'rb') as archivo:
    dict_sofipos = pickle.load(archivo)

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

#################################################################################################################
####### Función para crear gráfico de series de tiempo #######
#################################################################################################################
def plot_ln(df : pd.DataFrame, 
            serie : str, 
            titulo: str, 
            categorias : str,
            sofipos : list,
            log : bool,
            doble_eje : bool = True,
            eje : str | None = None,
            inicio : str | None = None,
            mostrar : bool = True):

        import pandas as pd
        import numpy as np
        import plotly.express as px
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots

        # Define el inicio de las series
        if pd.isna(inicio) == False:

            df = df[df['periodo'] >= inicio] 

        # Asegura orden cronológico para que el "último valor" sea correcto
        df = df.sort_values('periodo')

        if log == True:
            # Convierte a logaritmo e la serie
            df[serie] = df[serie].astype(float)
            df[f'{serie}_ln'] = np.log(df[serie])
        
            # Selecciona las sofipos 
            df = df[df['sofipo'].isin(sofipos)]

            y_col = f'{serie}_ln'

        else:
            # Selecciona las sofipos 
            df = df[df['sofipo'].isin(sofipos)]
            y_col = serie
        
        fig_px = px.line(
            df, 
            x="periodo", 
            y=y_col, 
            title= titulo,
            color=categorias)

        if doble_eje:
            # Construye la figura con doble eje
            fig = make_subplots(specs=[[{"secondary_y": True}]])

            for trace in fig_px.data:
                es_total = trace.name in ['Total SOFIPOS', 'Fintech']
                fig.add_trace(trace, secondary_y=not es_total)

            fig.update_layout(
                title=titulo,
                xaxis=dict(
                    title=None,
                    tickformat="%Y",
                    dtick="M12",
                    hoverformat="%Y-%m")
                )
            
            fig.update_yaxes(title_text="Sector SOFIPOS", secondary_y=False)
            fig.update_yaxes(title_text="Otras SOFIPOS", secondary_y=True)

            # Líneas de referencia en y = 100 para cada eje
            fig.add_hline(y=100, line_dash="dash", line_color="black", secondary_y=False)
            fig.add_hline(y=100, line_dash="dash", line_color="darkblue", secondary_y=True)

        else:
            # Figura de un solo eje
            fig = fig_px

            fig.update_layout(
                title=titulo,
                xaxis=dict(
                    title=None,
                    tickformat="%Y",
                    dtick="M12",
                    hoverformat="%Y-%m")
                )

            fig.update_yaxes(
                side="right",
                showticklabels=True,
                title_text= eje
            )

            # Línea de referencia en y = 100
            fig.add_hline(y=100, line_dash="dash", line_color="black")

        # Leyenda dentro del gráfico, esquina superior izquierda
        fig.update_layout(
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

        fig.for_each_trace(actualizar_leyenda)

        if mostrar:
            fig.show()

        return fig