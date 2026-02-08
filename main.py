# main.py
"""
Calculadora de Costos de Viaje en Moto
Calcula los costos de mantenimiento y combustible para un viaje en motocicleta.
"""

from base_de_datos import crear_base_de_datos
from interfaz import iniciar_interfaz

def main():
    """
    Función principal del programa.
    Crea la base de datos e inicia la interfaz gráfica.
    """
    print("="*60)
    print("CALCULADORA DE COSTOS DE VIAJE EN MOTO")
    print("="*60)
    print("\nIniciando aplicación...")
    
    # Crear la base de datos si no existe
    print("Verificando base de datos...")
    crear_base_de_datos()
    print("Base de datos lista.\n")
    
    # Iniciar la interfaz gráfica
    print("Iniciando interfaz gráfica...")
    iniciar_interfaz()

if __name__ == "__main__":
    main()
