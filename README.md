# Pertutti Reviews Scraper

Este proyecto contiene herramientas para scraping y análisis de reseñas del sitio web Pertutti.

## Archivos del proyecto

- `scraper.py` - Script principal para hacer scraping de reseñas
- `limpiar_datos.py` - Herramientas para limpiar y procesar los datos
- `cargar_db.py` - Script para cargar datos en la base de datos
- `consultar_db.py` - Script para consultar y analizar datos de la base de datos
- `pertutti_reviews.csv` - Datos originales de reseñas
- `pertutti_reviews_limpio.csv` - Datos limpiados
- `pertutti_reviews_procesado_y_ordenado.csv` - Datos procesados y ordenados

## Requisitos

- Python 3.x
- Bibliotecas requeridas (instalar con pip):
  - requests
  - beautifulsoup4
  - pandas
  - sqlite3 (incluido en Python)

## Uso

1. Ejecutar el scraper:
   ```bash
   python scraper.py
   ```

2. Limpiar los datos:
   ```bash
   python limpiar_datos.py
   ```

3. Cargar datos en la base de datos:
   ```bash
   python cargar_db.py
   ```

4. Consultar la base de datos:
   ```bash
   python consultar_db.py
   ```

## Configuración

Asegúrate de crear un entorno virtual antes de instalar las dependencias:

```bash
python -m venv venv
source venv/bin/activate  # En macOS/Linux
pip install -r requirements.txt
```