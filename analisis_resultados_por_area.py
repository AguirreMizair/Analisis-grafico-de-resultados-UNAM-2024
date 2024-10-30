# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 15:57:59 2024

@author: HP
"""

#%%
import pandas as pd
import plotly.graph_objects as go
import scipy.stats as stats
import numpy as np

#%% Carga de datos
Area = 4

# Cargar los datos
datos = pd.read_csv("resultados_todas_las_areas.csv", encoding='latin1')

# Procesar la columna 'Carrera'
datos['Carrera'] = datos['Carrera'].apply(
    lambda x: x.split(': ')[1].split('\n')[0][6:])

datos_f = datos[datos["Area"]==f"Area {Area}"]

#%%  Grafico, histograma del area

# Crear el histograma
fig = go.Figure(data=[go.Histogram(
    x=datos_f['Aciertos'],
    nbinsx=20,
    marker_color='blue',
    marker_line_color='black',
    marker_line_width=1,
    opacity=0.7
)])

# Agregar títulos y etiquetas
fig.update_layout(
    title=f'Histograma de Aciertos del área {Area}',
    xaxis_title='Número de Aciertos',
    yaxis_title='Frecuencia',
    yaxis=dict(showgrid=True, gridcolor='LightGray')
)

# Guardar el gráfico como un archivo HTML
fig.write_html(f"Area_{Area}\histograma_aciertos_area_{Area}.html")

#%% Grafico, histograma carrera en especial

# Carrera = "ACTUARIA"

# datos_f_actuaria = datos_f[datos_f['Carrera'] == Carrera]

# # Crear el histograma
# fig = go.Figure(data=[go.Histogram(
#     x=datos_f_actuaria['Aciertos'],
#     nbinsx=20,
#     marker_color='blue',
#     marker_line_color='black',
#     marker_line_width=1,
#     opacity=0.7
# )])

# # Agregar títulos y etiquetas
# fig.update_layout(
#     title=f'Histograma de Aciertos de {Carrera}',
#     xaxis_title='Número de Aciertos',
#     yaxis_title='Frecuencia',
#     yaxis=dict(showgrid=True, gridcolor='LightGray')
# )

# # Guardar el gráfico como un archivo HTML
# fig.write_html(f"Area_{Area}\histograma_aciertos_{Carrera}.html")


#%% Grafica, promedio de aciertos por carrera ci

# Agrupamos por Carrera, calculamos la media y los intervalos de confianza al 95%
grupo = datos_f.groupby('Carrera')['Aciertos']
media_aciertos = grupo.mean()
std_aciertos = grupo.std()
n = grupo.size()

# Intervalo de confianza al 95% (media ± z * (std / sqrt(n)))
z = stats.norm.ppf(0.975)  # Valor crítico para un intervalo del 95%
ci = z * (std_aciertos / np.sqrt(n))

# Ordenamos de mayor a menor promedio de aciertos
media_aciertos = media_aciertos.sort_values(ascending=True)
ci = ci[media_aciertos.index]  # Ordenamos los intervalos de confianza de la misma manera

# Creamos el gráfico de barras horizontal con intervalos de confianza
fig = go.Figure()

fig.add_trace(go.Bar(
    x=media_aciertos,
    y=media_aciertos.index,
    orientation='h',
    error_x=dict(
        type='data',
        array=ci,  # Intervalos de confianza
        visible=True
    )
))

# Añadimos título y etiquetas
fig.update_layout(
    title=f'Media de Aciertos por Carrera de area {Area} con Intervalos de Confianza del 95%',
    xaxis_title='Media de Aciertos',
    yaxis_title='Carrera'
)

# Guardamos el gráfico como archivo HTML interactivo
fig.write_html(f"Area_{Area}\grafico_aciertos_carrera_area_{Area}_ci.html")

