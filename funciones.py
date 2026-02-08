# funciones.py
def convertir_a_float(valor):
    """
    Convierte un valor a float, manejando formato argentino.
    
    Formato argentino:
    - Separador de miles: punto (.)
    - Separador decimal: coma (,)
    
    Ejemplos:
    - "13.500" → 13500.0
    - "13.500,50" → 13500.5
    - "$ 13.500" → 13500.0
    - "$13500" → 13500.0
    """
    try:
        if isinstance(valor, str):
            # Limpiar caracteres especiales
            valor_limpio = valor.replace("$", "").replace(" ", "").strip()
            
            # Detectar si tiene coma (separador decimal argentino)
            if "," in valor_limpio:
                # Tiene decimales
                # Ejemplo: "13.500,50" → "13500.50"
                valor_limpio = valor_limpio.replace(".", "").replace(",", ".")
            else:
                # No tiene decimales, solo miles
                # Ejemplo: "13.500" → "13500"
                valor_limpio = valor_limpio.replace(".", "")
            
            return float(valor_limpio)
            
        elif isinstance(valor, (float, int)):
            return float(valor)
        else:
            return 0.0
    except ValueError:
        return 0.0
