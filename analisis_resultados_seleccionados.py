# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 16:44:49 2024

@author: HP
"""

#%%
import pandas as pd
import plotly.graph_objects as go
import scipy.stats as stats
import numpy as np

#%% Carga de datos

datos = pd.read_csv("resultados_todas_las_areas.csv", encoding='latin1')

datos_f = datos[datos["Acreditado"]=="S"]

#%% Grafica, histograma por area

# Agrupamos por Area, calculamos la media y los intervalos de confianza al 95%
grupo = datos_f.groupby('Area')['Aciertos']
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
    title='Media de Aciertos (de los seleccionados) por Area con Intervalos de Confianza del 95%',
    xaxis_title='Media de Aciertos',
    yaxis_title='Area'
)

# Guardamos el gráfico como archivo HTML interactivo
fig.write_html("Seleccionado/grafico_aciertos_area_ci.html")

#%% Grafico de puntos, por area

# Filtrar el 10% de los resultados más altos de la columna 'aciertos'
top_10_percent = datos_f[datos_f['Aciertos'] >= datos_f['Aciertos'].quantile(0.90)]

# Agrupar los datos por 'Area'
areas = top_10_percent['Area'].unique()

# Crear la figura
fig = go.Figure()

# Añadir un gráfico de dispersión con jitter para cada área
for i, area in enumerate(areas):  # Enumerar las áreas para asignar un índice numérico
    # Filtrar los datos por área
    datos_f_area = top_10_percent[top_10_percent['Area'] == area]
    
    # Añadir jitter al eje X usando np.random.normal para crear un pequeño desplazamiento
    jitter = np.random.normal(0, 0.1, len(datos_f_area))  # Desplazamiento con media 0 y desviación estándar 0.1
    
    # Añadir un scatter plot para el área actual con jitter
    fig.add_trace(go.Scatter(
        x=np.repeat(i, len(datos_f_area)) + jitter,  # Usamos el índice numérico en lugar del nombre del área
        y=datos_f_area['Aciertos'],  # Valores de aciertos en el eje Y
        mode='markers',  # Mostrar puntos
        name=f'Área {area}',
        marker=dict(size=8, opacity=0.7),  # Tamaño y transparencia de los puntos
    ))

# Actualizar el layout
fig.update_layout(
    title='Distribución de aciertos (de los seleccionados) en el 10% más alto por área con jitter',
    xaxis_title='Área',
    xaxis=dict(
        tickvals=np.arange(len(areas)),  # Posiciones de las áreas en el eje X
        ticktext=areas  # Nombres de las áreas
    ),
    yaxis_title='Aciertos',
    showlegend=False
)

# Guardamos el gráfico como archivo HTML interactivo
fig.write_html("Seleccionado/mejores_area_p.html")

#%% Violin plot por area

# Agrupar los datos por 'Area'
areas = top_10_percent['Area'].unique()

# Crear la figura
fig = go.Figure()

# Añadir un gráfico de violín para cada área
for area in areas:
    # Filtrar los datos por área
    datos_f_area = top_10_percent[top_10_percent['Area'] == area]['Aciertos'].dropna()
    
    # Añadir el gráfico de violín para esta área
    fig.add_trace(go.Violin(
        y=datos_f_area,  # Datos de aciertos
        x=[area] * len(datos_f_area),  # Colocar el área en el eje X
        name=f'Área {area}',  # Nombre del área
        box_visible=True,  # Mostrar caja dentro del violín
        meanline_visible=True,  # Mostrar línea de la media
        points='all',  # Mostrar todos los puntos dentro del violín
        jitter=0.4,  # Desplazamiento aleatorio para los puntos
        marker=dict(opacity=0.6, size=6),  # Tamaño y transparencia de los puntos
    ))

# Actualizar el layout
fig.update_layout(
    title='Distribución de aciertos (Del 10% mas alto de los seleccionados) por área',
    xaxis_title='Área',
    yaxis_title='Aciertos',
    showlegend=False
)

# Guardamos el gráfico como archivo HTML interactivo
fig.write_html("Seleccionado/mejores_area_violin.html")

#%% 

# Contar el número de alumnos por carrera
carrera_counts = top_10_percent['Carrera'].value_counts().reset_index()
carrera_counts.columns = ['Carrera', 'Numero de Alumnos']

# Calcular el porcentaje de alumnos por carrera
total_alumnos = carrera_counts['Numero de Alumnos'].sum()
carrera_counts['Porcentaje de Alumnos'] = (carrera_counts['Numero de Alumnos'] / total_alumnos) * 100

# Crear la figura de barras
fig = go.Figure()

# Añadir el gráfico de barras
fig.add_trace(go.Bar(
    x=carrera_counts['Carrera'],  # Nombres de las carreras en el eje X
    y=carrera_counts['Porcentaje de Alumnos'],  # Porcentaje de alumnos en el eje Y
    marker=dict(color='royalblue'),  # Color de las barras
))

# Actualizar el layout
fig.update_layout(
    title='Porcentaje de aspirantes (Del 10% mas alto de los seleccionados) en cada carrera',
    xaxis_title='Carrera',
    yaxis_title='Porcentaje de Alumnos (%)',
    xaxis_tickangle=-45,  # Rotar las etiquetas del eje X si son largas
    yaxis_ticksuffix='%',  # Añadir el símbolo de porcentaje en el eje Y
    showlegend=False
)

# Guardamos el gráfico como archivo HTML interactivo
fig.write_html("Seleccionado/mejores_por_carrera.html")

#%%

# Crear una figura
fig = go.Figure()

# Añadir un histograma para cada 'Area'
for area in ['Area 3','Area 2', 'Area 1', 'Area 4']:
    # Filtrar los datos para el área actual
    datos_f_area = datos_f[datos_f['Area'] == area]
    
    # Añadir un histograma de la columna 'aciertos' para el área actual
    fig.add_trace(go.Histogram(x=datos_f_area['Aciertos'], name=f'Área {area}', opacity=0.75))

# Actualizar el layout
fig.update_layout(
    barmode='overlay',
    title='Histograma de aciertos (de los seleccionados) por Área',
    xaxis_title='Aciertos',
    yaxis_title='Frecuencia',
    bargap=0.2,  # Ajuste del espacio entre las barras
    bargroupgap=0.1  # Ajuste del espacio entre grupos de barras
)

# Guardamos el gráfico como archivo HTML interactivo
fig.write_html("Seleccionado/histogramas.html")