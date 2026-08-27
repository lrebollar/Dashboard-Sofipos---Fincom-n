import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st

def desl_periodo(df : pd.DataFrame,
                 key: str = None):

    ##### Periodo ####
    fecha_min = pd.to_datetime('2022-01-01').date()
    fecha_max = df['periodo'].max().date()

    periodo = st.slider(
        "Período",
        min_value=fecha_min,
        max_value=fecha_max,
        value=(fecha_min, fecha_max),  # rango, no un solo valor
        format="YYYY-MM",
        key=key
    )

    # Filtrar el dataframe
    df_filtrado = df[(df['periodo'] >= pd.Timestamp(periodo[0])) & 
                    (df['periodo'] <= pd.Timestamp(periodo[1]))]

    return periodo, df_filtrado

def desl_2var(df : pd.DataFrame,
              var1 : str,
              label1 : str,
              var2 : str,
              label2 : str,
              key_prefix: str = ""):

    periodo, df_filtrado = desl_periodo(df, key=f"{key_prefix}_periodo")

    col1, col2 = st.columns(2)

    with col1:
        rango_i100 = st.slider(
            label1,
            min_value=float(df[var1].min()),
            max_value=float(df[var1].max()),
            value=(float(df[var1].min()), 
                float(df[var1].max())),
            key=f"{key_prefix}_{var1}"
        )

    with col2:
        rango_pch = st.slider(
            label2,
            min_value=float(df[var2].min()),
            max_value=float(df[var2].max()),
            value=(float(df[var2].min()), 
                float(df[var2].max())),
            key=f"{key_prefix}_{var2}"
        )

    df_filtrado = df_filtrado[
        (df_filtrado[var1].between(*rango_i100)) &
        (df_filtrado[var2].between(*rango_pch))
        ]

    return  periodo, df_filtrado

def plot_st(df : pd.DataFrame, 
            serie : str, 
            titulo: str, 
            categorias : str,
            sofipos : list,
            log : bool,
            doble_eje : bool = True,
            eje : str | None = None,
            inicio : str | None = None,
            mostrar : bool = True):

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

__all__ = ['plot_st', 'desl_periodo', 'desl_2var']
