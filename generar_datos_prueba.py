"""
Script para generar datos de prueba en el historial de búsquedas.
Genera aproximadamente 100 búsquedas simuladas con variedad de casos.
"""

import json
import random
from datetime import datetime, timedelta
import pandas as pd

# Cargar base de datos de vehículos
df = pd.read_csv('data/placas_database.csv')

# Preparar lista de historial
historial = []

# Generar 100 búsquedas simuladas
num_busquedas = 100
fecha_inicio = datetime.now() - timedelta(days=7)  # Últimos 7 días

for i in range(num_busquedas):
    # Timestamp aleatorio en los últimos 7 días
    offset_minutos = random.randint(0, 7 * 24 * 60)
    timestamp = fecha_inicio + timedelta(minutes=offset_minutos)

    # Seleccionar vehículo aleatorio (90% encontrado, 10% no encontrado)
    encontrado = random.random() < 0.9

    if encontrado:
        vehiculo = df.sample(1).iloc[0]
        placa = vehiculo['placa']
        peaje_ciudad = vehiculo['peaje_ciudad']
        estado_ant = vehiculo['estado_ANT']
        ubicacion_camara = vehiculo['ubicacion_camara']
    else:
        # Placa no encontrada (inventada)
        letras = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
        numeros = ''.join(random.choices('0123456789', k=4))
        placa = f"{letras}-{numeros}"
        peaje_ciudad = None
        estado_ant = None
        ubicacion_camara = None

    # Simular tiempos de ejecución basados en resultados REALES
    # Según pruebas: Merge Sort ~10ms, Radix Sort ~16ms
    # Merge Sort es MÁS RÁPIDO que Radix Sort (aproximadamente 40% más rápido)

    # Merge Sort: 8-12ms (promedio ~10ms)
    merge_time = round(random.uniform(8.0, 12.0), 4)

    # Radix Sort: 14-19ms (promedio ~16.5ms, siempre más lento que Merge)
    # Aseguramos que sea al menos 30% más lento que Merge Sort
    radix_time = round(merge_time * random.uniform(1.4, 1.8), 4)

    # Merge Sort SIEMPRE gana (es más rápido)
    winner = "Merge Sort"

    # Crear entrada de historial
    entrada = {
        'timestamp': timestamp.isoformat(),
        'plate': placa,
        'found': encontrado,
        'winner': winner,
        'merge_time': merge_time,
        'radix_time': radix_time,
        'peaje_ciudad': peaje_ciudad,
        'estado_ANT': estado_ant,
        'ubicacion_camara': ubicacion_camara
    }

    historial.append(entrada)

# Ordenar por timestamp
historial.sort(key=lambda x: x['timestamp'])

# Guardar en archivo JSON
with open('data/search_history.json', 'w', encoding='utf-8') as f:
    json.dump(historial, f, indent=2, ensure_ascii=False)

print(f"Generados {len(historial)} registros de busqueda")
print(f"Encontrados: {sum(1 for h in historial if h['found'])}")
print(f"No encontrados: {sum(1 for h in historial if not h['found'])}")
print(f"Guardado en: data/search_history.json")

# Estadísticas adicionales
estados = [h['estado_ANT'] for h in historial if h['estado_ANT']]
print(f"\nDistribucion de estados ANT:")
for estado in set(estados):
    count = estados.count(estado)
    print(f"   - {estado}: {count}")

peajes = [h['peaje_ciudad'] for h in historial if h['peaje_ciudad']]
print(f"\nTotal de peajes unicos: {len(set(peajes))}")
