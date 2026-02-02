"""
Servicio de búsqueda que integra la base de datos con los algoritmos.
Mantiene historial de búsquedas para análisis estadístico.
"""

from flask_app.services.database_loader import get_database
from app.search import comparative_search
import json
import os
from datetime import datetime


class SearchService:
    """
    Servicio de búsqueda para el sistema de peaje.

    Responsabilidades:
    - Ejecutar búsquedas comparativas
    - Mantener historial de búsquedas
    - Guardar historial en archivo JSON
    """

    def __init__(self):
        self.db = get_database()
        self.history = []
        self._load_history()

    def search_plate(self, plate: str) -> dict:
        """
        Busca una placa usando ambos algoritmos y retorna comparativa.

        Args:
            plate: Placa a buscar (ej: "ABC-1234")

        Returns:
            Dict con resultados de búsqueda y comparativa de algoritmos
        """
        # Obtener lista de vehículos como diccionarios
        vehicles = self.db.get_all_vehicles().to_dict('records')

        # Realizar búsqueda comparativa usando ambos algoritmos
        result = comparative_search(vehicles, plate)

        # Guardar en historial
        self._save_to_history(result)

        return result

    def _load_history(self):
        """Carga historial desde archivo JSON si existe."""
        try:
            if os.path.exists('data/search_history.json'):
                with open('data/search_history.json', 'r') as f:
                    self.history = json.load(f)
        except:
            self.history = []

    def _save_to_history(self, result: dict):
        """Guarda búsqueda en historial."""
        merge_res = result['merge_sort_result']
        radix_res = result['radix_sort_result']

        entry = {
            'timestamp': datetime.now().isoformat(),
            'plate': result['plate_searched'],
            'found': result['found'],
            'winner': result['winner'],
            'merge_time': merge_res['total_time_ms'],
            'radix_time': radix_res['total_time_ms'],
            # Métricas de algoritmos
            'merge_comparisons': merge_res['total_comparisons'],
            'merge_search_comparisons': merge_res['search_comparisons'],
            'merge_recursive_calls': merge_res['recursive_calls'],
            'radix_operations': radix_res['sort_operations'],
            'radix_search_comparisons': radix_res['search_comparisons'],
            'radix_passes': radix_res['passes'],
            # Incluir datos del vehículo si fue encontrado
            'peaje_ciudad': result['vehicle']['peaje_ciudad'] if result['found'] and result['vehicle'] else None,
            'estado_ANT': result['vehicle']['estado_ANT'] if result['found'] and result['vehicle'] else None,
            'ubicacion_camara': result['vehicle']['ubicacion_camara'] if result['found'] and result['vehicle'] else None
        }
        self.history.append(entry)

        # Guardar en archivo JSON
        try:
            os.makedirs('data', exist_ok=True)
            with open('data/search_history.json', 'w') as f:
                json.dump(self.history, f, indent=2)
        except:
            pass

    def get_history(self, limit=50):
        """Retorna historial de búsquedas."""
        return self.history[-limit:]


# Instancia global (Singleton)
_search_service = None


def get_search_service():
    """Obtiene instancia global del servicio de búsqueda."""
    global _search_service
    if _search_service is None:
        _search_service = SearchService()
    return _search_service
