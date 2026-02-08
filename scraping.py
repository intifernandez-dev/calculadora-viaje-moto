# scraping.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from base_de_datos import guardar_precio_en_bd, obtener_precio_bd
from funciones import convertir_a_float
import time

# Headers para requests (solo combustible)
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "es-AR,es;q=0.9",  
    "Accept-Encoding": "gzip, deflate, br",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}

# Variable global para reutilizar el driver de Selenium
_driver = None

def obtener_driver():
    """
    Crea o retorna el driver de Selenium (reutilizable).
    Configurado en modo headless con anti-detección mejorada.
    """
    global _driver
    if _driver is None:
        try:
            print("  [SELENIUM] Iniciando navegador Chrome...")
            chrome_options = Options()
            
            # Configuración headless mejorada
            chrome_options.add_argument('--headless=new')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--start-maximized')
            
            # Anti-detección
            chrome_options.add_argument('--disable-blink-features=AutomationControlled')
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # User agent realista
            chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
            
            # Preferencias adicionales
            prefs = {
                "profile.managed_default_content_settings.images": 2,  # No cargar imágenes (más rápido)
            }
            chrome_options.add_experimental_option("prefs", prefs)
            
            _driver = webdriver.Chrome(options=chrome_options)
            
            # Ejecutar script anti-detección
            _driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
                'source': '''
                    Object.defineProperty(navigator, 'webdriver', {
                        get: () => undefined
                    });
                    Object.defineProperty(navigator, 'plugins', {
                        get: () => [1, 2, 3, 4, 5]
                    });
                    Object.defineProperty(navigator, 'languages', {
                        get: () => ['es-AR', 'es', 'en']
                    });
                '''
            })
            
            print("  [SELENIUM] Navegador iniciado correctamente")
        except WebDriverException as e:
            print(f"  [SELENIUM] ERROR: No se pudo iniciar Chrome. ¿Está instalado chromedriver?")
            print(f"  [SELENIUM] Detalles: {e}")
            raise
    return _driver

def cerrar_driver():
    """Cierra el driver de Selenium al finalizar."""
    global _driver
    if _driver:
        try:
            print("  [SELENIUM] Cerrando navegador...")
            _driver.quit()
            _driver = None
            print("  [SELENIUM] Navegador cerrado")
        except Exception as e:
            print(f"  [SELENIUM] Error al cerrar: {e}")
            _driver = None

def obtener_precio_mercadolibre_selenium(url, nombre_producto):
    """
    Obtiene el precio de un producto de MercadoLibre usando Selenium.
    Usa aria-hidden='true' como estrategia principal (la más confiable según tests).
    
    Args:
        url: URL del producto en MercadoLibre
        nombre_producto: Nombre para guardar en BD (ej: "Aceite")
    
    Returns:
        float: Precio obtenido o None si falla
    """
    try:
        driver = obtener_driver()
        print(f"  [SELENIUM] Cargando {url}...")
        driver.get(url)
        
        # Esperar que la página cargue completamente
        time.sleep(3)
        
        # ========================================================================
        # ESTRATEGIA PRINCIPAL: aria-hidden='true' ⭐
        # (Probada y funciona en todos los casos)
        # ========================================================================
        try:
            print(f"  [SELENIUM] Buscando precio con aria-hidden='true'...")
            
            precio_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    "span[class*='andes-money-amount__fraction'][aria-hidden='true']"
                ))
            )
            
            precio_texto = precio_elem.text.strip()
            print(f"  [SELENIUM] ✅ Precio encontrado: {precio_texto}")
            
            precio_float = convertir_a_float(precio_texto)
            
            if precio_float > 0:
                guardar_precio_en_bd(nombre_producto, precio_float)
                print(f"Precio de {nombre_producto} obtenido: ${precio_float:,.0f}")
                return precio_float
            else:
                print(f"  [SELENIUM] ⚠️ Precio inválido: {precio_float}")
                
        except Exception as e:
            print(f"  [SELENIUM] ⚠️ Estrategia principal falló: {str(e)[:100]}")
        
        # ========================================================================
        # ESTRATEGIA DE RESPALDO 1: Contenedor principal
        # ========================================================================
        try:
            print(f"  [SELENIUM] Intentando estrategia de respaldo (contenedor principal)...")
            
            contenedor_precio = driver.find_element(By.CSS_SELECTOR, "div.ui-pdp-price__main-container")
            precio_elem = contenedor_precio.find_element(By.CLASS_NAME, "andes-money-amount__fraction")
            precio_texto = precio_elem.text.strip()
            
            print(f"  [SELENIUM] ✅ Precio encontrado (respaldo): {precio_texto}")
            precio_float = convertir_a_float(precio_texto)
            
            if precio_float > 0:
                guardar_precio_en_bd(nombre_producto, precio_float)
                print(f"Precio de {nombre_producto} obtenido: ${precio_float:,.0f}")
                return precio_float
                
        except Exception as e:
            print(f"  [SELENIUM] ⚠️ Estrategia de respaldo 1 falló: {str(e)[:100]}")
        
        # ========================================================================
        # ESTRATEGIA DE RESPALDO 2: Precio máximo (más conservadora)
        # ========================================================================
        try:
            print(f"  [SELENIUM] Intentando última estrategia (precio máximo)...")
            
            precios_elements = driver.find_elements(By.CLASS_NAME, "andes-money-amount__fraction")
            
            precios_valores = []
            for elem in precios_elements:
                texto = elem.text.strip()
                valor = convertir_a_float(texto)
                if valor > 0:
                    precios_valores.append(valor)
            
            if precios_valores:
                precio_max = max(precios_valores)
                print(f"  [SELENIUM] ✅ Precio máximo encontrado: ${precio_max:,.0f}")
                
                guardar_precio_en_bd(nombre_producto, precio_max)
                print(f"Precio de {nombre_producto} obtenido: ${precio_max:,.0f}")
                return precio_max
                
        except Exception as e:
            print(f"  [SELENIUM] ⚠️ Estrategia de respaldo 2 falló: {str(e)[:100]}")
        
        # ========================================================================
        # Si todas las estrategias fallan
        # ========================================================================
        print(f"  [SELENIUM] ❌ No se pudo obtener el precio de {nombre_producto}")
        
        # Guardar HTML para debug
        try:
            with open(f'debug_{nombre_producto}.html', 'w', encoding='utf-8') as f:
                f.write(driver.page_source)
            print(f"  [DEBUG] HTML guardado en: debug_{nombre_producto}.html")
        except:
            pass
            
        return None
        
    except Exception as e:
        print(f"  [SELENIUM] ❌ Error general obteniendo precio: {e}")
        import traceback
        traceback.print_exc()
        return None

# ============================================================================
# FUNCIONES DE SCRAPING POR PRODUCTO
# ============================================================================

def obtener_precio_combustible(url):
    """Obtiene el precio del combustible desde la página web o la base de datos."""
    precio_bd = obtener_precio_bd("Combustible")
    if precio_bd:
        print(f"Precio de combustible obtenido de la base de datos: ${precio_bd:,.0f}")
        return precio_bd

    try:
        print("Obteniendo precio de combustible desde la web...")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            div_cuerpo = soup.find('div', class_='cuerpo-noticia py-3')
            
            if div_cuerpo:
                encabezado = div_cuerpo.find('h2', string=lambda text: text and 'tabla de precios' in text.lower())
                if encabezado:
                    tabla = encabezado.find_next('table')
                    if tabla:
                        filas = tabla.find_all('tr')
                        meses_fila = filas[0].find_all('td')
                        meses = [mes.text.strip().lower() for mes in meses_fila]
                        
                        mes_actual = datetime.now().strftime('%B').lower()
                        meses_esp = {
                            'january': 'enero', 'february': 'febrero', 'march': 'marzo',
                            'april': 'abril', 'may': 'mayo', 'june': 'junio',
                            'july': 'julio', 'august': 'agosto', 'september': 'septiembre',
                            'october': 'octubre', 'november': 'noviembre', 'december': 'diciembre'
                        }
                        mes_actual_esp = meses_esp.get(mes_actual, 'febrero')

                        if mes_actual_esp in meses:
                            indice_mes = meses.index(mes_actual_esp)
                            precios_fila = filas[1].find_all('td')
                            precio_super = precios_fila[indice_mes].text.strip()
                            precio_float = convertir_a_float(precio_super)
                            guardar_precio_en_bd("Combustible", precio_float)
                            print(f"Precio de combustible obtenido: ${precio_float:,.0f}")
                            return precio_float
        
        print("No se pudo obtener el precio del combustible. Usando valor por defecto.")
        return 1000.0
    except Exception as e:
        print(f"Error al obtener el precio del combustible: {e}")
        return 1000.0

def obtener_precio_aceite(url):
    """Obtiene el precio del aceite desde MercadoLibre o la base de datos."""
    precio_bd = obtener_precio_bd("Aceite")
    if precio_bd:
        print(f"Precio de aceite obtenido de la base de datos: ${precio_bd:,.0f}")
        return precio_bd

    print("Obteniendo precio de aceite desde la web...")
    precio = obtener_precio_mercadolibre_selenium(url, "Aceite")
    
    if precio:
        return precio
    else:
        print("No se pudo obtener el precio del aceite. Usando valor por defecto.")
        return 15000.0

def obtener_precio_frenos(url):
    """Obtiene el precio del líquido de frenos desde MercadoLibre o la base de datos."""
    precio_bd = obtener_precio_bd("Frenos")
    if precio_bd:
        print(f"Precio de líquido de frenos obtenido de la base de datos: ${precio_bd:,.0f}")
        return precio_bd

    print("Obteniendo precio de líquido de frenos desde la web...")
    precio = obtener_precio_mercadolibre_selenium(url, "Frenos")
    
    if precio:
        return precio
    else:
        print("No se pudo obtener el precio del líquido de frenos. Usando valor por defecto.")
        return 8000.0

def obtener_precio_lubricante(url):
    """Obtiene el precio del lubricante de cadena desde MercadoLibre o la base de datos."""
    precio_bd = obtener_precio_bd("Lubricante")
    if precio_bd:
        print(f"Precio de lubricante obtenido de la base de datos: ${precio_bd:,.0f}")
        return precio_bd

    print("Obteniendo precio de lubricante desde la web...")
    precio = obtener_precio_mercadolibre_selenium(url, "Lubricante")
    
    if precio:
        return precio
    else:
        print("No se pudo obtener el precio del lubricante. Usando valor por defecto.")
        return 12000.0

def obtener_precio_transmision(url):
    """Obtiene el precio del kit de transmisión desde MercadoLibre o la base de datos."""
    precio_bd = obtener_precio_bd("Transmision")
    if precio_bd:
        print(f"Precio de transmisión obtenido de la base de datos: ${precio_bd:,.0f}")
        return precio_bd

    print("Obteniendo precio de kit de transmisión desde la web...")
    precio = obtener_precio_mercadolibre_selenium(url, "Transmision")
    
    if precio:
        return precio
    else:
        print("No se pudo obtener el precio del kit de transmisión. Usando valor por defecto.")
        return 50000.0
