import sqlite3
import pandas as pd # Usaremos Pandas para mostrar la tabla bonita

ARCHIVO_DB = "pertutti.db"

def consultar_base_de_datos(query):
    """
    Se conecta a la BD, ejecuta una consulta (query) y muestra los resultados.
    """
    print(f"\n--- 🔎 Ejecutando Consulta ---")
    print(f"QUERY: {query}")
    
    try:
        # Nos conectamos a la base de datos
        conn = sqlite3.connect(ARCHIVO_DB)
        
        # Usamos Pandas para leer el resultado del SQL directamente
        # Esto es un atajo muy útil
        df_resultados = pd.read_sql_query(query, conn)
        
        # Cerramos la conexión
        conn.close()
        
        if df_resultados.empty:
            print("La consulta no devolvió resultados.")
            return

        # Imprimimos los resultados
        print(f"\n--- 📊 Resultados ({len(df_resultados)} filas) ---")
        print(df_resultados.to_string()) # .to_string() lo muestra completo

    except Exception as e:
        print(f"❌ Ocurrió un error al consultar la BD: {e}")

# --- ¡AQUÍ PROBAMOS NUESTRAS CONSULTAS! ---
# El script ejecutará la consulta que esté "descomentada"

# -----------------------------------------------------------------
# EJEMPLO 1: Contar el TOTAL de reseñas
query_contar_todo = "SELECT COUNT(*) as total_reseñas FROM reseñas;"
consultar_base_de_datos(query_contar_todo)
# -----------------------------------------------------------------


# -----------------------------------------------------------------
# EJEMPLO 2: Mostrar las 5 peores reseñas (rating 1)
query_peores_reseñas = """
     SELECT sucursal, autor_nombre, rating, fecha_publicacion, texto_reseña 
     FROM reseñas 
     WHERE rating = 1 
     LIMIT 5;
 """
consultar_base_de_datos(query_peores_reseñas)
# -----------------------------------------------------------------


# -----------------------------------------------------------------
# EJEMPLO 3: Contar cuántas reseñas tiene CADA sucursal
query_conteo_por_sucursal = """
     SELECT sucursal, COUNT(*) as total_reseñas
     FROM reseñas
     GROUP BY sucursal
     ORDER BY total_reseñas DESC;
     """
consultar_base_de_datos(query_conteo_por_sucursal)
# -----------------------------------------------------------------


# -----------------------------------------------------------------
# EJEMPLO 4: Ver la reseña más RECIENTE de todas
# query_mas_reciente = """
#     SELECT sucursal, autor_nombre, fecha_publicacion, texto_reseña
#     FROM reseñas
#     ORDER BY fecha_publicacion DESC
#     LIMIT 1;
# """
# consultar_base_de_datos(query_mas_reciente)
# -----------------------------------------------------------------