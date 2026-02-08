# interfaz.py
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import threading
from scraping import obtener_precio_combustible, obtener_precio_aceite, obtener_precio_frenos, obtener_precio_lubricante, obtener_precio_transmision, cerrar_driver
from calculos import calcular_costos

class CalculadoraViajeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de Costos de Viaje en Moto")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Variables
        self.calculando = False
        
        # Crear widgets
        self.crear_widgets()
    
    def crear_widgets(self):
        # Frame principal
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        titulo = tk.Label(main_frame, text="Calculadora de Costos de Viaje", 
                         font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Kilómetros
        tk.Label(main_frame, text="Kilómetros a recorrer:", 
                font=("Arial", 11)).grid(row=1, column=0, sticky="w", pady=10)
        self.entry_kilometros = tk.Entry(main_frame, width=20, font=("Arial", 11))
        self.entry_kilometros.grid(row=1, column=1, pady=10, padx=10)
        
        # Peajes
        tk.Label(main_frame, text="Costo total de peajes ($):", 
                font=("Arial", 11)).grid(row=2, column=0, sticky="w", pady=10)
        self.entry_peajes = tk.Entry(main_frame, width=20, font=("Arial", 11))
        self.entry_peajes.grid(row=2, column=1, pady=10, padx=10)
        
        # Separador
        ttk.Separator(main_frame, orient='horizontal').grid(row=3, column=0, columnspan=2, 
                                                            sticky="ew", pady=20)
        
        # Botón calcular
        self.boton_calcular = tk.Button(main_frame, text="Calcular Costos", 
                                       command=self.iniciar_calculo,
                                       font=("Arial", 12, "bold"),
                                       bg="#4CAF50", fg="white",
                                       padx=20, pady=10,
                                       cursor="hand2")
        self.boton_calcular.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(main_frame, length=400, mode='indeterminate')
        self.progress.grid(row=5, column=0, columnspan=2, pady=10)
        
        # Label de estado
        self.label_estado = tk.Label(main_frame, text="", 
                                     font=("Arial", 10), fg="blue")
        self.label_estado.grid(row=6, column=0, columnspan=2, pady=5)
        
        # Área de texto para resultados
        resultado_frame = tk.Frame(main_frame)
        resultado_frame.grid(row=7, column=0, columnspan=2, pady=10, sticky="ew")
        
        tk.Label(resultado_frame, text="Resultados:", 
                font=("Arial", 11, "bold")).pack(anchor="w")
        
        self.text_resultado = tk.Text(resultado_frame, height=10, width=60, 
                                      font=("Courier", 9), state=tk.DISABLED)
        self.text_resultado.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar para el área de texto
        scrollbar = tk.Scrollbar(resultado_frame, command=self.text_resultado.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_resultado.config(yscrollcommand=scrollbar.set)
    
    def iniciar_calculo(self):
        """Inicia el cálculo en un hilo separado para no bloquear la GUI."""
        if self.calculando:
            messagebox.showwarning("Advertencia", "Ya hay un cálculo en proceso.")
            return
        
        # Validar entradas
        try:
            kilometros = float(self.entry_kilometros.get())
            peajes = float(self.entry_peajes.get())
            
            if kilometros <= 0:
                messagebox.showerror("Error", "Los kilómetros deben ser mayores a 0.")
                return
            if peajes < 0:
                messagebox.showerror("Error", "El costo de peajes no puede ser negativo.")
                return
                
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores numéricos válidos.")
            return
        
        # Iniciar cálculo en hilo separado
        self.calculando = True
        self.boton_calcular.config(state=tk.DISABLED)
        self.progress.start()
        self.label_estado.config(text="Obteniendo precios actualizados...")
        
        thread = threading.Thread(target=self.realizar_calculo, args=(kilometros, peajes))
        thread.daemon = True
        thread.start()
    
    def realizar_calculo(self, kilometros, peajes):
        """Realiza el cálculo de costos."""
        try:
            # URLs de los precios
            url_combustible = 'https://surtidores.com.ar/precios/'
            url_aceite = 'https://www.mercadolibre.com.ar/aceite-castrol-power-1-4t-15w-50-moto-lub-semisintetico-1-l/p/MLA19726323'
            url_frenos = 'https://www.mercadolibre.com.ar/liquido-para-frenos-tipo-4-1-litro-wagner-lockheed-67262/p/MLA26074783'
            url_lubricante = 'https://articulo.mercadolibre.com.ar/MLA-875201333-lucricante-cadena-ipone-x-trem-chain-road-750-ml-fas-motos-_JM'
            url_transmision = 'https://www.mercadolibre.com.ar/kit-de-transmision-mondial-hd-150-motos-franco/up/MLAU236584766'
            
            # Obtener precios
            self.actualizar_estado("Obteniendo precio del combustible...")
            precio_combustible = obtener_precio_combustible(url_combustible)
            
            self.actualizar_estado("Obteniendo precio del aceite...")
            precio_aceite = obtener_precio_aceite(url_aceite)
            
            self.actualizar_estado("Obteniendo precio del líquido de frenos...")
            precio_frenos = obtener_precio_frenos(url_frenos)
            
            self.actualizar_estado("Obteniendo precio del lubricante...")
            precio_lubricante = obtener_precio_lubricante(url_lubricante)
            
            self.actualizar_estado("Obteniendo precio de la transmisión...")
            precio_transmision = obtener_precio_transmision(url_transmision)
            
            self.actualizar_estado("Calculando costos del viaje...")
            
            # Capturar la salida de calcular_costos
            import io
            import sys
            
            old_stdout = sys.stdout
            sys.stdout = buffer = io.StringIO()
            
            costo_total = calcular_costos(kilometros, peajes, precio_combustible, 
                                         precio_aceite, precio_frenos, 
                                         precio_lubricante, precio_transmision)
            
            output = buffer.getvalue()
            sys.stdout = old_stdout
            
            # Mostrar resultados en la GUI
            self.root.after(0, self.mostrar_resultados, output, costo_total)
            
        except Exception as e:
            self.root.after(0, self.mostrar_error, str(e))
        finally:
            # IMPORTANTE: Cerrar Selenium al finalizar
            try:
                cerrar_driver()
            except Exception as e:
                print(f"Error al cerrar Selenium: {e}")
            
            self.root.after(0, self.finalizar_calculo)
    
    def actualizar_estado(self, mensaje):
        """Actualiza el label de estado desde un hilo."""
        self.root.after(0, lambda: self.label_estado.config(text=mensaje))
    
    def mostrar_resultados(self, output, costo_total):
        """Muestra los resultados en el área de texto."""
        self.text_resultado.config(state=tk.NORMAL)
        self.text_resultado.delete(1.0, tk.END)
        self.text_resultado.insert(tk.END, output)
        self.text_resultado.config(state=tk.DISABLED)
        self.label_estado.config(text=f"Cálculo completado. Costo total: ${costo_total:,.2f}", 
                                fg="green")
        messagebox.showinfo("Éxito", f"Cálculo completado.\n\nCosto total: ${costo_total:,.2f}")
    
    def mostrar_error(self, mensaje):
        """Muestra un mensaje de error."""
        self.label_estado.config(text="Error en el cálculo", fg="red")
        messagebox.showerror("Error", f"Ocurrió un error:\n{mensaje}")
    
    def finalizar_calculo(self):
        """Finaliza el proceso de cálculo."""
        self.progress.stop()
        self.boton_calcular.config(state=tk.NORMAL)
        self.calculando = False

def iniciar_interfaz():
    """Función para iniciar la interfaz gráfica."""
    root = tk.Tk()
    app = CalculadoraViajeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    iniciar_interfaz()
