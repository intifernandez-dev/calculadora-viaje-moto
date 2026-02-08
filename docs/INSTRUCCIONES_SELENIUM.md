# INSTRUCCIONES DE INSTALACIÓN - SELENIUM

## 1. Instalar Selenium

Abre tu terminal o CMD y ejecuta:

```bash
pip install selenium
```

## 2. Instalar ChromeDriver

### Opción A: Instalación Automática (Recomendada)

```bash
pip install webdriver-manager
```

Si usas esta opción, modifica scraping.py línea 42:
```python
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Cambiar esta línea:
_driver = webdriver.Chrome(options=chrome_options)

# Por esta:
_driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
```

### Opción B: Instalación Manual

1. Verifica tu versión de Chrome:
   - Abre Chrome
   - Ve a chrome://settings/help
   - Anota la versión (ej: 120.0.6099.109)

2. Descarga ChromeDriver compatible:
   - https://googlechromelabs.github.io/chrome-for-testing/
   - Descarga la versión que coincida con tu Chrome

3. Extrae el ejecutable:
   - Windows: chromedriver.exe
   - Linux/Mac: chromedriver

4. Coloca chromedriver en tu PATH o en la carpeta del proyecto

## 3. Verificar Instalación

Ejecuta este script de prueba:

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

try:
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.google.com')
    print("✅ Selenium funciona correctamente!")
    driver.quit()
except Exception as e:
    print(f"❌ Error: {e}")
    print("\nPosibles soluciones:")
    print("1. Instala webdriver-manager: pip install webdriver-manager")
    print("2. Descarga chromedriver manualmente")
```

## 4. Reemplazar Archivos

Una vez instalado Selenium, reemplaza:
- scraping.py → scraping_selenium.py
- interfaz.py → interfaz_selenium.py

## 5. Ejecutar

```bash
python main.py
```

## Troubleshooting

### Error: "chromedriver not found"
- Instala webdriver-manager (Opción A)
- O descarga chromedriver manualmente (Opción B)

### Error: "session not created"
- La versión de ChromeDriver no coincide con tu Chrome
- Actualiza Chrome o descarga otra versión de ChromeDriver

### Error: "Chrome failed to start"
- En Linux: `sudo apt-get install chromium-browser chromium-chromedriver`
- Verifica que Chrome esté instalado

### El programa se cuelga
- Selenium tarda ~3-5 segundos por producto (es normal)
- La primera vez tarda más porque descarga ChromeDriver

## Rendimiento Esperado

- Combustible: ~1 segundo (requests)
- Aceite: ~3-5 segundos (Selenium)
- Frenos: ~2-3 segundos (reutiliza navegador)
- Lubricante: ~2-3 segundos (reutiliza navegador)
- Transmisión: ~2-3 segundos (reutiliza navegador)

**Total: ~12-17 segundos** para obtener todos los precios

## Ventajas de esta Solución

✅ Funciona con cualquier sitio que use JavaScript
✅ No depende de cambios en HTML de MercadoLibre
✅ Reutiliza el navegador (más rápido)
✅ Modo headless (no abre ventanas)
✅ Manejo de errores robusto

## Desventajas

❌ Requiere ChromeDriver instalado
❌ Más lento que requests puro
❌ Consume más recursos (RAM)
