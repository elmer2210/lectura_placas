"""
================================================================================
SERVICIO DE CARGA DE BASE DE DATOS EN MEMORIA
================================================================================
Universidad Nacional de Chimborazo
Facultad de Ingeniería - Ciencia de Datos e Inteligencia Artificial
Asignatura: Estructura de Datos

Este servicio carga la base de datos CSV al iniciar la aplicación Flask
y la mantiene en memoria para búsquedas rápidas.

OBJETIVO:
Simular una base de datos real que estaría en un servidor PostgreSQL/MySQL,
pero usando CSV por simplicidad académica.

PATRÓN: Singleton (una sola instancia global)

Autores: Juan David Ruiz Jara, Ian Nolivos, Kléver Castillo,
         Estefany Condor, Natasha Nuñez, Elmer Rivadeneira
================================================================================
"""

import pandas as pd
import os
from app.io import read_csv
from app.cleaning import validate_schema, convert_types


class VehicleDatabase:
    """
    Base de datos de vehículos en memoria.

    Esta clase carga el archivo CSV una sola vez al iniciar la aplicación
    y lo mantiene en memoria RAM para acceso rápido durante las búsquedas.

    VENTAJAS:
    - Acceso extremadamente rápido (datos en RAM)
    - Sin latencia de I/O de disco
    - Ideal para datasets pequeños-medianos (< 1 millón registros)

    LIMITACIONES:
    - Consume memoria RAM
    - No es persistente (cambios se pierden al reiniciar)
    - No escala para datasets muy grandes

    EN UN SISTEMA REAL:
    Se usaría PostgreSQL, MySQL o MongoDB con conexiones pooling,
    índices B-tree para búsquedas rápidas, y caché Redis.
    """

    def __init__(self, csv_path='data/placas_database.csv'):
        """
        Inicializa la base de datos cargando el CSV.

        Este proceso se ejecuta UNA SOLA VEZ al iniciar la aplicación Flask.

        Args:
            csv_path (str): Ruta al archivo CSV de la base de datos

        Raises:
            DataReadError: Si el archivo no existe o está corrupto
            SchemaError: Si el esquema del CSV es inválido
        """
        print("\n" + "=" * 70)
        print("🔄 CARGANDO BASE DE DATOS DE VEHÍCULOS EN MEMORIA")
        print("=" * 70)

        # Verificar que el archivo existe
        if not os.path.exists(csv_path):
            # Si no existe, usar el archivo raw.csv
            alt_path = 'data/raw.csv'
            if os.path.exists(alt_path):
                print(f"⚠️  Usando {alt_path} como base de datos")
                csv_path = alt_path
            else:
                raise FileNotFoundError(f"No se encontró el archivo de base de datos: {csv_path}")

        # Cargar CSV usando módulo de I/O existente
        self.df = read_csv(csv_path)

        # Validar esquema
        validate_schema(self.df)

        # Convertir tipos de datos
        self.df = convert_types(self.df)

        # Crear índice por placa para búsqueda rápida O(1)
        # Nota: set_index optimiza búsquedas con .loc[]
        self.df.set_index('placa', inplace=True, drop=False)

        # Estadísticas de carga
        print(f"\n✅ Base de datos cargada exitosamente:")
        print(f"   📊 Total de registros: {len(self.df):,}")
        print(f"   🚗 Placas únicas: {self.df['placa'].nunique():,}")
        print(f"   📍 Ubicaciones: {self.df['ubicacion_camara'].nunique()}")
        print(f"   💾 Memoria usada: {self.df.memory_usage(deep=True).sum() / 1024:.2f} KB")
        print("=" * 70 + "\n")

    def get_all_plates(self) -> list:
        """
        Retorna lista de todas las placas para ordenamiento.

        Returns:
            list: Lista de strings con todas las placas
        """
        return self.df['placa'].tolist()

    def get_vehicle_by_plate(self, plate: str) -> dict:
        """
        Busca vehículo por placa usando índice de Pandas (búsqueda directa O(1)).

        NOTA IMPORTANTE:
        Esta búsqueda NO usa los algoritmos Merge/Radix Sort.
        Es una búsqueda directa usando el índice de Pandas.

        Los algoritmos Merge/Radix Sort se usan en el módulo search.py
        para comparación académica de rendimiento.

        Args:
            plate (str): Placa a buscar (ej: "ABC-1234")

        Returns:
            dict: Datos del vehículo, o None si no existe
        """
        plate = plate.upper().strip()

        if plate in self.df.index:
            return self.df.loc[plate].to_dict()
        return None

    def get_all_vehicles(self) -> pd.DataFrame:
        """
        Retorna DataFrame completo de vehículos.

        Returns:
            pd.DataFrame: Copia del DataFrame completo
        """
        return self.df.reset_index(drop=True).copy()

    def get_statistics(self) -> dict:
        """
        Retorna estadísticas de la base de datos.

        Útil para el dashboard y API.

        Returns:
            dict con:
            - total_vehiculos: número total de registros
            - placas_unicas: número de placas diferentes
            - estados: distribución de estados ANT
            - ubicaciones: distribución de ubicaciones
        """
        return {
            'total_vehiculos': len(self.df),
            'placas_unicas': self.df['placa'].nunique(),
            'estados': self.df['estado_ANT'].value_counts().to_dict(),
            'ubicaciones': self.df['ubicacion_camara'].value_counts().to_dict()
        }


# ============================================================================
# PATRÓN SINGLETON - INSTANCIA GLOBAL ÚNICA
# ============================================================================

_db_instance = None


def get_database() -> VehicleDatabase:
    """
    Obtiene la instancia global de la base de datos.

    PATRÓN SINGLETON:
    Garantiza que solo exista UNA instancia de VehicleDatabase en toda
    la aplicación, evitando cargar el CSV múltiples veces.

    FLUJO:
    1. Primera llamada: crea instancia y carga CSV
    2. Llamadas subsecuentes: retorna instancia existente

    Returns:
        VehicleDatabase: Instancia única de la base de datos

    Example:
        >>> db = get_database()
        >>> print(len(db.get_all_plates()))
    """
    global _db_instance

    if _db_instance is None:
        _db_instance = VehicleDatabase()

    return _db_instance


if __name__ == "__main__":
    # Prueba del servicio
    print("PRUEBA DEL SERVICIO DE BASE DE DATOS")
    print("=" * 70)

    # Cargar base de datos
    db = get_database()

    # Probar métodos
    print(f"\n📊 Estadísticas:")
    stats = db.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")

    print(f"\n🚗 Primeras 5 placas:")
    plates = db.get_all_plates()[:5]
    for plate in plates:
        print(f"   {plate}")

    print("\n✅ Prueba completada")
