"""
================================================================================
MÓDULO DE ALGORITMOS DE ORDENAMIENTO
================================================================================
Universidad Nacional de Chimborazo
Facultad de Ingeniería - Ciencia de Datos e Inteligencia Artificial
Asignatura: Estructura de Datos

Este módulo implementa los algoritmos de ordenamiento Merge Sort y Radix Sort
para el análisis comparativo de eficiencia en el ordenamiento de placas 
vehiculares ecuatorianas.

COMPLEJIDAD ALGORÍTMICA:
- Merge Sort: O(n log n) en todos los casos
- Radix Sort: O(d * (n + k)) donde d=dígitos, k=rango de valores

Autores: Juan David Ruiz Jara, Ian Nolivos, Kléver Castillo, 
         Estefany Condor, Natasha Nuñez, Elmer Rivadeneira
================================================================================
"""

import time
import copy
from typing import List, Dict, Tuple, Any
import numpy as np

from app.exceptions import SortingError, TransformError


# ============================================================================
# MERGE SORT - Algoritmo de divide y vencerás
# ============================================================================

def merge_sort(arr: List[Dict], key: str = 'placa') -> Tuple[List[Dict], Dict]:
    """
    Implementación del algoritmo Merge Sort para ordenar placas vehiculares.
    
    TEORÍA:
    -------
    Merge Sort fue inventado por John von Neumann en 1945. Utiliza la estrategia
    de "divide y vencerás":
    
    1. DIVIDIR: Divide el arreglo en dos mitades
    2. CONQUISTAR: Ordena recursivamente cada mitad  
    3. COMBINAR: Fusiona las dos mitades ordenadas
    
    COMPLEJIDAD:
    - Temporal: O(n log n) en TODOS los casos (mejor, promedio, peor)
    - Espacial: O(n) - requiere espacio auxiliar proporcional al tamaño
    
    VENTAJAS:
    - Rendimiento garantizado O(n log n)
    - Algoritmo estable (preserva orden relativo de elementos iguales)
    - Funciona bien con datos de cualquier tipo que soporten comparación
    
    DESVENTAJAS:
    - Requiere O(n) espacio adicional
    - Mayor overhead para conjuntos pequeños
    
    Args:
        arr (List[Dict]): Lista de diccionarios a ordenar
        key (str): Clave del diccionario por la cual ordenar (default: 'placa')
        
    Returns:
        Tuple[List[Dict], Dict]: Lista ordenada y métricas de rendimiento
        
    Raises:
        SortingError: Si ocurre un error durante el ordenamiento
        
    Example:
        >>> data = [{'placa': 'XYZ-1234'}, {'placa': 'ABC-5678'}]
        >>> sorted_data, metrics = merge_sort(data)
        >>> print(sorted_data[0]['placa'])  # 'ABC-5678'
    """
    metrics = {
        'algorithm': 'Merge Sort',
        'comparisons': 0,
        'swaps': 0,
        'recursive_calls': 0,
        'input_size': len(arr),
        'execution_time_ms': 0
    }
    
    comparisons = [0]  # Lista para modificar en función anidada
    recursive_calls = [0]
    
    def merge(left: List[Dict], right: List[Dict]) -> List[Dict]:
        """
        Función auxiliar para fusionar dos listas ordenadas.
        
        Esta es la operación clave de Merge Sort. Combina dos sublistas
        ya ordenadas en una sola lista ordenada.
        
        Complejidad: O(n) donde n = len(left) + len(right)
        """
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            comparisons[0] += 1
            
            # Extraer valores para comparación (sin guión para orden lexicográfico correcto)
            left_val = left[i][key].replace('-', '').upper()
            right_val = right[j][key].replace('-', '').upper()
            
            if left_val <= right_val:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        # Agregar elementos restantes (ya están ordenados)
        result.extend(left[i:])
        result.extend(right[j:])
        
        return result
    
    def _merge_sort(arr: List[Dict]) -> List[Dict]:
        """
        Función recursiva principal de Merge Sort.
        
        Implementa la división recursiva del arreglo hasta llegar a
        subarreglos de tamaño 1 (caso base), luego combina.
        """
        recursive_calls[0] += 1
        
        # Caso base: arreglo de 0 o 1 elemento ya está ordenado
        if len(arr) <= 1:
            return arr
        
        # Dividir: encontrar el punto medio
        mid = len(arr) // 2
        
        # Conquistar: ordenar recursivamente cada mitad
        left = _merge_sort(arr[:mid])
        right = _merge_sort(arr[mid:])
        
        # Combinar: fusionar las mitades ordenadas
        return merge(left, right)
    
    try:
        # Medir tiempo de ejecución
        start_time = time.perf_counter()
        
        # Ejecutar ordenamiento
        result = _merge_sort(arr.copy())
        
        end_time = time.perf_counter()
        
        # Actualizar métricas
        metrics['comparisons'] = comparisons[0]
        metrics['recursive_calls'] = recursive_calls[0]
        metrics['execution_time_ms'] = (end_time - start_time) * 1000
        
        return result, metrics
        
    except Exception as e:
        raise SortingError(
            "Error durante la ejecución de Merge Sort",
            algorithm="merge_sort",
            data_size=len(arr),
            original_error=e
        )


# ============================================================================
# RADIX SORT - Algoritmo de ordenamiento por dígitos
# ============================================================================

def radix_sort(arr: List[Dict], key: str = 'placa') -> Tuple[List[Dict], Dict]:
    """
    Implementación del algoritmo Radix Sort (LSD) para placas vehiculares.
    
    TEORÍA:
    -------
    Radix Sort ordena los elementos procesando cada dígito/carácter de forma
    individual, desde el dígito menos significativo (LSD - Least Significant
    Digit) hasta el más significativo. Utiliza Counting Sort como subrutina
    estable para cada posición.
    
    PARA PLACAS ECUATORIANAS (ABC-1234):
    - Longitud fija: 7 caracteres (sin guión)
    - Rango: 36 valores posibles (0-9, A-Z)
    - Se procesa de derecha a izquierda
    
    COMPLEJIDAD:
    - Temporal: O(d * (n + k)) donde:
      * d = número de dígitos (7 para placas)
      * n = número de elementos
      * k = rango de valores por posición (36)
    - Espacial: O(n + k)
    
    VENTAJAS:
    - Complejidad lineal O(d*n) cuando d y k son pequeños
    - Muy eficiente para datos con longitud fija
    - Algoritmo estable
    
    DESVENTAJAS:
    - Requiere conocer el rango de valores (k)
    - Menos eficiente cuando d es grande
    - Overhead significativo para conjuntos pequeños
    
    Args:
        arr (List[Dict]): Lista de diccionarios a ordenar
        key (str): Clave del diccionario por la cual ordenar
        
    Returns:
        Tuple[List[Dict], Dict]: Lista ordenada y métricas de rendimiento
        
    Raises:
        SortingError: Si ocurre un error durante el ordenamiento
    """
    metrics = {
        'algorithm': 'Radix Sort',
        'operations': 0,
        'passes': 0,
        'buckets_used': 37,  # 0-9, A-Z, padding
        'input_size': len(arr),
        'execution_time_ms': 0
    }
    
    operations = [0]
    
    if len(arr) == 0:
        return arr, metrics
    
    def get_key_value(item: Dict) -> str:
        """Extrae y normaliza el valor de la clave para ordenamiento."""
        return item[key].replace('-', '').upper()
    
    # Encontrar la longitud máxima de las claves
    max_length = max(len(get_key_value(item)) for item in arr)
    
    def counting_sort_by_position(arr: List[Dict], position: int) -> List[Dict]:
        """
        Counting Sort estable para una posición de carácter específica.
        
        Esta es la subrutina clave de Radix Sort. Ordena los elementos
        basándose en un solo carácter en la posición especificada.
        
        Args:
            arr: Lista a ordenar
            position: Posición del carácter (desde la derecha, empezando en 0)
            
        Returns:
            Lista ordenada por el carácter en la posición especificada
        """
        # RADIX = 37: 10 dígitos (0-9) + 26 letras (A-Z) + 1 padding
        RADIX = 37
        count = [0] * RADIX
        output = [None] * len(arr)
        
        def char_to_index(char: str) -> int:
            """
            Convierte un carácter a su índice en el arreglo de conteo.
            
            Mapeo:
            - Dígitos '0'-'9': índices 0-9
            - Letras 'A'-'Z': índices 10-35
            - Padding (vacío): índice 36
            """
            operations[0] += 1
            
            if char == '':
                return 36  # Padding para strings más cortos
            elif char.isdigit():
                return int(char)
            else:
                return ord(char.upper()) - ord('A') + 10
        
        def get_char_at_position(item: Dict, pos: int) -> str:
            """Obtiene el carácter en la posición especificada (desde la derecha)."""
            s = get_key_value(item)
            idx = len(s) - 1 - pos  # Posición desde la derecha
            if idx < 0:
                return ''  # Padding
            return s[idx]
        
        # PASO 1: Contar ocurrencias de cada carácter en la posición actual
        for item in arr:
            char = get_char_at_position(item, position)
            index = char_to_index(char)
            count[index] += 1
        
        # PASO 2: Calcular posiciones acumulativas
        # count[i] ahora contiene la posición donde termina el grupo i
        for i in range(1, RADIX):
            count[i] += count[i - 1]
        
        # PASO 3: Construir arreglo de salida (de derecha a izquierda para estabilidad)
        for i in range(len(arr) - 1, -1, -1):
            item = arr[i]
            char = get_char_at_position(item, position)
            index = char_to_index(char)
            count[index] -= 1
            output[count[index]] = item
        
        return output
    
    try:
        start_time = time.perf_counter()
        
        # Aplicar Counting Sort para cada posición (LSD a MSD)
        result = arr.copy()
        for position in range(max_length):
            result = counting_sort_by_position(result, position)
            metrics['passes'] += 1
        
        end_time = time.perf_counter()
        
        metrics['operations'] = operations[0]
        metrics['execution_time_ms'] = (end_time - start_time) * 1000
        
        return result, metrics
        
    except Exception as e:
        raise SortingError(
            "Error durante la ejecución de Radix Sort",
            algorithm="radix_sort",
            data_size=len(arr),
            original_error=e
        )


# ============================================================================
# FUNCIONES DE COMPARACIÓN Y BENCHMARKING
# ============================================================================

def run_sorting_benchmark(data: List[Dict], n_iterations: int = 10) -> Dict:
    """
    Ejecuta un benchmark comparativo entre Merge Sort y Radix Sort.
    
    Realiza múltiples iteraciones de cada algoritmo para obtener
    estadísticas robustas de rendimiento.
    
    Args:
        data: Lista de diccionarios a ordenar
        n_iterations: Número de iteraciones para cada algoritmo
        
    Returns:
        Dict con estadísticas comparativas de ambos algoritmos
        
    Example:
        >>> results = run_sorting_benchmark(data, n_iterations=10)
        >>> print(results['winner'])
    """
    print("=" * 60)
    print("🏁 EJECUTANDO BENCHMARK DE ALGORITMOS DE ORDENAMIENTO")
    print("=" * 60)
    print(f"📊 Configuración:")
    print(f"   - Elementos a ordenar: {len(data):,}")
    print(f"   - Iteraciones por algoritmo: {n_iterations}")
    
    results = {
        'merge_sort': {'times': [], 'comparisons': []},
        'radix_sort': {'times': [], 'operations': []}
    }
    
    # Benchmark Merge Sort
    print(f"\n🔄 Ejecutando {n_iterations} iteraciones de Merge Sort...")
    for i in range(n_iterations):
        data_copy = copy.deepcopy(data)
        _, metrics = merge_sort(data_copy)
        results['merge_sort']['times'].append(metrics['execution_time_ms'])
        results['merge_sort']['comparisons'].append(metrics['comparisons'])
        print(f"   Iteración {i+1:2d}: {metrics['execution_time_ms']:.4f} ms")
    
    # Benchmark Radix Sort
    print(f"\n🔄 Ejecutando {n_iterations} iteraciones de Radix Sort...")
    for i in range(n_iterations):
        data_copy = copy.deepcopy(data)
        _, metrics = radix_sort(data_copy)
        results['radix_sort']['times'].append(metrics['execution_time_ms'])
        results['radix_sort']['operations'].append(metrics['operations'])
        print(f"   Iteración {i+1:2d}: {metrics['execution_time_ms']:.4f} ms")
    
    # Calcular estadísticas
    stats = {
        'merge_sort': {
            'avg_time': np.mean(results['merge_sort']['times']),
            'std_time': np.std(results['merge_sort']['times']),
            'min_time': np.min(results['merge_sort']['times']),
            'max_time': np.max(results['merge_sort']['times']),
            'avg_comparisons': np.mean(results['merge_sort']['comparisons'])
        },
        'radix_sort': {
            'avg_time': np.mean(results['radix_sort']['times']),
            'std_time': np.std(results['radix_sort']['times']),
            'min_time': np.min(results['radix_sort']['times']),
            'max_time': np.max(results['radix_sort']['times']),
            'avg_operations': np.mean(results['radix_sort']['operations'])
        },
        'n_elements': len(data),
        'n_iterations': n_iterations
    }
    
    # Determinar ganador
    if stats['merge_sort']['avg_time'] < stats['radix_sort']['avg_time']:
        stats['winner'] = 'Merge Sort'
        stats['time_difference_ms'] = stats['radix_sort']['avg_time'] - stats['merge_sort']['avg_time']
        stats['percentage_faster'] = (stats['time_difference_ms'] / stats['radix_sort']['avg_time']) * 100
    else:
        stats['winner'] = 'Radix Sort'
        stats['time_difference_ms'] = stats['merge_sort']['avg_time'] - stats['radix_sort']['avg_time']
        stats['percentage_faster'] = (stats['time_difference_ms'] / stats['merge_sort']['avg_time']) * 100
    
    return stats


def verify_sorting_correctness(data: List[Dict], key: str = 'placa') -> bool:
    """
    Verifica que ambos algoritmos producen el mismo resultado ordenado.
    
    Args:
        data: Lista de diccionarios a ordenar
        key: Clave por la cual ordenar
        
    Returns:
        bool: True si ambos algoritmos producen el mismo resultado
    """
    print("\n🔍 Verificando correctitud de algoritmos...")
    
    data_copy1 = copy.deepcopy(data)
    data_copy2 = copy.deepcopy(data)
    
    result_merge, _ = merge_sort(data_copy1, key)
    result_radix, _ = radix_sort(data_copy2, key)
    
    # Extraer solo las placas para comparación
    placas_merge = [item[key] for item in result_merge]
    placas_radix = [item[key] for item in result_radix]
    
    if placas_merge == placas_radix:
        print("✅ VERIFICACIÓN EXITOSA: Ambos algoritmos producen el mismo orden")
        return True
    else:
        print("❌ VERIFICACIÓN FALLIDA: Los resultados difieren")
        return False


if __name__ == "__main__":
    # Pruebas del módulo
    print("=" * 60)
    print("PRUEBAS DEL MÓDULO DE ORDENAMIENTO")
    print("=" * 60)
    
    # Crear datos de prueba
    test_data = [
        {'placa': 'XYZ-9999'},
        {'placa': 'ABC-1234'},
        {'placa': 'MNO-5555'},
        {'placa': 'DEF-2222'},
        {'placa': 'AAA-0001'},
        {'placa': 'ZZZ-9999'},
        {'placa': 'BBB-3333'},
    ]
    
    print("\n📌 Datos de prueba:")
    for item in test_data:
        print(f"   {item['placa']}")
    
    # Prueba Merge Sort
    print("\n📌 Prueba Merge Sort:")
    sorted_merge, metrics_merge = merge_sort(test_data)
    print(f"   Comparaciones: {metrics_merge['comparisons']}")
    print(f"   Tiempo: {metrics_merge['execution_time_ms']:.4f} ms")
    print("   Resultado:", [item['placa'] for item in sorted_merge])
    
    # Prueba Radix Sort
    print("\n📌 Prueba Radix Sort:")
    sorted_radix, metrics_radix = radix_sort(test_data)
    print(f"   Operaciones: {metrics_radix['operations']}")
    print(f"   Tiempo: {metrics_radix['execution_time_ms']:.4f} ms")
    print("   Resultado:", [item['placa'] for item in sorted_radix])
    
    # Verificar correctitud
    verify_sorting_correctness(test_data)
    
    print("\n✅ Todas las pruebas completadas")
