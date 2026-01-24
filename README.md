# Sistema de Peaje Inteligente - UNACH

## Proyecto Académico de Estructura de Datos

**Universidad Nacional de Chimborazo**
Facultad de Ingeniería - Ciencia de Datos e Inteligencia Artificial
Asignatura: Estructura de Datos
Periodo: Octubre 2025 - Febrero 2026

### Autores
- Juan David Ruiz Jara
- Ian Nolivos
- Kléver Castillo
- Estefany Condor
- Natasha Nuñez
- Elmer Rivadeneira

### Personal Académico
- **Director de Carrera**: Mg. Milton López Ramos
- **Profesora**: Ing. Evelyn Rosero

---

## Descripción del Proyecto

Sistema web que simula un **peaje inteligente con reconocimiento automático de placas vehiculares**, implementando una **comparativa en tiempo real de algoritmos de ordenamiento** (Merge Sort vs Radix Sort) para búsqueda de vehículos.

### Objetivo Académico

Comparar el rendimiento de dos algoritmos de ordenamiento clásicos en un caso de uso real:
- **Merge Sort + Binary Search**: O(n log n) + O(log n)
- **Radix Sort + Binary Search**: O(d×(n+k)) + O(log n)

---

## Características

✅ **Simulador de Cámara**: Input manual que simula captura automática de placas
✅ **Búsqueda Comparativa**: Ejecuta ambos algoritmos simultáneamente
✅ **Visualización de Resultados**: Gráficos interactivos con Plotly.js
✅ **Información del Vehículo**: Datos completos + estado ANT (Habilitado/Suspendido/Bloqueado)
✅ **Métricas Detalladas**: Tiempos de ejecución, comparaciones, operaciones
✅ **API REST**: Endpoints para consumir datos de la base de datos
✅ **Historial de Búsquedas**: Registro en JSON para análisis estadístico
✅ **Vista de Historial**: Lista ordenada de vehículos capturados con filtros por peaje y algoritmo ganador
✅ **Reportes Estadísticos**: Análisis exploratorio de datos con visualizaciones interactivas (Pandas + Plotly)

---

## Instalación

### 1. Clonar el repositorio
```bash
cd proyecto_placas_ecuador
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Verificar archivos de datos
Asegúrate de que exista el archivo `data/placas_database.csv` o `data/raw.csv`.

---

## Ejecución

### Iniciar la aplicación Flask
```bash
python run_flask.py
```

El sistema estará disponible en:
- **Página Principal**: http://localhost:5000/
- **Simulador de Peaje**: http://localhost:5000/peaje
- **Historial de Búsquedas**: http://localhost:5000/historial
- **Reportes Estadísticos**: http://localhost:5000/reportes
- **API REST**: http://localhost:5000/api/

---

## Uso del Simulador

1. Abre http://localhost:5000/peaje
2. Ingresa una placa en formato **ABC-1234** (3 letras - 4 números)
3. Click en "Buscar Vehículo" o presiona Enter
4. El sistema ejecutará búsqueda con **ambos algoritmos** y mostrará:
   - ✅ Información del vehículo encontrado
   - ⚠️ Estado ANT (Habilitado/Suspendido/Bloqueado)
   - 📊 **Gráfico comparativo** de tiempos de ejecución
   - 📈 **Tabla detallada** con métricas de cada algoritmo
   - 🏆 **Algoritmo ganador** con porcentaje de ventaja

### Función "Placa Aleatoria"
Click en el botón para obtener una placa aleatoria de la base de datos para testing rápido.

---

## Vista de Historial

1. Abre http://localhost:5000/historial
2. Visualiza todos los vehículos capturados ordenados por fecha
3. Utiliza los filtros disponibles:
   - **Filtrar por Peaje**: Selecciona un peaje específico (ej: "Peaje Rumiñahui")
   - **Número de registros**: Elige cuántos registros mostrar (50, 100, 200, 500, todos)
   - **Algoritmo ganador**: Filtra por Merge Sort o Radix Sort
4. La tabla muestra:
   - ✅ Fecha y hora de captura
   - 🚗 Placa del vehículo
   - 📍 Peaje y ubicación de cámara
   - ⚠️ Estado ANT con colores
   - 🏆 Algoritmo ganador con badge
   - ⏱️ Tiempos de ejecución de ambos algoritmos
   - 📊 Ventaja porcentual del ganador

---

## Vista de Reportes

1. Abre http://localhost:5000/reportes
2. Visualiza el análisis exploratorio de datos (EDA) del historial:
   - **Métricas Principales**: Total búsquedas, tasa de éxito, total alertas, tiempo promedio
   - **TOP 10 Placas con Alertas**: Ranking de placas suspendidas/bloqueadas más capturadas
   - **Distribución por Estado ANT**: Gráfico circular (Habilitada, Suspendida, Bloqueada)
   - **Algoritmo Ganador**: Comparativa de rendimiento entre Merge Sort vs Radix Sort
   - **Distribución por Hora**: Análisis temporal de búsquedas durante el día
   - **TOP 10 Peajes**: Peajes con mayor número de capturas
   - **Tiempos Promedio**: Comparación de rendimiento promedio de algoritmos
   - **Búsquedas por Día**: Serie temporal de actividad del sistema

3. Los datos son generados automáticamente desde el historial JSON
4. Todas las visualizaciones son interactivas con Plotly.js

### Generar Datos de Prueba

Para poblar el sistema con ~100 búsquedas simuladas:
```bash
python generar_datos_prueba.py
```

---

## Arquitectura del Proyecto

```
proyecto_placas_ecuador/
├── app/                          # Lógica core (algoritmos y análisis)
│   ├── sorting.py               # Merge Sort y Radix Sort
│   ├── search.py                # Búsqueda con algoritmos (NUEVO)
│   ├── cleaning.py, analysis.py, etc.
│
├── flask_app/                   # Aplicación web Flask
│   ├── services/
│   │   ├── database_loader.py  # Carga CSV en memoria
│   │   └── search_service.py   # Servicio de búsqueda
│   ├── templates/
│   │   └── pages/
│   │       ├── index.html      # Landing page
│   │       └── peaje.html      # Simulador principal
│   └── static/css/peaje.css    # Estilos y animaciones
│
├── data/
│   ├── placas_database.csv     # Base de datos (1000 vehículos)
│   └── search_history.json     # Historial de búsquedas
│
├── run_flask.py                # Punto de entrada Flask
└── requirements.txt            # Dependencias
```

---

## Endpoints de API

### `POST /peaje/buscar`
Ejecuta búsqueda comparativa de una placa.

**Request:**
```json
{
  "placa": "ABC-1234"
}
```

**Response:**
```json
{
  "success": true,
  "found": true,
  "vehicle": { ... },
  "comparison": {
    "winner": "Merge Sort",
    "percentage_faster": 42.15,
    "merge_sort": { "total_time": 2.45, ... },
    "radix_sort": { "total_time": 4.23, ... }
  }
}
```

### `GET /api/database/stats`
Retorna estadísticas de la base de datos.

### `GET /api/vehicles/random`
Retorna un vehículo aleatorio (útil para testing).

### `GET /api/search/history?limit=50&peaje=Peaje%20Rumiñahui`
Retorna historial de búsquedas con filtros opcionales.

**Parámetros:**
- `limit`: Número máximo de registros (default: 50)
- `peaje`: Filtrar por peaje específico (opcional)

### `GET /api/reportes/analisis`
Retorna análisis exploratorio de datos del historial.

**Response:**
```json
{
  "success": true,
  "total_busquedas": 100,
  "tasa_exito": 87.0,
  "top_alertas": [
    {
      "placa": "XYZ-1234",
      "total_alertas": 5,
      "estado": "Bloqueada",
      "peaje": "Peaje Rumiñahui"
    }
  ],
  "distribucion_estados": {
    "Habilitada": 83,
    "Suspendida": 1,
    "Bloqueada": 3
  },
  "distribucion_horas": { ... },
  "distribucion_peajes": { ... },
  "algoritmo_ganador": {
    "Merge Sort": 45,
    "Radix Sort": 55
  },
  "tiempos_promedio": {
    "merge_sort": 1.7234,
    "radix_sort": 1.4521
  },
  "busquedas_por_dia": { ... },
  "top_peajes": { ... }
}
```

---

## Algoritmos Implementados

### Merge Sort + Binary Search
- **Complejidad**: O(n log n) + O(log n) = O(n log n)
- **Ventajas**: Rendimiento garantizado, estable
- **Desventajas**: Requiere O(n) espacio auxiliar

### Radix Sort + Binary Search
- **Complejidad**: O(d×(n+k)) + O(log n) ≈ O(d×n)
- **Ventajas**: Lineal para datos de longitud fija
- **Desventajas**: Mayor overhead para conjuntos pequeños

### Código Altamente Comentado
Los módulos `app/sorting.py` y `app/search.py` contienen **comentarios extensos** explicando:
- Teoría de algoritmos
- Complejidad temporal y espacial
- Ventajas y desventajas
- Casos de uso ideales

---

## Tecnologías Utilizadas

- **Backend**: Flask 3.0
- **Frontend**: Bootstrap 5, Font Awesome 6
- **Visualización**: Plotly.js 2.27
- **Análisis de Datos**: Pandas 2.1, NumPy 1.25
- **Formato de Datos**: CSV, JSON

---

## Capturas de Pantalla

### Simulador de Peaje
- Input de placa con simulación de cámara
- Búsqueda en tiempo real con loading spinner

### Resultados
- Tarjeta con información del vehículo
- Estado ANT destacado con colores (verde/amarillo/rojo)
- Gráfico de barras comparativo (Plotly interactivo)
- Tabla con métricas detalladas
- Badge del algoritmo ganador

---

## Licencia

Proyecto Académico - Universidad Nacional de Chimborazo © 2026
