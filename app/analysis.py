"""
================================================================================
MÓDULO DE ANÁLISIS DE DATOS CON PANDAS
================================================================================
Universidad Nacional de Chimborazo
Facultad de Ingeniería - Ciencia de Datos e Inteligencia Artificial
Asignatura: Estructura de Datos

Este módulo implementa funciones de análisis exploratorio de datos (EDA)
utilizando la librería Pandas para el dataset de placas vehiculares.

JUSTIFICACIÓN DEL USO DE PANDAS:
- Eficiencia en manipulación de datos tabulares
- Funciones optimizadas para agregación y estadísticas
- Integración nativa con visualización (matplotlib)
- Manejo elegante de datos faltantes y tipos de datos

Autores: Juan David Ruiz Jara, Ian Nolivos, Kléver Castillo, 
         Estefany Condor, Natasha Nuñez, Elmer Rivadeneira
================================================================================
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime

from app.exceptions import TransformError


# ============================================================================
# FUNCIONES DE ANÁLISIS EXPLORATORIO
# ============================================================================

def get_dataset_summary(df: pd.DataFrame) -> Dict:
    """
    Genera un resumen completo del dataset.
    
    JUSTIFICACIÓN DE PANDAS:
    - df.shape: Obtener dimensiones de forma eficiente
    - df.dtypes: Inspección de tipos de datos
    - df.isna().sum(): Conteo vectorizado de nulos
    - df.nunique(): Conteo de valores únicos optimizado
    
    Args:
        df (pd.DataFrame): DataFrame a analizar
        
    Returns:
        Dict: Diccionario con el resumen del dataset
    """
    summary = {
        'filas': len(df),
        'columnas': len(df.columns),
        'columnas_lista': list(df.columns),
        'tipos_datos': df.dtypes.to_dict(),
        'valores_nulos': df.isna().sum().to_dict(),
        'total_nulos': df.isna().sum().sum(),
        'valores_unicos': df.nunique().to_dict(),
        'memoria_uso_mb': df.memory_usage(deep=True).sum() / (1024 * 1024)
    }
    
    return summary


def analyze_estados_ant(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza la distribución de estados ANT en el dataset.
    
    JUSTIFICACIÓN DE PANDAS:
    - value_counts(): Conteo eficiente de frecuencias
    - Operaciones vectorizadas para cálculo de porcentajes
    - reset_index(): Conversión a DataFrame estructurado
    
    Args:
        df (pd.DataFrame): DataFrame con columna 'estado_ANT'
        
    Returns:
        pd.DataFrame: Tabla de frecuencias y porcentajes por estado
        
    Example:
        >>> analysis = analyze_estados_ant(df)
        >>> print(analysis)
        
           estado_ANT  cantidad  porcentaje
        0  Habilitada       902       90.20
        1  Suspendida        55        5.50
        2   Bloqueada        43        4.30
    """
    print("📊 Analizando distribución de estados ANT...")
    
    # Usar value_counts() de Pandas - muy eficiente para conteos
    counts = df['estado_ANT'].value_counts()
    percentages = df['estado_ANT'].value_counts(normalize=True) * 100
    
    # Crear DataFrame de análisis
    analysis = pd.DataFrame({
        'estado_ANT': counts.index,
        'cantidad': counts.values,
        'porcentaje': percentages.values.round(2)
    })
    
    print(f"✅ Análisis completado: {len(analysis)} estados encontrados")
    
    return analysis


def analyze_trafico_por_ubicacion(df: pd.DataFrame) -> pd.DataFrame:
    """
    Analiza el volumen de tráfico por ubicación de cámara y peaje.
    
    JUSTIFICACIÓN DE PANDAS:
    - groupby(): Agrupación eficiente de datos
    - agg(): Agregaciones múltiples en una sola operación
    - sort_values(): Ordenamiento optimizado
    
    Args:
        df (pd.DataFrame): DataFrame con columnas 'ubicacion_camara' y 'peaje_ciudad'
        
    Returns:
        pd.DataFrame: Análisis de tráfico por ubicación
    """
    print("📊 Analizando tráfico por ubicación...")
    
    # Usar groupby de Pandas para agregación eficiente
    trafico = df.groupby(['ubicacion_camara', 'peaje_ciudad']).agg(
        registros=('id', 'count'),
        placas_unicas=('placa', 'nunique'),
        primera_fecha=('fecha_registro', 'min'),
        ultima_fecha=('fecha_registro', 'max')
    ).reset_index()
    
    # Ordenar por número de registros (descendente)
    trafico = trafico.sort_values('registros', ascending=False)
    
    print(f"✅ Análisis completado: {len(trafico)} combinaciones ubicación-peaje")
    
    return trafico


def analyze_temporal(df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Realiza análisis temporal del dataset.
    
    JUSTIFICACIÓN DE PANDAS:
    - dt accessor: Extracción eficiente de componentes de fecha
    - groupby + size(): Conteo rápido por grupos
    - Soporte nativo para series temporales
    
    Args:
        df (pd.DataFrame): DataFrame con columna 'fecha_registro'
        
    Returns:
        Dict con DataFrames de análisis temporal:
        - 'por_año': Registros por año
        - 'por_mes': Registros por mes
        - 'por_hora': Registros por hora del día
        - 'por_dia_semana': Registros por día de la semana
    """
    print("📊 Realizando análisis temporal...")
    
    # Asegurar que fecha_registro es datetime
    if not pd.api.types.is_datetime64_any_dtype(df['fecha_registro']):
        df = df.copy()
        df['fecha_registro'] = pd.to_datetime(df['fecha_registro'])
    
    # Análisis por año
    por_año = df.groupby(df['fecha_registro'].dt.year).size().reset_index()
    por_año.columns = ['año', 'registros']
    
    # Análisis por mes (1-12)
    por_mes = df.groupby(df['fecha_registro'].dt.month).size().reset_index()
    por_mes.columns = ['mes', 'registros']
    
    # Análisis por hora del día (0-23)
    por_hora = df.groupby(df['fecha_registro'].dt.hour).size().reset_index()
    por_hora.columns = ['hora', 'registros']
    
    # Análisis por día de la semana
    por_dia_semana = df.groupby(df['fecha_registro'].dt.day_name()).size().reset_index()
    por_dia_semana.columns = ['dia_semana', 'registros']
    
    # Ordenar días de la semana correctamente
    dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    por_dia_semana['dia_orden'] = por_dia_semana['dia_semana'].map(
        {day: i for i, day in enumerate(dias_orden)}
    )
    por_dia_semana = por_dia_semana.sort_values('dia_orden').drop('dia_orden', axis=1)
    
    print(f"✅ Análisis temporal completado")
    
    return {
        'por_año': por_año,
        'por_mes': por_mes,
        'por_hora': por_hora,
        'por_dia_semana': por_dia_semana
    }


def analyze_frecuencia_placas(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Analiza la frecuencia de aparición de cada placa.
    
    JUSTIFICACIÓN DE PANDAS:
    - value_counts(): Conteo ultra-eficiente de frecuencias
    - describe(): Estadísticas descriptivas automáticas
    - Indexación booleana para filtrado
    
    Args:
        df (pd.DataFrame): DataFrame con columna 'placa'
        
    Returns:
        Tuple[pd.DataFrame, Dict]: 
        - DataFrame con frecuencia por placa
        - Diccionario con estadísticas de frecuencia
    """
    print("📊 Analizando frecuencia de placas...")
    
    # Contar frecuencia de cada placa
    frecuencia = df['placa'].value_counts().reset_index()
    frecuencia.columns = ['placa', 'num_registros']
    
    # Calcular estadísticas
    stats = {
        'total_placas_unicas': len(frecuencia),
        'promedio_registros': frecuencia['num_registros'].mean(),
        'mediana_registros': frecuencia['num_registros'].median(),
        'max_registros': frecuencia['num_registros'].max(),
        'min_registros': frecuencia['num_registros'].min(),
        'placas_con_un_registro': (frecuencia['num_registros'] == 1).sum(),
        'placas_con_multiples': (frecuencia['num_registros'] > 1).sum()
    }
    
    print(f"✅ Análisis completado: {stats['total_placas_unicas']} placas únicas")
    
    return frecuencia, stats


def identify_alertas(df: pd.DataFrame) -> Dict:
    """
    Identifica vehículos con estados problemáticos (alertas).
    
    JUSTIFICACIÓN DE PANDAS:
    - isin(): Filtrado eficiente por múltiples valores
    - groupby().agg(): Agregaciones complejas en una operación
    - Manejo elegante de datos categóricos
    
    Args:
        df (pd.DataFrame): DataFrame con columna 'estado_ANT'
        
    Returns:
        Dict con información de alertas:
        - 'total_alertas': Número total de registros con alerta
        - 'por_estado': Conteo por tipo de alerta
        - 'placas_alertas': Lista de placas con alertas
        - 'detalle': DataFrame con detalle de alertas
    """
    print("🚨 Identificando vehículos con alertas...")
    
    # Filtrar estados problemáticos
    alertas_df = df[df['estado_ANT'].isin(['Bloqueada', 'Suspendida'])].copy()
    
    # Conteo por estado
    por_estado = alertas_df['estado_ANT'].value_counts().to_dict()
    
    # Placas únicas con alertas
    placas_con_alertas = alertas_df['placa'].unique().tolist()
    
    # Detalle de alertas por placa
    detalle = alertas_df.groupby(['placa', 'estado_ANT']).agg(
        num_detecciones=('id', 'count'),
        primera_deteccion=('fecha_registro', 'min'),
        ultima_deteccion=('fecha_registro', 'max'),
        ubicaciones=('ubicacion_camara', lambda x: ', '.join(x.unique()))
    ).reset_index().sort_values('num_detecciones', ascending=False)
    
    result = {
        'total_alertas': len(alertas_df),
        'por_estado': por_estado,
        'placas_con_alertas': len(placas_con_alertas),
        'lista_placas': placas_con_alertas,
        'detalle': detalle
    }
    
    print(f"✅ Alertas identificadas: {result['total_alertas']} registros, "
          f"{result['placas_con_alertas']} placas únicas")
    
    return result


def create_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Crea nuevas variables (feature engineering) para el dataset.
    
    JUSTIFICACIÓN DE PANDAS:
    - Operaciones vectorizadas para creación de columnas
    - dt accessor para extracción de componentes temporales
    - str accessor para manipulación de strings
    
    Nuevas variables creadas:
    - año, mes, dia, hora: Componentes de fecha
    - dia_semana: Nombre del día
    - es_fin_semana: Indicador booleano
    - placa_provincia: Código de provincia (primera letra)
    - placa_sin_guion: Placa normalizada para ordenamiento
    
    Args:
        df (pd.DataFrame): DataFrame original
        
    Returns:
        pd.DataFrame: DataFrame con nuevas variables
    """
    print("🔧 Creando nuevas variables (feature engineering)...")
    
    df_copy = df.copy()
    
    try:
        # Asegurar que fecha_registro es datetime
        if not pd.api.types.is_datetime64_any_dtype(df_copy['fecha_registro']):
            df_copy['fecha_registro'] = pd.to_datetime(df_copy['fecha_registro'])
        
        # Variables temporales usando el accessor .dt de Pandas
        df_copy['año'] = df_copy['fecha_registro'].dt.year
        df_copy['mes'] = df_copy['fecha_registro'].dt.month
        df_copy['dia'] = df_copy['fecha_registro'].dt.day
        df_copy['hora'] = df_copy['fecha_registro'].dt.hour
        df_copy['dia_semana'] = df_copy['fecha_registro'].dt.day_name()
        
        # Indicador de fin de semana
        df_copy['es_fin_semana'] = df_copy['fecha_registro'].dt.dayofweek >= 5
        
        # Extraer código de provincia de la placa (primera letra)
        # En Ecuador, la primera letra indica la provincia
        df_copy['placa_provincia'] = df_copy['placa'].str[0]
        
        # Placa normalizada (sin guión, mayúsculas) para ordenamiento
        df_copy['placa_sin_guion'] = df_copy['placa'].str.replace('-', '').str.upper()
        
        # Indicador de alerta
        df_copy['tiene_alerta'] = df_copy['estado_ANT'].isin(['Bloqueada', 'Suspendida'])
        
        print(f"✅ Variables creadas: año, mes, dia, hora, dia_semana, es_fin_semana, "
              f"placa_provincia, placa_sin_guion, tiene_alerta")
        
        return df_copy
        
    except Exception as e:
        raise TransformError(
            "Error al crear nuevas variables",
            transform_type="feature_engineering",
            original_error=e
        )


def generate_statistics_table(df: pd.DataFrame) -> pd.DataFrame:
    """
    Genera una tabla de estadísticas descriptivas para el dataset.
    
    JUSTIFICACIÓN DE PANDAS:
    - describe(): Estadísticas descriptivas automáticas
    - Operaciones de agregación múltiple
    - Formateo flexible de salida
    
    Args:
        df (pd.DataFrame): DataFrame a analizar
        
    Returns:
        pd.DataFrame: Tabla de estadísticas
    """
    # Estadísticas para columnas numéricas
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if numeric_cols:
        stats = df[numeric_cols].describe()
        return stats.T  # Transponer para mejor lectura
    else:
        return pd.DataFrame()


if __name__ == "__main__":
    # Pruebas del módulo
    print("=" * 60)
    print("PRUEBAS DEL MÓDULO DE ANÁLISIS")
    print("=" * 60)
    
    # Crear DataFrame de prueba
    np.random.seed(42)
    n = 100
    
    df_test = pd.DataFrame({
        'id': range(1, n + 1),
        'placa': [f"{'ABC'[i%3]}{chr(65+i%26)}{chr(65+(i+1)%26)}-{1000+i}" for i in range(n)],
        'fecha_registro': pd.date_range(start='2024-01-01', periods=n, freq='H'),
        'estado_ANT': np.random.choice(['Habilitada', 'Suspendida', 'Bloqueada'], n, p=[0.9, 0.06, 0.04]),
        'ubicacion_camara': np.random.choice(['Quito', 'Guayaquil', 'Cuenca'], n),
        'peaje_ciudad': np.random.choice(['Peaje A', 'Peaje B', 'Peaje C'], n)
    })
    
    print("\n📌 DataFrame de prueba creado")
    print(f"   Filas: {len(df_test)}, Columnas: {len(df_test.columns)}")
    
    # Prueba 1: Resumen del dataset
    print("\n📌 Prueba 1: Resumen del dataset")
    summary = get_dataset_summary(df_test)
    print(f"   Filas: {summary['filas']}, Columnas: {summary['columnas']}")
    
    # Prueba 2: Análisis de estados
    print("\n📌 Prueba 2: Análisis de estados ANT")
    estados = analyze_estados_ant(df_test)
    print(estados)
    
    # Prueba 3: Análisis temporal
    print("\n📌 Prueba 3: Análisis temporal")
    temporal = analyze_temporal(df_test)
    print(f"   Registros por hora: {len(temporal['por_hora'])} horas")
    
    # Prueba 4: Crear features
    print("\n📌 Prueba 4: Feature engineering")
    df_features = create_features(df_test)
    print(f"   Nuevas columnas: {[c for c in df_features.columns if c not in df_test.columns]}")
    
    # Prueba 5: Identificar alertas
    print("\n📌 Prueba 5: Identificar alertas")
    alertas = identify_alertas(df_test)
    print(f"   Total alertas: {alertas['total_alertas']}")
    
    print("\n✅ Todas las pruebas completadas")
