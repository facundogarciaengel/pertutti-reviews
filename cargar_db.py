import pandas as pd
import sqlite3

# Nombres de los archivos
ARCHIVO_CSV = "pertutti_reviews_procesado_y_ordenado.csv"
ARCHIVO_DB = "pertutti.db" # Este será el nuevo archivo de base de datos

# Nombre de la tabla que crearemos
NOMBRE_TABLA = "reseñas"

print(f"🚀 Iniciando carga de {ARCHIVO_CSV} a la base de datos {ARCHIVO_DB}...")

try:
    # 1. Leer los datos limpios del CSV
    df = pd.read_csv(ARCHIVO_CSV)
    print(f"Se leyeron {len(df)} reseñas del archivo CSV.")

    # 2. Conectar a la base de datos SQLite
    # (Si el archivo no existe, sqlite3 lo crea automáticamente)
    conn = sqlite3.connect(ARCHIVO_DB)
    cursor = conn.cursor()
    
    # 3. Crear la tabla 'reseñas'
    # Usamos "IF NOT EXISTS" para no borrarla si ya existe
    query_crear_tabla = f"""
    CREATE TABLE IF NOT EXISTS {NOMBRE_TABLA} (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sucursal TEXT,
        autor_nombre TEXT,
        fecha_publicacion DATE,
        rating INTEGER,
        texto_reseña TEXT,
        fecha_original TEXT
    );
    """
    cursor.execute(query_crear_tabla)
    print(f"Tabla '{NOMBRE_TABLA}' asegurada (creada o ya existente).")

    # 4. Insertar los datos del DataFrame en la tabla SQLite
    # 'to_sql' es una función de Pandas que hace esto automáticamente
    # if_exists='replace' borrará la tabla si ya existe y la creará de nuevo
    # (Esto es útil para correr el script varias veces sin duplicar datos)
    df.to_sql(NOMBRE_TABLA, conn, if_exists='replace', index=False)

    # 5. Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

    print("\n--- ¡Carga completada! ---")
    print(f"✅ Se insertaron {len(df)} reseñas en la tabla '{NOMBRE_TABLA}'.")
    print(f"Tu base de datos está lista en el archivo: {ARCHIVO_DB}")

except FileNotFoundError:
    print(f"❌ ERROR: No se encontró el archivo '{ARCHIVO_CSV}'.")
    print("Asegúrate de haber corrido el script de limpieza primero.")
except Exception as e:
    print(f"❌ Ocurrió un error inesperado durante la carga a la BD: {e}")