# Documentación de Módulo de Reportes Estadísticos

## Descripción General

El módulo de reportes proporciona **análisis exploratorio de datos (EDA)** del historial de búsquedas del sistema de peaje inteligente, utilizando Pandas para procesamiento de datos y Plotly.js para visualizaciones interactivas.

---

## Archivos Implementados

### 1. `flask_app/templates/pages/reportes.html`
- **Descripción**: Página web principal de reportes con visualizaciones interactivas
- **Tecnologías**: HTML5, Bootstrap 5, Plotly.js 2.27.0, JavaScript ES6
- **Características**:
  - 4 métricas principales destacadas (total búsquedas, tasa éxito, alertas, tiempo promedio)
  - Tabla TOP 10 placas con más alertas
  - 7 visualizaciones interactivas con Plotly
  - Diseño responsive con gradientes y animaciones
  - Navegación integrada con el resto del sistema

### 2. `run_flask.py` - Nuevas Rutas y Endpoints

#### Ruta: `GET /reportes`
```python
@app.route('/reportes')
def reportes():
    """Página de reportes y análisis estadístico"""
```
- Renderiza la página principal de reportes

#### Endpoint: `GET /api/reportes/analisis`
```python
@app.route('/api/reportes/analisis')
def get_analisis_datos():
    """Análisis exploratorio de datos del historial"""
```
- **Procesamiento con Pandas**: Convierte historial JSON a DataFrame
- **Extracción de features temporales**: hora, día_semana, fecha
- **Análisis implementados**:
  1. TOP 10 Placas con más alertas (Suspendidas/Bloqueadas)
  2. Distribución por Estado ANT
  3. Distribución por Hora del Día (0-23)
  4. Distribución por Peaje
  5. Algoritmo Ganador (Merge Sort vs Radix Sort)
  6. Tasa de Éxito de búsquedas
  7. Tiempos Promedio de algoritmos
  8. Búsquedas por Día (serie temporal)
  9. TOP 10 Peajes con más capturas

### 3. `generar_datos_prueba.py`
- **Descripción**: Script para generar ~100 búsquedas simuladas en el historial
- **Características**:
  - Genera datos realistas con timestamps en últimos 7 días
  - 90% de búsquedas exitosas, 10% no encontradas
  - Variedad de estados ANT (mayoría Habilitada, algunas Suspendidas/Bloqueadas)
  - Tiempos de ejecución simulados realistas
  - Determinación automática del algoritmo ganador

**Uso:**
```bash
python generar_datos_prueba.py
```

---

## Visualizaciones Implementadas

### 1. Métricas Principales (Cards)
- Total de búsquedas
- Tasa de éxito (%)
- Total de alertas (placas suspendidas/bloqueadas)
- Tiempo promedio de ejecución

### 2. TOP 10 Placas con Alertas (Tabla)
- Ranking visual con badges de colores
- Placa, total alertas, estado, último peaje
- Solo muestra placas con estado Suspendida o Bloqueada

### 3. Gráfico: Distribución por Estado ANT (Pie Chart)
- **Tipo**: Gráfico circular
- **Colores**: Verde (Habilitada), Amarillo (Suspendida), Rojo (Bloqueada)
- **Muestra**: Porcentaje y cantidad de cada estado

### 4. Gráfico: Algoritmo Ganador (Pie Chart)
- **Tipo**: Gráfico circular
- **Colores**: Azul (Merge Sort), Verde (Radix Sort)
- **Muestra**: Proporción de veces que cada algoritmo fue más rápido

### 5. Gráfico: Distribución por Hora del Día (Bar Chart)
- **Tipo**: Gráfico de barras vertical
- **Eje X**: Horas del día (0:00 - 23:00)
- **Eje Y**: Número de búsquedas
- **Color**: Escala de colores Viridis según intensidad

### 6. Gráfico: TOP 10 Peajes (Horizontal Bar Chart)
- **Tipo**: Gráfico de barras horizontal
- **Muestra**: Los 10 peajes con más capturas
- **Ordenado**: De mayor a menor número de capturas

### 7. Gráfico: Tiempos Promedio (Bar Chart)
- **Tipo**: Gráfico de barras comparativo
- **Compara**: Tiempo promedio Merge Sort vs Radix Sort
- **Unidad**: Milisegundos (ms)
- **Incluye**: Valores exactos en las barras

### 8. Gráfico: Búsquedas por Día (Line Chart)
- **Tipo**: Gráfico de línea con marcadores
- **Eje X**: Fechas
- **Eje Y**: Número de búsquedas
- **Muestra**: Tendencia temporal de actividad

---

## Análisis con Pandas

### Transformaciones Aplicadas
```python
# Conversión de timestamp a datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Extracción de componentes temporales
df['hora'] = df['timestamp'].dt.hour
df['dia_semana'] = df['timestamp'].dt.day_name()
df['fecha'] = df['timestamp'].dt.date.astype(str)

# Filtrado por estado (alertas)
df_alertas = df[df['estado_ANT'].isin(['Suspendida', 'Bloqueada'])]

# Agregaciones con value_counts()
estados_dist = df['estado_ANT'].value_counts().to_dict()
horas_dist = df['hora'].value_counts().sort_index().to_dict()

# Cálculos estadísticos
tasa_exito = (df['found'].sum() / len(df)) * 100
tiempo_merge_promedio = df['merge_time'].mean()
```

---

## Integración con Sistema Existente

### Navegación Actualizada
Todas las páginas ahora incluyen enlace a "Reportes":
- `index.html` - Landing page (añadida card de reportes)
- `peaje.html` - Simulador (añadido link en navbar)
- `historial.html` - Historial (añadido link en navbar)
- `reportes.html` - Nueva página de reportes

### Actualización del README
- Nueva sección "Vista de Reportes"
- Documentación del endpoint `/api/reportes/analisis`
- Instrucciones para generar datos de prueba

---

## Tecnologías Utilizadas

- **Backend**: Flask, Pandas, NumPy
- **Frontend**: Bootstrap 5, Plotly.js 2.27.0, JavaScript ES6
- **Visualización**: Plotly (pie charts, bar charts, line charts)
- **Análisis**: Pandas (DataFrame, value_counts, groupby, agregaciones)
- **Diseño**: CSS3 con gradientes, flexbox, animaciones

---

## Ejemplo de Respuesta del API

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
  "distribucion_horas": {
    "0": 2, "1": 1, "8": 12, "14": 15, ...
  },
  "distribucion_peajes": {
    "Peaje Rumiñahui": 25,
    "Peaje Ambato": 18,
    ...
  },
  "algoritmo_ganador": {
    "Merge Sort": 45,
    "Radix Sort": 55
  },
  "tiempos_promedio": {
    "merge_sort": 1.7234,
    "radix_sort": 1.4521
  },
  "busquedas_por_dia": {
    "2026-01-17": 12,
    "2026-01-18": 15,
    ...
  },
  "top_peajes": {
    "Peaje Rumiñahui": 25,
    "Peaje Ambato": 18,
    ...
  }
}
```

---

## Acceso al Sistema

1. Iniciar servidor: `python run_flask.py`
2. Acceder a reportes: http://localhost:5000/reportes
3. Ver API de análisis: http://localhost:5000/api/reportes/analisis

---

## Mantenimiento y Escalabilidad

### Para añadir nuevas visualizaciones:
1. Añadir análisis en el endpoint `/api/reportes/analisis` (run_flask.py)
2. Crear nueva función de gráfico JavaScript en reportes.html
3. Llamar la función desde `cargarAnalisis()`

### Para personalizar gráficos:
Modificar configuración de Plotly en las funciones `generar*()` de reportes.html:
```javascript
const layout = {
    height: 400,
    xaxis: { title: 'Título Eje X' },
    yaxis: { title: 'Título Eje Y' },
    // ... más opciones
};
```

---

## Notas Técnicas

- Los reportes se generan en **tiempo real** desde el historial JSON
- No requiere base de datos adicional
- Las visualizaciones son **100% interactivas** (zoom, hover, pan)
- El análisis con Pandas es **eficiente** incluso con miles de registros
- Los gráficos son **responsive** y se adaptan a diferentes tamaños de pantalla
