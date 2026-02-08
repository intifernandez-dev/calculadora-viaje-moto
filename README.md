# 🏍️ Calculadora de Costos de Viaje en Moto

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.0%2B-green)](https://www.selenium.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Aplicación de escritorio con interfaz gráfica que calcula automáticamente los costos de un viaje en motocicleta en Argentina, obteniendo precios actualizados mediante web scraping.

![Demo](docs/demo.png)

## 📋 Características

- ✅ **Web Scraping Inteligente**: Obtiene precios reales de MercadoLibre y sitios de combustible
- ✅ **Cache de Precios**: Base de datos SQLite que guarda precios por 24 horas (optimiza velocidad)
- ✅ **Interfaz Gráfica Intuitiva**: Desarrollada con Tkinter
- ✅ **Cálculos Precisos**: Basados en consumos reales de motocicletas
- ✅ **Multi-threading**: No bloquea la interfaz durante el scraping
- ✅ **Manejo Robusto de Errores**: Valores por defecto si el scraping falla

## 🎯 ¿Qué Calcula?

La aplicación calcula el costo total del viaje considerando:

| Concepto | Consumo/Frecuencia |
|----------|-------------------|
| 🛢️ Combustible | 4.5L cada 100km |
| 🛢️ Aceite de motor | 1L cada 3,000km |
| 🔧 Líquido de frenos | 0.2L cada 30,000km |
| ⛓️ Lubricante de cadena | 0.01L cada 500km |
| ⚙️ Kit de transmisión | 1 kit cada 25,000km |
| 🛣️ Peajes | Monto ingresado por el usuario |

## 🚀 Instalación

### Prerrequisitos

- Python 3.7 o superior
- Google Chrome instalado
- Conexión a Internet

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/calculadora-moto.git
cd calculadora-moto
```

### Paso 2: Crear entorno virtual (recomendado)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar dependencias

```bash
pip install -r requirements.txt
```

### Paso 4: Instalar ChromeDriver (automático)

```bash
pip install webdriver-manager
```

El ChromeDriver se descargará automáticamente la primera vez que ejecutes la aplicación.

## 💻 Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Pasos en la interfaz

1. **Ingresa los kilómetros** que vas a recorrer
2. **Ingresa el costo de peajes** (opcional, puedes poner 0)
3. Haz clic en **"Calcular Costos"**
4. Espera mientras la app obtiene los precios actualizados (~15 segundos)
5. ¡Listo! Verás el desglose completo de costos

### Ejemplo de Salida

```
============================================================
CALCULADORA DE COSTOS DE VIAJE EN MOTO
============================================================
---- DATOS INGRESADOS ----
Kilómetros a recorrer: 500 km
Costo total de peajes: $2,000.00
Precio del combustible por litro: $1,560.00
Precio del aceite por litro: $14,258.00
...

---- CÁLCULOS DEL VIAJE ----
Distancia total: 500 km
Consumo de combustible: 22.50 L | Costo: $35,100.00
Consumo de aceite: 0.1667 L | Costo: $2,376.81
...

============================================================
COSTO TOTAL DEL VIAJE: $39,847.23
============================================================
```

## 🏗️ Arquitectura del Proyecto

```
calculadora-moto/
│
├── main.py                 # Punto de entrada de la aplicación
├── interfaz.py            # GUI con Tkinter y manejo de threads
├── scraping.py            # Web scraping con Selenium y Requests
├── calculos.py            # Lógica de cálculos de consumo
├── base_de_datos.py       # Gestión de SQLite para cache
├── funciones.py           # Utilidades (conversión de precios argentinos)
├── requirements.txt       # Dependencias del proyecto
├── README.md             # Este archivo
├── LICENSE               # Licencia MIT
└── docs/                 # Documentación adicional
    ├── INSTALACION.md
    └── CONTRIBUIR.md
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.x**: Lenguaje principal
- **Tkinter**: Interfaz gráfica nativa
- **Selenium WebDriver**: Web scraping dinámico (MercadoLibre)
- **BeautifulSoup4**: Parsing HTML (sitio de combustible)
- **SQLite3**: Base de datos para cache de precios
- **Threading**: Ejecución asíncrona para no bloquear UI

## 🔧 Configuración Avanzada

### Cambiar parámetros de consumo

Edita `calculos.py`:

```python
# Ejemplo: cambiar consumo de combustible a 5L/100km
consumo_combustible = (kilometros / 100) * 5.0
```

### Cambiar tiempo de cache

Edita `base_de_datos.py`:

```python
# Cambiar de 24 horas a 12 horas
if datetime.now() - fecha_actualizacion < timedelta(hours=12):
```

### Cambiar URLs de productos

Edita `interfaz.py` en la función `realizar_calculo()`:

```python
url_aceite = 'https://www.mercadolibre.com.ar/TU_PRODUCTO'
```

## 🐛 Solución de Problemas

### Error: "chromedriver not found"

```bash
pip install webdriver-manager
```

### Error: "Chrome failed to start"

- **Windows**: Instala Google Chrome
- **Linux**: `sudo apt-get install chromium-browser`

### Los precios son incorrectos

1. Borra la base de datos: `rm precios_viaje.db`
2. Ejecuta de nuevo: `python main.py`

### La interfaz no se abre

**Linux**:
```bash
sudo apt-get install python3-tk
```

## 📊 Rendimiento

- **Primera ejecución**: ~15-20 segundos (obtiene todos los precios)
- **Siguientes ejecuciones**: ~1 segundo (usa cache de 24 horas)
- **Consumo de RAM**: ~150MB durante scraping
- **Tamaño de base de datos**: <100KB

## 🤝 Contribuir

Las contribuciones son bienvenidas! Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/NuevaCaracteristica`)
3. Commit tus cambios (`git commit -m 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/NuevaCaracteristica`)
5. Abre un Pull Request

Ver [CONTRIBUIR.md](docs/CONTRIBUIR.md) para más detalles.

## 📝 Roadmap

- [ ] Agregar soporte para más sitios de precios
- [ ] Exportar resultados a PDF/Excel
- [ ] Versión móvil (Kivy/React Native)
- [ ] Comparativa de costos entre diferentes motos
- [ ] Gráficos de evolución de precios
- [ ] API REST para consultar precios


## 👨‍💻 Autor

**Inti Fernandez**

- GitHub: [@tu-usuario](https://github.com/intifernandez-dev)
- LinkedIn: [Tu Nombre](https://linkedin.com/in/tu-perfil)
- Email: intifernandez.dev@gmail.com

## 🙏 Agradecimientos

- [MercadoLibre](https://www.mercadolibre.com.ar/) - Fuente de precios de productos
- [Surtidores.com.ar](https://surtidores.com.ar/) - Fuente de precios de combustible
- Comunidad de Python Argentina

---

⭐ Si este proyecto te fue útil, considera darle una estrella en GitHub!
