import pandas as pd
import re
from datetime import datetime
from dateutil.relativedelta import relativedelta 

# Asegúrate de haber corrido: pip install python-dateutil

ARCHIVO_ENTRADA = "pertutti_reviews.csv"
ARCHIVO_SALIDA = "pertutti_reviews_procesado_y_ordenado.csv" # Nuevo nombre de salida

print(f"🧹 Iniciando limpieza y procesamiento de {ARCHIVO_ENTRADA}...")

# --- Función para convertir fechas (sin cambios) ---
def convertir_fecha(texto_fecha):
    hoy = datetime.now()
    texto_fecha = str(texto_fecha).lower()

    try:
        if "ahora" in texto_fecha or "hoy" in texto_fecha:
            return hoy.date()
        if "ayer" in texto_fecha:
            return (hoy - relativedelta(days=1)).date()

        num_match = re.search(r'\d+', texto_fecha)
        num = int(num_match.group(0)) if num_match else 1

        if "día" in texto_fecha:
            return (hoy - relativedelta(days=num)).date()
        if "semana" in texto_fecha:
            return (hoy - relativedelta(weeks=num)).date()
        if "mes" in texto_fecha:
            return (hoy - relativedelta(months=num)).date()
        if "año" in texto_fecha:
            return (hoy - relativedelta(years=num)).date()
        
        return None
    except Exception:
        return None
# ------------------------------------

try:
    # 1. Leer el archivo CSV original
    df = pd.read_csv(ARCHIVO_ENTRADA)
    print(f"Datos originales: {len(df)} reseñas.")

    # 2. Limpieza de duplicados (como antes)
    df['largo_texto'] = df['texto_reseña'].fillna('').str.len()
    df = df.sort_values(by='largo_texto', ascending=False)
    columnas_duplicados = ['sucursal', 'autor_nombre', 'fecha', 'rating']
    df_limpio = df.drop_duplicates(subset=columnas_duplicados, keep='first')
    df_limpio = df_limpio.drop(columns=['largo_texto'])
    
    print(f"Datos después de eliminar duplicados: {len(df_limpio)} reseñas.")

    # 3. Convertir las fechas
    print("Convirtiendo fechas relativas a fechas reales...")
    df_limpio['fecha_publicacion'] = df_limpio['fecha'].apply(convertir_fecha)
    
    # 4. Reordenar las columnas
    columnas_ordenadas = [
        'sucursal', 
        'autor_nombre', 
        'fecha_publicacion', 
        'rating', 
        'texto_reseña',
        'fecha' 
    ]
    df_final = df_limpio[columnas_ordenadas]

    # --- ¡AQUÍ LA LÍNEA NUEVA! ---
    print("Ordenando el archivo final por sucursal y fecha...")
    df_final = df_final.sort_values(
        by=['sucursal', 'fecha_publicacion'], 
        ascending=[True, False] # Sucursal (A-Z), Fecha (Más nueva primero)
    )
    # -------------------------------

    # 5. Guardar el archivo final
    df_final.to_csv(ARCHIVO_SALIDA, index=False, encoding='utf-8-sig')

    print("\n--- ¡Procesamiento completado! ---")
    print(f"Total de reseñas únicas procesadas: {len(df_final)}.")
    print(f"✅ Archivo guardado como: {ARCHIVO_SALIDA}")

except FileNotFoundError:
    print(f"❌ ERROR: No se encontró el archivo '{ARCHIVO_ENTRADA}'.")
except Exception as e:
    print(f"❌ Ocurrió un error inesperado: {e}")