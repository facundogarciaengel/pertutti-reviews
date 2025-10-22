import time
import pandas as pd
from playwright.sync_api import sync_playwright
import re # Para expresiones regulares

# 1. LISTA DE OBJETIVOS (AHORA CON LAS URLS CORRECTAS)
sucursales = [
    {"nombre": "ABASTO", "url": "https://www.google.com/maps/place/Pertutti/@-34.6041703,-58.4105629,15z/data=!4m2!3m1!1s0x0:0xb795a3737806e661?sa=X&ved=2ahUKEwi-0oGtvrvzAhU8HrkGHYurBZYQ_BJ6BAhnEAU"},
    {"nombre": "ADROGUÉ", "url": "https://www.google.com/maps/place/Pertutti/@-34.7999937,-58.3989257,17z/data=!3m1!4b1!4m5!3m4!1s0x95bcd3153ab68947:0x5c7ad323c831c9cb!8m2!3d-34.7999937!4d-58.396737"},
    {"nombre": "AV. SANTA FÉ", "url": "https://www.google.com/maps/place/Pertutti/@-34.59598,-58.3971862,18.87z/data=!4m13!1m7!3m6!1s0x95bcca9668b521fd:0xf00f45bc93bb86bf!2sAv.+Santa+Fe+2020,+C1113+CABA!3b1!8m2!3d-34.5959736!4d-58.3965339!3m4!1s0x95bcca96695db245:0x1ffe205afcfe933a!8m2!3d-34.5958073!4d-58.3965011"},
    {"nombre": "AVELLANEDA", "url": "https://www.google.com/maps/place/Pertutti/@-34.6619249,-58.3674991,17z/data=!3m1!4b1!4m5!3m4!1s0x95a33351e4698d3f:0x82778a554ef59360!8m2!3d-34.6619249!4d-58.3653104"},
    {"nombre": "LOMAS DE ZAMORA", "url": "https://www.google.com/maps/place/Restaurante+Pertutti/@-34.7641945,-58.4025679,17z/data=!3m1!4b1!4m5!3m4!1s0x95bcd2eb7e1cdd41:0xa568e078811991f0!8m2!3d-34.7641956!4d-58.4003686"},
    {"nombre": "LONDON CITY", "url": "https://www.google.com/maps/place/London+City/@-34.6084128,-58.377093,17z/data=!3m1!4b1!4m9!1m2!2m1!1sAv.+de+Mayo+599+pertutti!3m5!1s0x95bccad3ac16ce41:0x613d6e53fc808781!8m2!3d-34.6083973!4d-58.3749063!15sChhBdi4gZGUgTWF5byA1OTkgcGVydHV0dGlaGSIXYXYgZGUgbWF5byA1OTkgcGVydHV0dGmSARNldXJvcGVhbl9yZXN0YXVyYW50mgEkQ2hkRFNVaE5NRzluUzBWSlEwRm5TVU41Y1U5aFIybEJSUkFC"},
    {"nombre": "PLAZA DE MAYO", "url": "https://www.google.com/maps/place/Pertutti+Suc.+Plaza+de+Mayo/@-34.609234,-58.3755247,17z/data=!3m1!4b1!4m5!3m4!1s0x95bccb68fb30e23b:0xb584a8a55cdf420f!8m2!3d-34.6092376!4d-58.37343"}
]

# 2. LISTA PARA ALMACENAR TODOS LOS DATOS
all_reviews_data = []

print("🚀 Iniciando el scraper de Pertutti... (v10 - Usando URLs oficiales)")

# 3. BUCLE PRINCIPAL
for sucursal in sucursales:
    print(f"\n--- 🔄 Procesando sucursal: {sucursal['nombre']} ---")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False) 
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",
            locale="es-AR", # Le decimos que preferimos español de Argentina
            viewport={'width': 1280, 'height': 1024}
        )
        page = context.new_page()

        try:
            # USAMOS LA URL DE LA LISTA
            url = sucursal['url']
            print(f"Navegando a: {url}")
            page.goto(url)
            page.wait_for_timeout(5000) # Espera 5 seg a que cargue y redirija

            # MANEJAR POP-UP DE COOKIES
            try:
                print("Buscando pop-up de cookies...")
                accept_button = page.locator('form button:has-text-matches("Aceptar todo|Accept all", "i")').first()
                accept_button.click(timeout=3000)
                print("Pop-up de cookies aceptado.")
                page.wait_for_timeout(2000)
            except Exception:
                print("No se encontró pop-up de cookies (o ya fue aceptado).")
            
            # --- PAUSA PARA VERIFICAR ---
            print("\n🛑 PAUSANDO EL SCRIPT. Verifica la ventana del navegador.")
            print("Ahora sí debería cargar la página de Pertutti. Dale a 'Resume' (▶️) en el Inspector para continuar.")
            page.pause()
            
            # CLIC EN "OPINIONES/REVISIONES"
            print("Buscando la pestaña de opiniones...")
            # AGREGAMOS "REVISIONES" AL SELECTOR
            reviews_button = page.get_by_role("tab", name=re.compile("Opiniones|Reviews|Revisiones", re.IGNORECASE))
            reviews_button.click(timeout=10000) 
            
            print("Clic en la pestaña exitoso.")
            page.wait_for_timeout(2000)
            
            # LÓGICA DE SCROLL (MÉTODO NUEVO Y MÁS ROBUSTO)
            print("Iniciando scroll con simulación de teclado...")
            
            last_reviews_count = 0
            for i in range(20): # Hacemos scroll un máximo de 20 veces (límite de seguridad)
                page.keyboard.press('End') # Simulamos presionar la tecla "Fin"
                print(f"Scroll #{i+1}...")
                page.wait_for_timeout(2500) # Esperamos que cargue

                current_reviews_count = page.locator('[data-review-id]').count()
                if current_reviews_count == last_reviews_count:
                    print("Llegamos al final, no cargaron más reseñas.")
                    break
                last_reviews_count = current_reviews_count

            print(f"Carga finalizada. Total de reseñas: {last_reviews_count}")

            # EXTRACCIÓN DE DATOS
            print("Extrayendo datos de las reseñas...")
            review_cards = page.locator('[data-review-id]').all()
            
            if not review_cards:
                 print(f"No se encontraron tarjetas de reseñas para {sucursal['nombre']}.")
                 browser.close()
                 continue 

            for card in review_cards:
                try:
                    autor_nombre = card.locator('.d4r55').inner_text(timeout=500)
                    fecha = card.locator('.rsqaWe').inner_text(timeout=500)
                    rating_text = card.locator('.kvMYJc').get_attribute('aria-label', timeout=500)
                    rating = re.search(r'\d+', rating_text).group(0) if rating_text else "N/A"
                    
                    try:
                        more_button = card.locator('button:has-text("Más")')
                        if more_button.is_visible(): more_button.click(timeout=500)
                    except: pass
                    
                    texto_reseña_element = card.locator('.wiI7pd')
                    texto_reseña = texto_reseña_element.inner_text(timeout=500) if texto_reseña_element.is_visible() else ""

                    all_reviews_data.append({
                        "sucursal": sucursal['nombre'], "autor_nombre": autor_nombre,
                        "fecha": fecha, "rating": int(rating) if rating.isdigit() else 0,
                        "texto_reseña": texto_reseña
                    })
                except Exception: continue 

            print(f"✅ Datos de {sucursal['nombre']} extraídos correctamente.")
        except Exception as e:
            print(f"❌ ERROR GRAVE procesando {sucursal['nombre']}: {e}")
            print("Saltando a la siguiente sucursal...")
        
        browser.close()

print("\n🎉 ¡Scraping completado!")

if all_reviews_data:
    print(f"Exportando un total de {len(all_reviews_data)} reseñas a CSV...")
    df = pd.DataFrame(all_reviews_data)
    df.to_csv("pertutti_reviews.csv", index=False, encoding='utf-8-sig')
    print("✅ Archivo 'pertutti_reviews.csv' guardado.")
else:
    print("No se encontraron datos para exportar.")