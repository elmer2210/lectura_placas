"""
================================================================================
MÓDULO DE LIMPIEZA Y VALIDACIÓN DE DATOS
================================================================================
Universidad Nacional de Chimborazo
Facultad de Ingeniería - Ciencia de Datos e Inteligencia Artificial
Asignatura: Estructura de Datos

Este módulo implementa funciones para:
- Validación de esquema del dataset
- Conversión de tipos de datos
- Eliminación de duplicados
- Manejo de valores faltantes

Autores: Juan David Ruiz Jara, Ian Nolivos, Kléver Castillo, 
         Estefany Condor, Natasha Nuñez, Elmer Rivadeneira
================================================================================
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Tuple, Optional

from app.exceptions import SchemaError, TransformError


# ============================================================================
# COLUMNAS REQUERIDAS PARA EL DATASET DE PLACAS VEHICULARES
# ============================================================================

REQUIRED_COLUMNS = ['id', 'placa', 'fecha_registro', 'estado_ANT', 
                    'ubicacion_camara', 'peaje_ciudad']

COLUMN_TYPES = {
    'id': 'numeric',
    'placa': 'string',
    'fecha_registro': 'datetime',
    'estado_ANT': 'string',
    'ubicacion_camara': 'string',
    'peaje_ciudad': 'string'
}


# ============================================================================
# ETAPA 3: VALIDACIÓN DE ESQUEMA Y TIPOS
# ============================================================================

def validate_schema(df: pd.DataFrame, required_columns: List[str] = None) -> bool:
    """
    Valida que el DataFrame contenga todas las columnas requeridas.
    
    Esta función verifica la estructura del dataset antes de procesarlo,
    asegurando que todas las columnas necesarias estén presentes.
    
    Args:
        df (pd.DataFrame): DataFrame a validar
        required_columns (List[str]): Lista de columnas requeridas
                                     (default: REQUIRED_COLUMNS)
    
    Returns:
        bool: True si el esquema es válido
        
    Raises:
        SchemaError: Si faltan columnas requeridas
        
    Example:
        >>> validate_schema(df)
        True
    """
    if required_columns is None:
        required_columns = REQUIRED_COLUMNS
    
    print("🔍 Validando esquema del dataset...")
    
    # Obtener columnas presentes en el DataFrame
    present_columns = set(df.columns)
    required_set = set(required_columns)
    
    # Encontrar columnas faltantes
    missing_columns = required_set - present_columns
    
    if missing_columns:
        raise SchemaError(
            "El dataset no contiene todas las columnas requeridas",
            missing_columns=list(missing_columns)
        )
    
    print(f"✅ Esquema válido: {len(required_columns)} columnas verificadas")
    print(f"   Columnas encontradas: {list(required_columns)}")
    
    return True


def convert_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convierte las columnas a sus tipos de datos correctos.
    
    Realiza conversiones de tipo con manejo de errores:
    - id: a numérico (int)
    - placa: a string
    - fecha_registro: a datetime
    - estado_ANT, ubicacion_camara, peaje_ciudad: a string
    
    Args:
        df (pd.DataFrame): DataFrame a convertir
        
    Returns:
        pd.DataFrame: DataFrame con tipos convertidos
        
    Raises:
        TransformError: Si la conversión de tipos falla de forma irrecuperable
        
    Example:
        >>> df_converted = convert_types(df)
    """
    print("🔄 Convirtiendo tipos de datos...")
    df_copy = df.copy()
    conversion_report = {}
    
    try:
        # Convertir 'id' a numérico
        if 'id' in df_copy.columns:
            original_nulls = df_copy['id'].isna().sum()
            df_copy['id'] = pd.to_numeric(df_copy['id'], errors='coerce')
            new_nulls = df_copy['id'].isna().sum()
            conversion_report['id'] = {
                'tipo': 'numeric',
                'valores_convertidos_a_nulo': new_nulls - original_nulls
            }
        
        # Convertir 'placa' a string
        if 'placa' in df_copy.columns:
            df_copy['placa'] = df_copy['placa'].astype(str)
            # Limpiar placas: eliminar espacios y convertir a mayúsculas
            df_copy['placa'] = df_copy['placa'].str.strip().str.upper()
            conversion_report['placa'] = {'tipo': 'string', 'limpieza': 'strip+upper'}
        
        # Convertir 'fecha_registro' a datetime
        if 'fecha_registro' in df_copy.columns:
            original_nulls = df_copy['fecha_registro'].isna().sum()
            df_copy['fecha_registro'] = pd.to_datetime(
                df_copy['fecha_registro'], 
                errors='coerce'
            )
            new_nulls = df_copy['fecha_registro'].isna().sum()
            conversion_report['fecha_registro'] = {
                'tipo': 'datetime',
                'valores_convertidos_a_nulo': new_nulls - original_nulls
            }
        
        # Convertir columnas de texto
        text_columns = ['estado_ANT', 'ubicacion_camara', 'peaje_ciudad']
        for col in text_columns:
            if col in df_copy.columns:
                df_copy[col] = df_copy[col].astype(str).str.strip()
                conversion_report[col] = {'tipo': 'string', 'limpieza': 'strip'}
        
        print("✅ Conversión de tipos completada")
        for col, info in conversion_report.items():
            print(f"   • {col}: {info}")
        
        return df_copy
        
    except Exception as e:
        raise TransformError(
            "Error durante la conversión de tipos",
            transform_type="type_conversion",
            original_error=e
        )


# ============================================================================
# ETAPA 4: LIMPIEZA BÁSICA
# ============================================================================

def remove_duplicates(df: pd.DataFrame, subset: List[str] = None) -> Tuple[pd.DataFrame, int]:
    """
    Elimina filas duplicadas del DataFrame.
    
    Args:
        df (pd.DataFrame): DataFrame a limpiar
        subset (List[str]): Columnas a considerar para detectar duplicados
                           (default: todas las columnas)
    
    Returns:
        Tuple[pd.DataFrame, int]: DataFrame sin duplicados y número de duplicados eliminados
        
    Example:
        >>> df_clean, n_removed = remove_duplicates(df)
        >>> print(f"Se eliminaron {n_removed} duplicados")
    """
    print("🧹 Eliminando duplicados...")
    
    rows_before = len(df)
    df_clean = df.drop_duplicates(subset=subset, keep='first')
    rows_after = len(df_clean)
    
    duplicates_removed = rows_before - rows_after
    
    print(f"✅ Duplicados eliminados: {duplicates_removed}")
    print(f"   Filas antes: {rows_before}, Filas después: {rows_after}")
    
    return df_clean, duplicates_removed


def handle_missing_values(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict]:
    """
    Maneja valores faltantes según reglas específicas para cada columna.
    
    Reglas de imputación:
    - id: eliminar filas sin id (son inválidas)
    - placa: eliminar filas sin placa (campo crítico)
    - fecha_registro: imputar con fecha actual
    - estado_ANT: imputar con "DESCONOCIDO"
    - ubicacion_camara: imputar con "DESCONOCIDO"
    - peaje_ciudad: imputar con "DESCONOCIDO"
    
    Args:
        df (pd.DataFrame): DataFrame a limpiar
        
    Returns:
        Tuple[pd.DataFrame, Dict]: DataFrame limpio y reporte de imputaciones
        
    Example:
        >>> df_clean, report = handle_missing_values(df)
    """
    print("🔧 Manejando valores faltantes...")
    df_copy = df.copy()
    
    # Reporte de valores nulos antes
    nulls_before = df_copy.isna().sum().to_dict()
    total_nulls_before = sum(nulls_before.values())
    
    imputation_report = {
        'nulls_before': nulls_before,
        'actions': {},
        'rows_removed': 0
    }
    
    # Regla 1: Eliminar filas sin id
    if 'id' in df_copy.columns:
        rows_before = len(df_copy)
        df_copy = df_copy.dropna(subset=['id'])
        rows_removed = rows_before - len(df_copy)
        imputation_report['actions']['id'] = f"Eliminadas {rows_removed} filas sin id"
        imputation_report['rows_removed'] += rows_removed
    
    # Regla 2: Eliminar filas sin placa
    if 'placa' in df_copy.columns:
        rows_before = len(df_copy)
        df_copy = df_copy.dropna(subset=['placa'])
        # También eliminar placas vacías o inválidas
        df_copy = df_copy[df_copy['placa'].str.len() > 0]
        df_copy = df_copy[df_copy['placa'] != 'nan']
        rows_removed = rows_before - len(df_copy)
        imputation_report['actions']['placa'] = f"Eliminadas {rows_removed} filas sin placa válida"
        imputation_report['rows_removed'] += rows_removed
    
    # Regla 3: Imputar fecha_registro con fecha actual
    if 'fecha_registro' in df_copy.columns:
        nulls = df_copy['fecha_registro'].isna().sum()
        if nulls > 0:
            df_copy['fecha_registro'] = df_copy['fecha_registro'].fillna(pd.Timestamp.now())
            imputation_report['actions']['fecha_registro'] = f"Imputados {nulls} valores con fecha actual"
    
    # Regla 4: Imputar columnas de texto con "DESCONOCIDO"
    text_columns = ['estado_ANT', 'ubicacion_camara', 'peaje_ciudad']
    for col in text_columns:
        if col in df_copy.columns:
            nulls = df_copy[col].isna().sum()
            # También considerar 'nan' como string nulo
            df_copy[col] = df_copy[col].replace('nan', np.nan)
            nulls += (df_copy[col] == 'nan').sum()
            if nulls > 0:
                df_copy[col] = df_copy[col].fillna('DESCONOCIDO')
                imputation_report['actions'][col] = f"Imputados {nulls} valores con 'DESCONOCIDO'"
    
    # Reporte de valores nulos después
    nulls_after = df_copy.isna().sum().to_dict()
    total_nulls_after = sum(nulls_after.values())
    imputation_report['nulls_after'] = nulls_after
    
    print(f"✅ Valores faltantes manejados")
    print(f"   Nulos antes: {total_nulls_before}, Nulos después: {total_nulls_after}")
    print(f"   Filas eliminadas: {imputation_report['rows_removed']}")
    
    for col, action in imputation_report['actions'].items():
        print(f"   • {col}: {action}")
    
    return df_copy, imputation_report


def validate_plate_format(df: pd.DataFrame) -> Tuple[pd.DataFrame, int]:
    """
    Valida que las placas tengan el formato ecuatoriano correcto (ABC-1234).
    
    Args:
        df (pd.DataFrame): DataFrame con columna 'placa'
        
    Returns:
        Tuple[pd.DataFrame, int]: DataFrame con placas válidas y número de inválidas
        
    Example:
        >>> df_valid, invalid_count = validate_plate_format(df)
    """
    import re
    
    print("🔍 Validando formato de placas...")
    
    # Patrón para placa ecuatoriana: 3 letras, guión, 4 números
    pattern = r'^[A-Z]{3}-[0-9]{4}$'
    
    # Verificar formato
    df_copy = df.copy()
    valid_mask = df_copy['placa'].str.match(pattern, na=False)
    
    invalid_count = (~valid_mask).sum()
    
    if invalid_count > 0:
        print(f"⚠️ Encontradas {invalid_count} placas con formato inválido")
        # Mostrar algunas placas inválidas como ejemplo
        invalid_plates = df_copy[~valid_mask]['placa'].head(5).tolist()
        print(f"   Ejemplos de placas inválidas: {invalid_plates}")
    
    # Filtrar solo placas válidas
    df_valid = df_copy[valid_mask].copy()
    
    print(f"✅ Validación completada: {len(df_valid)} placas válidas")
    
    return df_valid, invalid_count


if __name__ == "__main__":
    # Pruebas del módulo
    print("=" * 60)
    print("PRUEBAS DEL MÓDULO DE LIMPIEZA")
    print("=" * 60)
    
    # Crear DataFrame de prueba
    df_test = pd.DataFrame({
        'id': [1, 2, 3, None, 5, 5],
        'placa': ['ABC-1234', 'XYZ-5678', 'DEF-9012', 'GHI-3456', None, 'ABC-1234'],
        'fecha_registro': ['2024-01-01', '2024-01-02', None, '2024-01-04', '2024-01-05', '2024-01-01'],
        'estado_ANT': ['Habilitada', 'Suspendida', 'Bloqueada', None, 'Habilitada', 'Habilitada'],
        'ubicacion_camara': ['Quito', 'Guayaquil', None, 'Cuenca', 'Ambato', 'Quito'],
        'peaje_ciudad': ['Peaje A', 'Peaje B', 'Peaje C', 'Peaje D', None, 'Peaje A']
    })
    
    print("\n📌 DataFrame de prueba:")
    print(df_test)
    
    # Prueba 1: Validar esquema
    print("\n📌 Prueba 1: Validar esquema")
    try:
        validate_schema(df_test)
    except SchemaError as e:
        print(f"Error: {e}")
    
    # Prueba 2: Convertir tipos
    print("\n📌 Prueba 2: Convertir tipos")
    df_converted = convert_types(df_test)
    
    # Prueba 3: Eliminar duplicados
    print("\n📌 Prueba 3: Eliminar duplicados")
    df_no_dups, n_dups = remove_duplicates(df_converted)
    
    # Prueba 4: Manejar nulos
    print("\n📌 Prueba 4: Manejar valores faltantes")
    df_clean, report = handle_missing_values(df_no_dups)
    
    print("\n📌 DataFrame limpio final:")
    print(df_clean)
    
    print("\n✅ Todas las pruebas completadas")
