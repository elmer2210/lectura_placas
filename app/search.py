"""
================================================================================
MÓDULO DE BÚSQUEDA CON ALGORITMOS DE ORDENAMIENTO
================================================================================
Universidad Nacional de Chimborazo
Facultad de Ingeniería - Ciencia de Datos e Inteligencia Artificial
Asignatura: Estructura de Datos

Este módulo implementa búsqueda de placas vehiculares usando dos enfoques:
1. Búsqueda con Merge Sort + Binary Search
2. Búsqueda con Radix Sort + Binary Search

OBJETIVO ACADÉMICO:
Comparar el rendimiento de ambos algoritmos en un caso de uso real:
sistema de peaje con búsqueda de placas en tiempo real.

COMPLEJIDAD TOTAL:
- Merge Sort + Binary Search: O(n log n) + O(log n) = O(n log n)
- Radix Sort + Binary Search: O(d*(n+k)) + O(log n) ≈ O(d*n)

Autores: Juan David Ruiz Jara, Ian Nolivos, Kléver Castillo,
         Estefany Condor, Natasha Nuñez, Elmer Rivadeneira
================================================================================
"""

import time
from typing import Dict, Tuple, List, Optional
from app.sorting import merge_sort, radix_sort


def binary_search(sorted_array: List[Dict], target_plate: str) -> Optional[Dict]:
    """
    Búsqueda binaria en un arreglo ordenado de vehículos.

    TEORÍA:
    -------
    La búsqueda binaria divide el espacio de búsqueda a la mitad en cada
    iteración, logrando complejidad O(log n).

    ALGORITMO:
    1. Comenzar con todo el arreglo
    2. Comparar el elemento del medio con el objetivo
    3. Si es igual: ¡encontrado!
    4. Si es menor: buscar en la mitad derecha
    5. Si es mayor: buscar en la mitad izquierda
    6. Repetir hasta encontrar o agotar elementos

    REQUISITO CRÍTICO: El arreglo DEBE estar ordenado previamente.

    COMPLEJIDAD: O(log n)

    Args:
        sorted_array: Lista de diccionarios ordenada por 'placa'
        target_plate: Placa a buscar (ej: "ABC-1234")

    Returns:
        Dict con información del vehículo, o None si no existe

    Example:
        >>> vehicles = [{'placa': 'AAA-1111'}, {'placa': 'BBB-2222'}]
        >>> result = binary_search(vehicles, 'AAA-1111')
        >>> print(result['placa'])  # 'AAA-1111'
    """
    left = 0
    right = len(sorted_array) - 1
    comparisons = 0

    # Normalizar placa objetivo (sin guión, mayúsculas)
    target_plate = target_plate.replace('-', '').upper()

    # Búsqueda binaria clásica
    while left <= right:
        comparisons += 1
        mid = (left + right) // 2
        mid_plate = sorted_array[mid]['placa'].replace('-', '').upper()

        if mid_plate == target_plate:
            # ¡Encontrado!
            result = sorted_array[mid].copy()
            result['_search_comparisons'] = comparisons
            return result
        elif mid_plate < target_plate:
            # Buscar en mitad derecha
            left = mid + 1
        else:
            # Buscar en mitad izquierda
            right = mid - 1

    # No encontrado
    return None


def search_with_merge_sort(vehicles: List[Dict], target_plate: str) -> Dict:
    """
    Busca una placa usando Merge Sort seguido de Binary Search.

    FLUJO COMPLETO:
    1. Ordenar vehículos con Merge Sort: O(n log n)
    2. Buscar con Binary Search: O(log n)
    3. Complejidad total: O(n log n)

    VENTAJAS DE MERGE SORT:
    - Rendimiento garantizado O(n log n) en TODOS los casos
    - Algoritmo estable (mantiene orden relativo)
    - No depende de la distribución de datos

    DESVENTAJAS:
    - Requiere O(n) espacio auxiliar
    - Overhead de llamadas recursivas
    - Mayor número de comparaciones

    Args:
        vehicles: Lista de diccionarios con datos de vehículos
        target_plate: Placa a buscar

    Returns:
        Dict con métricas detalladas:
        - algorithm: nombre del algoritmo
        - found: si se encontró la placa
        - vehicle: datos del vehículo (si se encontró)
        - sort_time_ms: tiempo de ordenamiento en milisegundos
        - search_time_ms: tiempo de búsqueda en milisegundos
        - total_time_ms: tiempo total
        - sort_comparisons: comparaciones durante ordenamiento
        - search_comparisons: comparaciones durante búsqueda
        - total_comparisons: total de comparaciones
    """
    # PASO 1: Ordenar con Merge Sort
    sort_start = time.perf_counter()
    sorted_vehicles, sort_metrics = merge_sort(vehicles, key='placa')
    sort_end = time.perf_counter()
    sort_time_ms = (sort_end - sort_start) * 1000

    # PASO 2: Buscar con Binary Search
    search_start = time.perf_counter()
    result = binary_search(sorted_vehicles, target_plate)
    search_end = time.perf_counter()
    search_time_ms = (search_end - search_start) * 1000

    # Construir respuesta con métricas completas
    response = {
        'algorithm': 'Merge Sort + Binary Search',
        'found': result is not None,
        'vehicle': result if result else None,
        'sort_time_ms': sort_time_ms,
        'search_time_ms': search_time_ms,
        'total_time_ms': sort_time_ms + search_time_ms,
        'sort_comparisons': sort_metrics['comparisons'],
        'search_comparisons': result['_search_comparisons'] if result else 0,
        'total_comparisons': sort_metrics['comparisons'] + (result['_search_comparisons'] if result else 0),
        'recursive_calls': sort_metrics['recursive_calls']
    }

    return response


def search_with_radix_sort(vehicles: List[Dict], target_plate: str) -> Dict:
    """
    Busca una placa usando Radix Sort seguido de Binary Search.

    FLUJO COMPLETO:
    1. Ordenar vehículos con Radix Sort: O(d*(n+k))
    2. Buscar con Binary Search: O(log n)
    3. Complejidad total: O(d*(n+k))

    VENTAJAS DE RADIX SORT:
    - Complejidad lineal O(d*n) para datos de longitud fija
    - Ideal para placas vehiculares (longitud constante: 7 caracteres)
    - No usa comparaciones, usa conteo
    - Muy eficiente para conjuntos grandes

    DESVENTAJAS:
    - Requiere conocer el rango de valores (0-9, A-Z)
    - Mayor overhead para conjuntos pequeños
    - Requiere espacio adicional O(n+k)

    CASO DE USO IDEAL:
    Radix Sort es perfecto para placas ecuatorianas porque:
    - Longitud fija: ABC-1234 (7 caracteres)
    - Rango conocido: letras A-Z y dígitos 0-9
    - Dataset grande: cientos o miles de vehículos

    Args:
        vehicles: Lista de diccionarios con datos de vehículos
        target_plate: Placa a buscar

    Returns:
        Dict con métricas similares a search_with_merge_sort
    """
    # PASO 1: Ordenar con Radix Sort
    sort_start = time.perf_counter()
    sorted_vehicles, sort_metrics = radix_sort(vehicles, key='placa')
    sort_end = time.perf_counter()
    sort_time_ms = (sort_end - sort_start) * 1000

    # PASO 2: Buscar con Binary Search
    search_start = time.perf_counter()
    result = binary_search(sorted_vehicles, target_plate)
    search_end = time.perf_counter()
    search_time_ms = (search_end - search_start) * 1000

    # Construir respuesta con métricas completas
    response = {
        'algorithm': 'Radix Sort + Binary Search',
        'found': result is not None,
        'vehicle': result if result else None,
        'sort_time_ms': sort_time_ms,
        'search_time_ms': search_time_ms,
        'total_time_ms': sort_time_ms + search_time_ms,
        'sort_operations': sort_metrics['operations'],
        'search_comparisons': result['_search_comparisons'] if result else 0,
        'passes': sort_metrics['passes']
    }

    return response


def comparative_search(vehicles: List[Dict], target_plate: str) -> Dict:
    """
    Realiza búsqueda comparativa usando ambos algoritmos en paralelo.

    Esta es la función principal del sistema de peaje inteligente.
    Ejecuta búsqueda con Merge Sort y Radix Sort simultáneamente
    y compara los resultados para determinar cuál es más eficiente.

    FLUJO DEL SISTEMA DE PEAJE:
    1. Cámara captura placa del vehículo
    2. Sistema ejecuta búsqueda con AMBOS algoritmos
    3. Compara tiempos de ejecución
    4. Retorna información del vehículo + comparativa de rendimiento
    5. Interfaz muestra resultado visual con gráficos

    MÉTRICAS CALCULADAS:
    - Tiempo de cada algoritmo
    - Algoritmo ganador (más rápido)
    - Diferencia de tiempo absoluta
    - Diferencia de tiempo porcentual

    Args:
        vehicles: Lista de vehículos de la base de datos
        target_plate: Placa capturada por la "cámara"

    Returns:
        Dict con:
        - plate_searched: placa buscada
        - found: si se encontró en la base de datos
        - vehicle: datos completos del vehículo (si se encontró)
        - merge_sort_result: resultado completo de Merge Sort
        - radix_sort_result: resultado completo de Radix Sort
        - winner: algoritmo más rápido ('Merge Sort' o 'Radix Sort')
        - time_difference_ms: diferencia de tiempo en milisegundos
        - percentage_faster: porcentaje más rápido del ganador

    Example:
        >>> vehicles = cargar_base_datos()
        >>> result = comparative_search(vehicles, "ABC-1234")
        >>> print(f"Ganador: {result['winner']}")
        >>> print(f"Diferencia: {result['percentage_faster']:.2f}%")
    """
    print(f"🔍 Búsqueda comparativa de placa: {target_plate}")

    # Buscar con ambos algoritmos (copias independientes)
    merge_result = search_with_merge_sort(vehicles.copy(), target_plate)
    radix_result = search_with_radix_sort(vehicles.copy(), target_plate)

    # Extraer tiempos para comparación
    merge_time = merge_result['total_time_ms']
    radix_time = radix_result['total_time_ms']

    # Determinar algoritmo ganador
    if merge_time < radix_time:
        winner = 'Merge Sort'
        time_diff = radix_time - merge_time
        percentage = (time_diff / radix_time) * 100
    else:
        winner = 'Radix Sort'
        time_diff = merge_time - radix_time
        percentage = (time_diff / merge_time) * 100

    # Logging para consola (debugging)
    print(f"   Merge Sort: {merge_time:.4f} ms")
    print(f"   Radix Sort: {radix_time:.4f} ms")
    print(f"   🏆 Ganador: {winner} ({percentage:.2f}% más rápido)")

    # Retornar resultados completos
    return {
        'plate_searched': target_plate,
        'found': merge_result['found'],  # Ambos deben dar el mismo resultado
        'vehicle': merge_result['vehicle'],  # Datos del vehículo
        'merge_sort_result': merge_result,
        'radix_sort_result': radix_result,
        'winner': winner,
        'time_difference_ms': time_diff,
        'percentage_faster': percentage
    }


if __name__ == "__main__":
    # Pruebas del módulo
    print("=" * 70)
    print("PRUEBAS DEL MÓDULO DE BÚSQUEDA")
    print("=" * 70)

    # Crear datos de prueba
    test_vehicles = [
        {'placa': 'XYZ-9999', 'estado_ANT': 'Habilitada'},
        {'placa': 'ABC-1234', 'estado_ANT': 'Suspendida'},
        {'placa': 'MNO-5555', 'estado_ANT': 'Habilitada'},
        {'placa': 'DEF-2222', 'estado_ANT': 'Bloqueada'},
        {'placa': 'AAA-0001', 'estado_ANT': 'Habilitada'},
        {'placa': 'ZZZ-9999', 'estado_ANT': 'Habilitada'},
        {'placa': 'BBB-3333', 'estado_ANT': 'Habilitada'},
    ]

    print(f"\n📊 Dataset de prueba: {len(test_vehicles)} vehículos")

    # Prueba de búsqueda comparativa
    print("\n🔍 Prueba de búsqueda comparativa")
    result = comparative_search(test_vehicles, 'ABC-1234')

    if result['found']:
        print(f"\n✅ Vehículo encontrado:")
        print(f"   Placa: {result['vehicle']['placa']}")
        print(f"   Estado: {result['vehicle']['estado_ANT']}")
    else:
        print(f"\n❌ Vehículo no encontrado")

    print(f"\n📈 Resultados del benchmark:")
    print(f"   Ganador: {result['winner']}")
    print(f"   Diferencia: {result['percentage_faster']:.2f}%")

    print("\n✅ Pruebas completadas")
