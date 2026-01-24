"""
================================================================================
MÓDULO DE EXCEPCIONES PERSONALIZADAS
================================================================================
Universidad Nacional de Chimborazo
Facultad de Ingeniería - Ciencia de Datos e Inteligencia Artificial
Asignatura: Estructura de Datos
Periodo: Octubre 2025 - Febrero 2026

Este módulo define las excepciones personalizadas del proyecto para el manejo
robusto de errores durante el procesamiento de datos de placas vehiculares.

Autores:
- Juan David Ruiz Jara
- Ian Nolivos
- Kléver Castillo
- Estefany Condor
- Natasha Nuñez
- Elmer Rivadeneira
================================================================================
"""


class PlacasDataError(Exception):
    """
    Excepción base del proyecto de análisis de placas vehiculares.
    
    Todas las excepciones personalizadas del proyecto heredan de esta clase,
    permitiendo capturar cualquier error del dominio con un solo except.
    
    Attributes:
        message (str): Mensaje descriptivo del error
        details (dict): Información adicional sobre el error (opcional)
    """
    
    def __init__(self, message: str, details: dict = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)
    
    def __str__(self):
        if self.details:
            return f"{self.message} | Detalles: {self.details}"
        return self.message


class DataReadError(PlacasDataError):
    """
    Excepción lanzada cuando ocurre un error al leer archivos de datos.
    
    Se utiliza cuando:
    - El archivo no existe
    - La ruta es inválida
    - El contenido del archivo está corrupto
    - El formato del archivo no es válido (no es CSV válido)
    
    Example:
        >>> raise DataReadError("No se pudo leer el archivo", {"path": "data/raw.csv"})
    """
    
    def __init__(self, message: str, filepath: str = None, original_error: Exception = None):
        details = {}
        if filepath:
            details["filepath"] = filepath
        if original_error:
            details["original_error"] = str(original_error)
        super().__init__(message, details)


class SchemaError(PlacasDataError):
    """
    Excepción lanzada cuando el esquema del dataset no cumple los requisitos.
    
    Se utiliza cuando:
    - Faltan columnas requeridas
    - Los tipos de datos no son los esperados
    - La estructura del DataFrame no es válida
    
    Example:
        >>> raise SchemaError("Faltan columnas", {"missing": ["placa", "estado_ANT"]})
    """
    
    def __init__(self, message: str, missing_columns: list = None, invalid_types: dict = None):
        details = {}
        if missing_columns:
            details["columnas_faltantes"] = missing_columns
        if invalid_types:
            details["tipos_invalidos"] = invalid_types
        super().__init__(message, details)


class TransformError(PlacasDataError):
    """
    Excepción lanzada cuando falla una transformación de datos.
    
    Se utiliza cuando:
    - La conversión de tipos falla
    - La limpieza de datos encuentra errores irrecuperables
    - El tratamiento de outliers falla
    - La creación de nuevas variables falla
    
    Example:
        >>> raise TransformError("Error en conversión de tipos", {"column": "income"})
    """
    
    def __init__(self, message: str, transform_type: str = None, column: str = None, 
                 original_error: Exception = None):
        details = {}
        if transform_type:
            details["tipo_transformacion"] = transform_type
        if column:
            details["columna"] = column
        if original_error:
            details["error_original"] = str(original_error)
        super().__init__(message, details)


class SaveError(PlacasDataError):
    """
    Excepción lanzada cuando ocurre un error al guardar archivos.
    
    Se utiliza cuando:
    - No se puede escribir en la ruta especificada
    - No hay permisos de escritura
    - El disco está lleno
    - Error de formato al exportar
    
    Example:
        >>> raise SaveError("No se pudo guardar", {"path": "data/processed.csv"})
    """
    
    def __init__(self, message: str, filepath: str = None, original_error: Exception = None):
        details = {}
        if filepath:
            details["filepath"] = filepath
        if original_error:
            details["original_error"] = str(original_error)
        super().__init__(message, details)


class SortingError(PlacasDataError):
    """
    Excepción lanzada cuando ocurre un error en los algoritmos de ordenamiento.
    
    Se utiliza cuando:
    - Los datos de entrada no son válidos para el algoritmo
    - El algoritmo encuentra un estado inconsistente
    - La comparación de elementos falla
    
    Example:
        >>> raise SortingError("Error en Merge Sort", {"algorithm": "merge_sort"})
    """
    
    def __init__(self, message: str, algorithm: str = None, data_size: int = None,
                 original_error: Exception = None):
        details = {}
        if algorithm:
            details["algoritmo"] = algorithm
        if data_size:
            details["tamaño_datos"] = data_size
        if original_error:
            details["error_original"] = str(original_error)
        super().__init__(message, details)


class ValidationError(PlacasDataError):
    """
    Excepción lanzada cuando falla la validación de datos.
    
    Se utiliza cuando:
    - Los datos no cumplen con las reglas de negocio
    - El formato de placa no es válido
    - Los valores están fuera de rango permitido
    
    Example:
        >>> raise ValidationError("Placa inválida", {"placa": "ABC123", "formato_esperado": "ABC-1234"})
    """
    
    def __init__(self, message: str, field: str = None, value: str = None, 
                 expected_format: str = None):
        details = {}
        if field:
            details["campo"] = field
        if value:
            details["valor"] = value
        if expected_format:
            details["formato_esperado"] = expected_format
        super().__init__(message, details)


# ============================================================================
# FUNCIONES DE UTILIDAD PARA MANEJO DE EXCEPCIONES
# ============================================================================

def format_error_message(error: PlacasDataError) -> str:
    """
    Formatea un mensaje de error para mostrar al usuario.
    
    Args:
        error: Excepción del proyecto
        
    Returns:
        str: Mensaje formateado para consola
    """
    error_type = type(error).__name__
    separator = "=" * 60
    
    message = f"""
{separator}
❌ ERROR: {error_type}
{separator}
📝 Mensaje: {error.message}
"""
    
    if error.details:
        message += "📋 Detalles:\n"
        for key, value in error.details.items():
            message += f"   • {key}: {value}\n"
    
    message += separator
    return message


if __name__ == "__main__":
    # Demostración de las excepciones personalizadas
    print("=" * 60)
    print("DEMOSTRACIÓN DE EXCEPCIONES PERSONALIZADAS")
    print("=" * 60)
    
    # Ejemplo 1: DataReadError
    try:
        raise DataReadError(
            "No se pudo leer el archivo de datos",
            filepath="data/raw.csv",
            original_error=FileNotFoundError("Archivo no encontrado")
        )
    except PlacasDataError as e:
        print(format_error_message(e))
    
    # Ejemplo 2: SchemaError
    try:
        raise SchemaError(
            "El dataset no tiene las columnas requeridas",
            missing_columns=["placa", "estado_ANT"]
        )
    except PlacasDataError as e:
        print(format_error_message(e))
    
    # Ejemplo 3: SortingError
    try:
        raise SortingError(
            "Error durante la ejecución de Radix Sort",
            algorithm="radix_sort",
            data_size=1000
        )
    except PlacasDataError as e:
        print(format_error_message(e))
    
    print("\n✅ Todas las excepciones funcionan correctamente")
