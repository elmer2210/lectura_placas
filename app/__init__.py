"""
================================================================================
PAQUETE APP - Sistema de Análisis de Placas Vehiculares Ecuatorianas
================================================================================
Universidad Nacional de Chimborazo
Facultad de Ingeniería - Ciencia de Datos e Inteligencia Artificial
Asignatura: Estructura de Datos

Este paquete contiene todos los módulos necesarios para el análisis
comparativo de algoritmos de ordenamiento (Radix Sort vs Merge Sort)
aplicado a datos de placas vehiculares.

ESTRUCTURA DEL PAQUETE:
- exceptions.py: Excepciones personalizadas del proyecto
- io.py: Funciones de entrada/salida (lectura y escritura de archivos)
- cleaning.py: Funciones de limpieza y validación de datos
- sorting.py: Implementación de algoritmos de ordenamiento
- analysis.py: Funciones de análisis exploratorio con Pandas
- report.py: Generación de reportes
- pipeline.py: Orquestación del flujo de procesamiento

Autores: Juan David Ruiz Jara, Ian Nolivos, Kléver Castillo, 
         Estefany Condor, Natasha Nuñez, Elmer Rivadeneira
================================================================================
"""

# Importar excepciones
from app.exceptions import (
    PlacasDataError,
    DataReadError,
    SchemaError,
    TransformError,
    SaveError,
    SortingError,
    ValidationError
)

# Importar funciones de I/O
from app.io import (
    read_csv,
    save_csv,
    load_or_create_sample_data
)

# Importar funciones de limpieza
from app.cleaning import (
    validate_schema,
    convert_types,
    remove_duplicates,
    handle_missing_values,
    REQUIRED_COLUMNS
)

# Importar algoritmos de ordenamiento
from app.sorting import (
    merge_sort,
    radix_sort,
    run_sorting_benchmark,
    verify_sorting_correctness
)

# Importar funciones de análisis
from app.analysis import (
    get_dataset_summary,
    analyze_estados_ant,
    analyze_temporal,
    analyze_frecuencia_placas,
    identify_alertas,
    create_features
)

# Importar funciones de reporte
from app.report import (
    generate_sorting_report,
    generate_conclusion_report,
    save_report
)

# Importar pipeline
from app.pipeline import (
    run_cleaning_pipeline,
    run_sorting_pipeline,
    run_analysis_pipeline,
    run_full_pipeline
)

# Versión del paquete
__version__ = '1.0.0'
__author__ = 'Equipo UNACH - Estructura de Datos'

# Lista de elementos exportados
__all__ = [
    # Excepciones
    'PlacasDataError',
    'DataReadError', 
    'SchemaError',
    'TransformError',
    'SaveError',
    'SortingError',
    'ValidationError',
    
    # I/O
    'read_csv',
    'save_csv',
    'load_or_create_sample_data',
    
    # Limpieza
    'validate_schema',
    'convert_types',
    'remove_duplicates',
    'handle_missing_values',
    'REQUIRED_COLUMNS',
    
    # Ordenamiento
    'merge_sort',
    'radix_sort',
    'run_sorting_benchmark',
    'verify_sorting_correctness',
    
    # Análisis
    'get_dataset_summary',
    'analyze_estados_ant',
    'analyze_temporal',
    'analyze_frecuencia_placas',
    'identify_alertas',
    'create_features',
    
    # Reportes
    'generate_sorting_report',
    'generate_conclusion_report',
    'save_report',
    
    # Pipeline
    'run_cleaning_pipeline',
    'run_sorting_pipeline',
    'run_analysis_pipeline',
    'run_full_pipeline'
]

print(f"📦 Paquete 'app' cargado - v{__version__}")
