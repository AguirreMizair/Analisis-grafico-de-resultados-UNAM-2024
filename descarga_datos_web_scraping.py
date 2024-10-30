# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 15:33:15 2024

@author: HP
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv


# Función para extraer la tabla de una página
def extraer_datos_tabla(url):
    # Encabezado de User-Agent para simular un navegador
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Solicitud a la página web
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        # Parseamos el HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Inicializamos una lista para guardar los datos
        datos = []
        
        carrera = soup.find('h2').get_text(strip=True)
        
        # Buscamos todas las filas de la tabla
        filas = soup.find_all('tr')
        
        for fila in filas:
            # Buscamos todas las celdas <td> en la fila
            celdas = fila.find_all('td')
            
            # Si hay suficientes celdas, tomamos "Aciertos" y "Acreditado"
            if len(celdas) >= 3:
                aciertos = celdas[1].get_text(strip=True)  # Columna "Aciertos"
                acreditado = celdas[2].get_text(strip=True)  # Columna "Acreditado"
                
                # Guardamos la información
                datos.append({
                    "Carrera": carrera,
                    "Aciertos": aciertos,
                    "Acreditado": acreditado
                })
        
        return datos
    else:
        print(f"Error al acceder a la página {url}: Status code {response.status_code}")
        return []



with open('resultados_todas_las_areas.csv', mode='w', newline='') as file:
    # Definimos las columnas del CSV
    writer = csv.DictWriter(file, fieldnames=["Facultad", "Carrera", "Aciertos", "Acreditado", "Area"])
    writer.writeheader()

    # Iteramos sobre las áreas
    for Area in range(1, 5):
        # URL principal para cada área
        base_url = f"https://www.dgae.unam.mx/Licenciatura2024/resultados/{Area}5.html"
        
        # Encabezado de User-Agent para simular un navegador
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Solicitud a la página principal
        response = requests.get(base_url, headers=headers)
        
        if response.status_code == 200:
            # Parseamos el HTML de la página principal
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscamos todas las etiquetas <a> dentro de los <p> con clase 'post-meta'
            enlaces = soup.find_all('p', class_='post-meta')
            
            # Recorremos los enlaces y accedemos a las subpáginas
            for enlace in enlaces:
                # Buscamos todas las etiquetas <a> dentro de cada <p>
                links = enlace.find_all('a')
                
                for link in links:
                    facultad = link.get_text(strip=True)  # Nombre de la facultad
                    relative_url = link['href']
                    full_url = urljoin(base_url, relative_url)
                    datos = extraer_datos_tabla(full_url)
                    
                    for dato in datos:
                        # Añadimos la facultad y el área a los datos
                        dato['Facultad'] = facultad
                        dato['Area'] = f"Area {Area}"  # Añadimos el número del área
                        writer.writerow(dato)
        
        else:
            print(f"Error al acceder a la página principal: Status code {response.status_code}")