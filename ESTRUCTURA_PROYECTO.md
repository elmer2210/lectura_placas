# Estructura del Proyecto - Sistema de Peaje Inteligente

## Árbol de Directorios

```
proyecto_placas_ecuador/
│
├── app/                              # Módulos core de algoritmos y análisis
│   ├── __init__.py
│   ├── analysis.py                  # Análisis estadístico de datos
│   ├── cleaning.py                  # Limpieza y validación de datos
│   ├── exceptions.py                # Excepciones personalizadas
│   ├── io.py                        # Entrada/salida de datos
│   ├── search.py                    # Búsqueda comparativa (Merge Sort vs Radix Sort)
│   └── sorting.py                   # Implementación de algoritmos de ordenamiento
│
├── data/                            # Archivos de datos
│   ├── placas_database.csv         # Base de datos de 1000 vehículos
│   ├── raw.csv                     # Datos originales (backup)
│   └── search_history.json         # Historial de búsquedas (generado)
│
├── flask_app/                       # Aplicación web Flask
│   ├── __init__.py
│   ├── config.py                   # Configuración de Flask
│   │
│   ├── services/                   # Servicios de negocio
│   │   ├── __init__.py
│   │   ├── database_loader.py     # Carga CSV en memoria (Singleton)
│   │   └── search_service.py      # Servicio de búsqueda con historial
│   │
│   ├── static/                     # Archivos estáticos
│   │   └── css/
│   │       └── peaje.css          # Estilos del sistema
│   │
│   └── templates/                  # Plantillas HTML
│       ├── base.html              # Template base con Bootstrap 5
│       └── pages/
│           ├── index.html         # Landing page
│           ├── peaje.html         # Simulador de peaje
│           ├── historial.html     # Vista de historial
│           └── reportes.html      # Análisis estadístico
│
├── notebooks/                       # Jupyter notebooks (análisis exploratorio)
│   └── analisis_completo.ipynb
│
├── .gitignore                      # Archivos ignorados por Git
├── generar_datos_prueba.py         # Script para generar datos de prueba
├── README.md                       # Documentación principal
├── REPORTES_DOCUMENTACION.md       # Documentación del módulo de reportes
├── requirements.txt                # Dependencias Python
└── run_flask.py                    # Punto de entrada de la aplicación
```

---

## Descripción de Archivos Principales

### **Archivos de Configuración**

- **`requirements.txt`**: Dependencias del proyecto
  - Flask 3.0.0
  - pandas 2.1.0
  - numpy 1.25.0
  - plotly 5.17.0

- **`flask_app/config.py`**: Configuración de entornos (development, production)

- **`.gitignore`**: Excluye archivos temporales y sensibles del control de versiones

### **Módulos Core (`app/`)**

- **`sorting.py`**: Implementación de Merge Sort y Radix Sort
- **`search.py`**: Búsqueda comparativa con Binary Search
- **`analysis.py`**: Estadísticas y métricas de rendimiento
- **`cleaning.py`**: Validación y limpieza de placas
- **`io.py`**: Lectura y escritura de datos CSV

### **Aplicación Web (`flask_app/`)**

#### Servicios:
- **`database_loader.py`**: Carga CSV en memoria con pandas (patrón Singleton)
- **`search_service.py`**: Ejecuta búsquedas y mantiene historial en JSON

#### Templates:
- **`base.html`**: Layout base con Bootstrap 5, Font Awesome
- **`index.html`**: Página de inicio con features del sistema
- **`peaje.html`**: Simulador principal con input de placa y visualizaciones
- **`historial.html`**: Tabla de búsquedas con filtros (peaje, algoritmo)
- **`reportes.html`**: Dashboard con 5 gráficos interactivos (Plotly.js)

### **Scripts Utilitarios**

- **`run_flask.py`**: Servidor Flask con todas las rutas y endpoints API
- **`generar_datos_prueba.py`**: Genera ~100 registros de prueba realistas

### **Documentación**

- **`README.md`**: Guía completa de instalación, uso y arquitectura
- **`REPORTES_DOCUMENTACION.md`**: Documentación técnica del módulo de reportes

---

## Rutas de la Aplicación

### **Páginas Web**
- `GET /` - Landing page
- `GET /peaje` - Simulador de peaje
- `GET /historial` - Vista de historial
- `GET /reportes` - Análisis estadístico

### **API REST**
- `POST /peaje/buscar` - Búsqueda comparativa de placa
- `GET /api/database/stats` - Estadísticas de la base de datos
- `GET /api/vehicles/random` - Vehículo aleatorio
- `GET /api/search/history?limit=50&peaje=...` - Historial de búsquedas
- `GET /api/reportes/analisis` - Análisis exploratorio de datos

---

## Archivos Eliminados (Limpieza)

Los siguientes archivos/carpetas fueron eliminados por no ser necesarios:

❌ `flask_app/blueprints/` - Carpeta vacía no utilizada
❌ `flask_app/static/img/` - Carpeta vacía
❌ `flask_app/static/js/` - Carpeta vacía (JavaScript inline en templates)
❌ `flask_app/templates/components/` - Carpeta vacía
❌ `data/report.txt` - Archivo antiguo del CLI
❌ `app/pipeline.py` - Módulo del CLI antiguo no usado en Flask
❌ `app/report.py` - Módulo del CLI antiguo no usado en Flask
❌ `**/__pycache__/` - Archivos compilados temporales (incluidos en .gitignore)

---

## Tecnologías Utilizadas

- **Backend**: Python 3.12+, Flask 3.0
- **Análisis de Datos**: pandas, NumPy
- **Frontend**: HTML5, CSS3, Bootstrap 5, Font Awesome
- **Visualizaciones**: Plotly.js 2.27.0
- **Patrón de Diseño**: Singleton (servicios), MVC (Flask)

---

## Comandos Útiles

```bash
# Instalar dependencias
pip install -r requirements.txt

# Generar datos de prueba
python generar_datos_prueba.py

# Iniciar servidor
python run_flask.py

# Acceder al sistema
http://localhost:5000
```

---

**Última actualización**: 2026-01-23
**Estado**: Proyecto completo y listo para producción
