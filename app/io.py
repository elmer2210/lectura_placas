"""
================================================================================
MÓDULO DE ENTRADA/SALIDA (I/O)
================================================================================
Universidad Nacional de Chimborazo
Facultad de Ingeniería - Ciencia de Datos e Inteligencia Artificial
Asignatura: Estructura de Datos

Este módulo maneja la lectura y escritura de archivos CSV con manejo robusto
de errores utilizando try-except-finally.

Autores: Juan David Ruiz Jara, Ian Nolivos, Kléver Castillo, 
         Estefany Condor, Natasha Nuñez, Elmer Rivadeneira
================================================================================
"""

import pandas as pd
import os
from typing import Optional

from app.exceptions import DataReadError, SaveError


def read_csv(filepath: str, encoding: str = 'utf-8') -> pd.DataFrame:
    """
    Lee un archivo CSV y retorna un DataFrame de pandas.
    
    Implementa manejo robusto de errores usando try-except-finally para
    garantizar que los recursos se liberen correctamente y que los errores
    se capturen de forma específica.
    
    Args:
        filepath (str): Ruta al archivo CSV a leer
        encoding (str): Codificación del archivo (default: 'utf-8')
        
    Returns:
        pd.DataFrame: DataFrame con los datos del archivo
        
    Raises:
        DataReadError: Si el archivo no existe, la ruta es inválida,
                      o el contenido está corrupto
                      
    Example:
        >>> df = read_csv("data/raw.csv")
        >>> print(f"Filas cargadas: {len(df)}")
    """
    file_handle = None
    df = None
    
    try:
        # Verificar que el archivo existe
        if not os.path.exists(filepath):
            raise DataReadError(
                f"El archivo no existe: {filepath}",
                filepath=filepath
            )
        
        # Verificar que es un archivo (no un directorio)
        if not os.path.isfile(filepath):
            raise DataReadError(
                f"La ruta no corresponde a un archivo: {filepath}",
                filepath=filepath
            )
        
        # Verificar extensión
        if not filepath.lower().endswith('.csv'):
            raise DataReadError(
                f"El archivo no tiene extensión .csv: {filepath}",
                filepath=filepath
            )
        
        # Intentar leer el archivo
        print(f"📂 Leyendo archivo: {filepath}")
        df = pd.read_csv(filepath, encoding=encoding)
        
        # Verificar que el DataFrame no está vacío
        if df.empty:
            raise DataReadError(
                "El archivo CSV está vacío",
                filepath=filepath
            )
        
        print(f"✅ Archivo leído exitosamente: {len(df)} filas, {len(df.columns)} columnas")
        
    except DataReadError:
        # Re-lanzar excepciones propias sin modificar
        raise
        
    except pd.errors.EmptyDataError as e:
        raise DataReadError(
            "El archivo CSV está vacío o tiene formato inválido",
            filepath=filepath,
            original_error=e
        )
        
    except pd.errors.ParserError as e:
        raise DataReadError(
            "Error al parsear el archivo CSV - formato corrupto",
            filepath=filepath,
            original_error=e
        )
        
    except UnicodeDecodeError as e:
        raise DataReadError(
            f"Error de codificación al leer el archivo (prueba con encoding='latin-1')",
            filepath=filepath,
            original_error=e
        )
        
    except PermissionError as e:
        raise DataReadError(
            "No hay permisos para leer el archivo",
            filepath=filepath,
            original_error=e
        )
        
    except Exception as e:
        raise DataReadError(
            f"Error inesperado al leer el archivo: {type(e).__name__}",
            filepath=filepath,
            original_error=e
        )
        
    finally:
        # Bloque finally: siempre se ejecuta, útil para liberar recursos
        if file_handle is not None:
            file_handle.close()
        print("📋 Operación de lectura finalizada")
    
    return df


def save_csv(df: pd.DataFrame, filepath: str, index: bool = False, 
             encoding: str = 'utf-8') -> bool:
    """
    Guarda un DataFrame en un archivo CSV.
    
    Implementa manejo robusto de errores para garantizar que los datos
    se guarden correctamente o se reporte el error de forma clara.
    
    Args:
        df (pd.DataFrame): DataFrame a guardar
        filepath (str): Ruta donde guardar el archivo
        index (bool): Si incluir el índice en el archivo (default: False)
        encoding (str): Codificación del archivo (default: 'utf-8')
        
    Returns:
        bool: True si se guardó exitosamente
        
    Raises:
        SaveError: Si no se puede guardar el archivo
        
    Example:
        >>> save_csv(df_processed, "data/processed.csv")
        True
    """
    try:
        # Verificar que el DataFrame es válido
        if df is None:
            raise SaveError(
                "El DataFrame es None, no hay datos para guardar",
                filepath=filepath
            )
        
        if not isinstance(df, pd.DataFrame):
            raise SaveError(
                f"Se esperaba un DataFrame, se recibió: {type(df).__name__}",
                filepath=filepath
            )
        
        # Crear directorio si no existe
        directory = os.path.dirname(filepath)
        if directory and not os.path.exists(directory):
            print(f"📁 Creando directorio: {directory}")
            os.makedirs(directory, exist_ok=True)
        
        # Guardar el archivo
        print(f"💾 Guardando archivo: {filepath}")
        df.to_csv(filepath, index=index, encoding=encoding)
        
        # Verificar que el archivo se guardó correctamente
        if not os.path.exists(filepath):
            raise SaveError(
                "El archivo no se creó después de guardar",
                filepath=filepath
            )
        
        file_size = os.path.getsize(filepath)
        print(f"✅ Archivo guardado exitosamente: {file_size:,} bytes")
        
        return True
        
    except SaveError:
        # Re-lanzar excepciones propias
        raise
        
    except PermissionError as e:
        raise SaveError(
            "No hay permisos para escribir en la ruta especificada",
            filepath=filepath,
            original_error=e
        )
        
    except OSError as e:
        raise SaveError(
            f"Error del sistema operativo al guardar: {e.strerror}",
            filepath=filepath,
            original_error=e
        )
        
    except Exception as e:
        raise SaveError(
            f"Error inesperado al guardar el archivo: {type(e).__name__}",
            filepath=filepath,
            original_error=e
        )
        
    finally:
        print("📋 Operación de guardado finalizada")


def load_or_create_sample_data(filepath: str, n_samples: int = 1000) -> pd.DataFrame:
    """
    Carga datos existentes o crea un dataset de ejemplo si no existe.
    
    Esta función es útil para pruebas y desarrollo, permitiendo trabajar
    incluso cuando no hay datos reales disponibles.
    
    Args:
        filepath (str): Ruta al archivo CSV
        n_samples (int): Número de muestras a generar si se crea el dataset
        
    Returns:
        pd.DataFrame: DataFrame con los datos
    """
    import numpy as np
    import random
    import string
    
    try:
        # Intentar cargar datos existentes
        return read_csv(filepath)
        
    except DataReadError:
        print(f"⚠️ Archivo no encontrado, generando datos de ejemplo...")
        
        # Generar datos sintéticos de placas ecuatorianas
        np.random.seed(42)
        
        def generate_plate():
            """Genera una placa ecuatoriana aleatoria (formato ABC-1234)"""
            letters = ''.join(random.choices(string.ascii_uppercase, k=3))
            numbers = ''.join(random.choices(string.digits, k=4))
            return f"{letters}-{numbers}"
        
        # Generar placas únicas
        placas = list(set([generate_plate() for _ in range(n_samples * 2)]))[:n_samples]
        
        # Ciudades y peajes de Ecuador
        ubicaciones = ['Quito', 'Guayaquil', 'Cuenca', 'Ambato', 'Riobamba', 
                      'Manta', 'Machala', 'Santo Domingo']
        peajes = ['Peaje Oyacoto', 'Peaje Yaguachi', 'Peaje Chivería', 
                 'Peaje San Andrés', 'Peaje Chaquilcay', 'Peaje San Juan',
                 'Peaje Manta-Rocafuerte', 'Peaje El Garrido', 'Peaje Santo Domingo']
        estados = ['Habilitada', 'Suspendida', 'Bloqueada']
        
        # Crear DataFrame
        df = pd.DataFrame({
            'id': range(1, n_samples + 1),
            'placa': np.random.choice(placas, n_samples),
            'fecha_registro': pd.date_range(
                start='2020-01-01', 
                end='2025-12-31', 
                periods=n_samples
            ),
            'estado_ANT': np.random.choice(
                estados, 
                n_samples, 
                p=[0.90, 0.06, 0.04]  # 90% habilitadas, 6% suspendidas, 4% bloqueadas
            ),
            'ubicacion_camara': np.random.choice(ubicaciones, n_samples),
            'peaje_ciudad': np.random.choice(peajes, n_samples)
        })
        
        # Guardar el archivo generado
        save_csv(df, filepath)
        print(f"✅ Dataset de ejemplo generado con {n_samples} registros")
        
        return df


if __name__ == "__main__":
    # Pruebas del módulo
    print("=" * 60)
    print("PRUEBAS DEL MÓDULO DE I/O")
    print("=" * 60)
    
    # Prueba 1: Intentar leer archivo inexistente
    print("\n📌 Prueba 1: Leer archivo inexistente")
    try:
        df = read_csv("archivo_que_no_existe.csv")
    except DataReadError as e:
        print(f"✅ Error capturado correctamente: {e.message}")
    
    # Prueba 2: Generar y leer datos de ejemplo
    print("\n📌 Prueba 2: Generar datos de ejemplo")
    df = load_or_create_sample_data("data/test_raw.csv", n_samples=100)
    print(f"   Filas: {len(df)}, Columnas: {list(df.columns)}")
    
    print("\n✅ Todas las pruebas completadas")
