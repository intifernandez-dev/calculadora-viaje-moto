# calculos.py
from funciones import convertir_a_float

def calcular_costos(kilometros, peajes, precio_combustible, precio_aceite, precio_frenos, precio_lubricante, precio_transmision):
    """
    Calcula los costos totales del viaje basado en los kilómetros y precios de productos.
    
    Parámetros de consumo:
    - Combustible: 4.5L por cada 100km
    - Aceite: 1L cada 3000km
    - Líquido de frenos: 0.2L cada 30000km
    - Lubricante de cadena: 0.01L cada 500km (el precio es por envase de 0.4L)
    - Kit de transmisión: 1 kit cada 25000km
    """
    try:
        # Convertir todos los precios a float
        precio_combustible = convertir_a_float(precio_combustible)
        precio_aceite = convertir_a_float(precio_aceite)
        precio_frenos = convertir_a_float(precio_frenos)
        precio_lubricante = convertir_a_float(precio_lubricante)
        precio_transmision = convertir_a_float(precio_transmision)

        # Calcular precio por litro del lubricante (viene en envase de 0.4L)
        precio_lubricante_por_litro = precio_lubricante / 0.4

        # Cálculos de consumo
        consumo_combustible = (kilometros / 100) * 4.5
        consumo_aceite = (kilometros / 3000) * 1
        consumo_frenos = (kilometros / 30000) * 0.2
        consumo_lubricante = (kilometros / 500) * 0.01
        kits_transmision = (kilometros / 25000) * 1

        # Cálculos de costos
        costo_combustible = consumo_combustible * precio_combustible
        costo_aceite = consumo_aceite * precio_aceite
        costo_frenos = consumo_frenos * precio_frenos
        costo_lubricante = consumo_lubricante * precio_lubricante_por_litro
        costo_transmision = kits_transmision * precio_transmision
        costo_peajes = peajes

        # Costo total
        costo_total = costo_combustible + costo_aceite + costo_frenos + costo_lubricante + costo_transmision + costo_peajes

        # Mostrar resultados
        print("\n" + "="*60)
        print("CALCULADORA DE COSTOS DE VIAJE EN MOTO")
        print("="*60)
        
        print("\n---- DATOS INGRESADOS ----")
        print(f"Kilómetros a recorrer: {kilometros:,.0f} km")
        print(f"Costo total de peajes: ${costo_peajes:,.2f}")
        print(f"Precio del combustible por litro: ${precio_combustible:,.2f}")
        print(f"Precio del aceite por litro: ${precio_aceite:,.2f}")
        print(f"Precio del líquido de frenos por litro: ${precio_frenos:,.2f}")
        print(f"Precio del lubricante de cadena por litro: ${precio_lubricante_por_litro:,.2f}")
        print(f"Precio del kit de transmisión: ${precio_transmision:,.2f}")
        
        print("\n---- CÁLCULOS DEL VIAJE ----")
        print(f"Distancia total: {kilometros:,.0f} km")
        print(f"Consumo de combustible: {consumo_combustible:.2f} L | Costo: ${costo_combustible:,.2f}")
        print(f"Consumo de aceite: {consumo_aceite:.4f} L | Costo: ${costo_aceite:,.2f}")
        print(f"Consumo de líquido de frenos: {consumo_frenos:.4f} L | Costo: ${costo_frenos:,.2f}")
        print(f"Consumo de lubricante de cadena: {consumo_lubricante:.4f} L | Costo: ${costo_lubricante:,.2f}")
        print(f"Cambio de transmisión: {kits_transmision:.4f} kits | Costo: ${costo_transmision:,.2f}")
        print(f"Costo total de peajes: ${costo_peajes:,.2f}")
        
        print("\n" + "="*60)
        print(f"COSTO TOTAL DEL VIAJE: ${costo_total:,.2f}")
        print("="*60 + "\n")
        
        return costo_total
        
    except Exception as e:
        print(f"Error en el cálculo: {e}")
        return 0
