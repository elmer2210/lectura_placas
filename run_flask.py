"""
Punto de entrada de la aplicación Flask.
Ejecutar con: python run_flask.py
"""

import os
import sys

# Agregar directorio del proyecto al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, render_template, request, jsonify
from flask_app.config import config_by_name
from flask_app.services.database_loader import get_database
from flask_app.services.search_service import get_search_service
import re


# Crear aplicación Flask
app = Flask(__name__,
            template_folder='flask_app/templates',
            static_folder='flask_app/static')

# Cargar configuración
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config_by_name[env])

# Cargar base de datos al iniciar
with app.app_context():
    get_database()


# ============================================================================
# RUTAS PRINCIPALES
# ============================================================================

@app.route('/')
def index():
    """Landing page."""
    return render_template('pages/index.html')


@app.route('/peaje')
def peaje():
    """Página principal del simulador de peaje."""
    return render_template('pages/peaje.html')


@app.route('/historial')
def historial():
    """
    Página de historial de vehículos capturados.
    Muestra lista ordenada por algoritmo más rápido con filtro por peaje.
    """
    db = get_database()
    # Obtener lista única de peajes para el filtro
    peajes = db.get_all_vehicles()['peaje_ciudad'].unique().tolist()
    peajes.sort()
    return render_template('pages/historial.html', peajes=peajes)


@app.route('/reportes')
def reportes():
    """
    Página de reportes y análisis estadístico.
    Análisis exploratorio de datos del historial de búsquedas.
    """
    return render_template('pages/reportes.html')


@app.route('/peaje/buscar', methods=['POST'])
def buscar_placa():
    """
    Endpoint que recibe la placa y ejecuta búsqueda comparativa.
    """
    data = request.get_json()
    plate = data.get('placa', '').strip().upper()

    if not plate:
        return jsonify({'success': False, 'error': 'Debe ingresar una placa'}), 400

    # Validar formato (ABC-1234)
    if not re.match(r'^[A-Z]{3}-\d{4}$', plate):
        return jsonify({'success': False, 'error': 'Formato de placa inválido. Use: ABC-1234'}), 400

    # Ejecutar búsqueda
    search_service = get_search_service()
    result = search_service.search_plate(plate)

    # Preparar respuesta
    response = {
        'success': True,
        'found': result['found'],
        'plate': result['plate_searched'],
        'vehicle': result['vehicle'],
        'comparison': {
            'winner': result['winner'],
            'percentage_faster': round(result['percentage_faster'], 2),
            'merge_sort': {
                'total_time': round(result['merge_sort_result']['total_time_ms'], 4),
                'sort_time': round(result['merge_sort_result']['sort_time_ms'], 4),
                'search_time': round(result['merge_sort_result']['search_time_ms'], 4),
                'comparisons': result['merge_sort_result']['total_comparisons']
            },
            'radix_sort': {
                'total_time': round(result['radix_sort_result']['total_time_ms'], 4),
                'sort_time': round(result['radix_sort_result']['sort_time_ms'], 4),
                'search_time': round(result['radix_sort_result']['search_time_ms'], 4),
                'operations': result['radix_sort_result']['sort_operations']
            }
        }
    }

    return jsonify(response)


# ============================================================================
# API REST
# ============================================================================

@app.route('/api/database/stats')
def get_database_stats():
    """Retorna estadísticas de la base de datos."""
    db = get_database()
    stats = db.get_statistics()
    return jsonify({'success': True, 'data': stats})


@app.route('/api/vehicles/random')
def get_random_vehicle():
    """Retorna un vehículo aleatorio (para testing)."""
    db = get_database()
    df = db.get_all_vehicles()
    random_vehicle = df.sample(1).to_dict('records')[0]
    return jsonify({'success': True, 'data': random_vehicle})


@app.route('/api/search/history')
def get_search_history():
    """Retorna historial de búsquedas."""
    limit = request.args.get('limit', 50, type=int)
    peaje_filter = request.args.get('peaje', None)

    search_service = get_search_service()
    history = search_service.get_history(limit)

    # Filtrar por peaje si se especifica
    if peaje_filter and peaje_filter != 'todos':
        history = [h for h in history if h.get('peaje_ciudad') == peaje_filter]

    return jsonify({'success': True, 'data': history})


@app.route('/api/reportes/analisis')
def get_analisis_datos():
    """
    Endpoint para análisis exploratorio de datos del historial.
    Retorna estadísticas agregadas y datos para visualizaciones.
    """
    import pandas as pd
    from collections import Counter

    search_service = get_search_service()
    history = search_service.get_history(10000)  # Obtener todo el historial

    if not history:
        return jsonify({'success': False, 'error': 'No hay datos en el historial'})

    # Convertir a DataFrame para análisis
    df = pd.DataFrame(history)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Extraer componentes de tiempo
    df['hora'] = df['timestamp'].dt.hour
    df['dia_semana'] = df['timestamp'].dt.day_name()
    df['fecha'] = df['timestamp'].dt.date.astype(str)

    # --- ANÁLISIS 1: Top 10 Placas con más Alertas (Suspendida/Bloqueada) ---
    df_alertas = df[df['estado_ANT'].isin(['Suspendida', 'Bloqueada'])]
    top_alertas = df_alertas['plate'].value_counts().head(10).to_dict()

    # Obtener detalles de las placas con alertas
    top_alertas_detalle = []
    for placa, count in list(top_alertas.items())[:10]:
        registros = df_alertas[df_alertas['plate'] == placa]
        top_alertas_detalle.append({
            'placa': placa,
            'total_alertas': int(count),
            'estado': registros.iloc[0]['estado_ANT'],
            'peaje': registros.iloc[0]['peaje_ciudad']
        })

    # --- ANÁLISIS 2: Distribución por Estado ANT ---
    estados_dist = df[df['found'] == True]['estado_ANT'].value_counts().to_dict()

    # --- ANÁLISIS 3: Distribución por Hora del Día ---
    horas_dist = df['hora'].value_counts().sort_index().to_dict()

    # --- ANÁLISIS 4: Distribución por Peaje ---
    peajes_dist = df[df['found'] == True]['peaje_ciudad'].value_counts().to_dict()

    # --- ANÁLISIS 5: Algoritmo Ganador ---
    winner_dist = df['winner'].value_counts().to_dict()

    # --- ANÁLISIS 6: Tasa de Éxito de Búsqueda ---
    tasa_exito = (df['found'].sum() / len(df)) * 100

    # --- ANÁLISIS 7: Tiempos Promedio ---
    tiempo_merge_promedio = df['merge_time'].mean()
    tiempo_radix_promedio = df['radix_time'].mean()

    # --- ANÁLISIS 8: Búsquedas por Día ---
    busquedas_por_dia = df['fecha'].value_counts().sort_index().to_dict()

    # --- ANÁLISIS 9: Top 10 Peajes con Más Capturas ---
    top_peajes = df[df['found'] == True]['peaje_ciudad'].value_counts().head(10).to_dict()

    # Respuesta
    analisis = {
        'success': True,
        'total_busquedas': len(df),
        'tasa_exito': round(tasa_exito, 2),
        'top_alertas': top_alertas_detalle,
        'distribucion_estados': estados_dist,
        'distribucion_horas': horas_dist,
        'distribucion_peajes': peajes_dist,
        'algoritmo_ganador': winner_dist,
        'tiempos_promedio': {
            'merge_sort': round(tiempo_merge_promedio, 4),
            'radix_sort': round(tiempo_radix_promedio, 4)
        },
        'busquedas_por_dia': busquedas_por_dia,
        'top_peajes': top_peajes
    }

    return jsonify(analisis)


# ============================================================================
# MANEJO DE ERRORES
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Página no encontrada'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Error interno del servidor'}), 500


# ============================================================================
# PUNTO DE ENTRADA
# ============================================================================

if __name__ == '__main__':
    print("\n" + "=" * 70)
    print("INICIANDO SISTEMA DE PEAJE INTELIGENTE")
    print("=" * 70)
    print(f"Servidor: http://localhost:5000")
    print(f"Simulador: http://localhost:5000/peaje")
    print(f"Historial: http://localhost:5000/historial")
    print(f"Reportes: http://localhost:5000/reportes")
    print(f"Modo: {env}")
    print("=" * 70 + "\n")

    app.run(host='0.0.0.0', port=5000, debug=(env == 'development'))
