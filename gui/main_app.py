import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import customtkinter as ctk
import threading
from datetime import datetime
import matplotlib.pyplot as plt
# Añade estos imports en la parte superior del archivo
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

from algorithm.utils.custom_data_manager import CustomDataManager
from algorithm import ComputerGenerator
from models import UserPreferences

# Módulos visuales
from gui.styles import setup_style, update_colors
from gui.menu import create_menu

# Pestañas
from gui.tabs.generator_tab import setup_generator_tab
from gui.tabs.results_tab import setup_results_tab
from gui.tabs.comparison_tab import setup_comparison_tab
from gui.tabs.visualization_tab import setup_visualization_tab
from gui.tabs.component_browser_tab import setup_component_browser_tab

class ComputerGeneratorGUI:
    def __init__(self, master):
        self.master = master
        self.data_manager = CustomDataManager()

        # Inicialización de variables que necesitamos antes de crear los widgets
        # Variables para la pestaña del generador
        self.usage_var = tk.StringVar(value="gaming")
        self.price_min_var = tk.StringVar(value="8000")
        self.price_max_var = tk.StringVar(value="15000")
        self.priority_var = tk.StringVar(value="balanced")
        self.form_factor_var = tk.StringVar(value="ATX")
        self.future_proof_var = tk.BooleanVar(value=False)
        self.population_var = tk.IntVar(value=30)
        self.generations_var = tk.IntVar(value=50)
        self.crossover_var = tk.DoubleVar(value=0.7)
        self.mutation_var = tk.DoubleVar(value=0.1)
        self.rgb_lighting_var = tk.BooleanVar(value=False)
        self.case_color_var = tk.StringVar(value="Black")
        self.progress_var = tk.DoubleVar(value=0)
        
        # Variables para preferencias
        self.brand_preferences = {}
        self.must_include = {}
        self.must_exclude = {}
        
        # Variables para fitness weights
        self.fitness_weights = {
            'price_range': 20,
            'compatibility': 25,
            'usage_match': 30,
            'power_balance': 5,
            'bottleneck': 10,
            'value_cpu': 5,
            'value_gpu': 5,
        }
        
        # Estado de optimización
        self.optimization_running = False
        self.current_computer = None
        self.generated_computers = []
        self.result_history = []

        # Estilo y tema
        setup_style(self)

        # Ventana principal
        self.setup_main_window()

        # Crear pestañas
        self.setup_tabs()

        # Cargar configuración
        self.load_application_settings()

        # Confirmación
        print("✅ Interfaz cargada correctamente")
        self.status_bar.config(text="Interfaz cargada correctamente")

    def setup_main_window(self):
        """Configura la ventana principal y el layout base"""
        self.master.title("Computer Generator Pro")
        self.master.geometry("1200x800")
        self.master.minsize(1000, 700)
        self.master.grid_columnconfigure(0, weight=1)
        self.master.grid_rowconfigure(0, weight=1)

        # Crear menú
        create_menu(self)

        # Barra de estado
        self.status_bar = ttk.Label(self.master, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.grid(row=1, column=0, sticky="ew")

    def setup_tabs(self):
        """Inicializa las pestañas"""
        self.notebook = ttk.Notebook(self.master)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # Agregar pestañas desde módulos
        setup_generator_tab(self)
        setup_results_tab(self)
        setup_comparison_tab(self)
        setup_visualization_tab(self)
        setup_component_browser_tab(self)

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)

    def on_tab_change(self, event):
        """Evento al cambiar de pestaña"""
        # Obtener pestaña seleccionada
        tab_id = self.notebook.select()
        tab_name = self.notebook.tab(tab_id, "text").strip()
        
        # Actualizar barra de estado
        self.status_bar.config(text=f"Vista actual: {tab_name}")
        
        # Actualizar UI según la pestaña seleccionada
        if tab_name == " Results " and hasattr(self, 'current_computer'):
            self.update_results_text()
            if hasattr(self, 'components_tree'):
                self.update_components_tree()

    def load_application_settings(self):
        """Carga configuraciones si es necesario"""
        pass

    def change_theme(self, mode):
        """Cambia el tema (claro/oscuro/sistema)"""
        ctk.set_appearance_mode(mode)
        update_colors(self)

    # Métodos de navegación y menú
    def new_configuration(self):
        """Inicia una nueva configuración"""
        # Confirmar si hay una configuración existente
        if hasattr(self, 'current_computer'):
            confirm = messagebox.askyesno("Confirmar nueva configuración", 
                                         "Esto borrará la configuración actual. ¿Continuar?")
            if not confirm:
                return
        
        # Restablecer formulario
        self.reset_form()
        
        # Borrar computadora actual
        if hasattr(self, 'current_computer'):
            delattr(self, 'current_computer')
        
        # Limpiar resultados si existe el widget
        if hasattr(self, 'results_text'):
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Genera una computadora para ver resultados aquí...")
            self.results_text.config(state=tk.DISABLED)
        
        # Limpiar árbol de componentes si existe
        if hasattr(self, 'components_tree'):
            for item in self.components_tree.get_children():
                self.components_tree.delete(item)
        
        # Actualizar estado
        self.status_bar.config(text="Nueva configuración iniciada")

    def open_configuration(self):
        """Abrir una configuración guardada"""
        print("Abrir configuración (por implementar)")
        self.status_bar.config(text="Abrir configuración (no implementado)")

    def save_configuration(self):
        """Guardar la configuración actual"""
        if not hasattr(self, 'current_computer'):
            messagebox.showinfo("Sin configuración", "No hay ninguna configuración para guardar.")
            return
        
        print("Guardar configuración (por implementar)")
        self.status_bar.config(text="Guardar configuración (no implementado)")

    def export_results(self):
        """Exportar los resultados actuales"""
        if not hasattr(self, 'current_computer'):
            messagebox.showinfo("Sin configuración", "No hay resultados para exportar.")
            return
        
        print("Exportar resultados (por implementar)")
        self.status_bar.config(text="Exportar resultados (no implementado)")

    def show_preferences(self):
        """Mostrar diálogo de preferencias"""
        print("Mostrar preferencias (por implementar)")
        self.status_bar.config(text="Preferencias (no implementado)")

    def show_documentation(self):
        """Mostrar documentación"""
        print("Abrir documentación (por implementar)")
        self.status_bar.config(text="Documentación (no implementado)")

    def show_about(self):
        """Mostrar diálogo Acerca de"""
        messagebox.showinfo("Acerca de", "Computer Generator Pro\nDesarrollado con ♥")

    def reset_form(self):
        """Restablecer todos los campos del formulario a sus valores predeterminados"""
        # Si los widgets existen, restablecer sus valores
        if hasattr(self, 'usage_var'):
            self.usage_var.set('gaming')
        
        if hasattr(self, 'price_min_var') and hasattr(self, 'price_max_var'):
            self.price_min_var.set('8000')
            self.price_max_var.set('15000')
        
        if hasattr(self, 'population_var'):
            self.population_var.set(30)
        
        if hasattr(self, 'generations_var'):
            self.generations_var.set(50)
        
        if hasattr(self, 'crossover_var'):
            self.crossover_var.set(0.7)
        
        if hasattr(self, 'mutation_var'):
            self.mutation_var.set(0.1)
            
        # Restablecer preferencias de marca
        self.brand_preferences = {}
        
        # Restablecer inclusiones/exclusiones
        self.must_include = {}
        self.must_exclude = {}
        
        # Actualizar estado
        self.status_bar.config(text="Formulario restablecido a valores predeterminados")
# Actualizar el método generate_computers en gui/main_app.py

    def generate_computers(self):
        """Inicia el proceso de generación de configuraciones de computadora"""
        try:
            # Validar entradas
            min_price = int(self.price_min_var.get())
            max_price = int(self.price_max_var.get())
            population_size = int(self.population_var.get())
            generations = int(self.generations_var.get())
            crossover_rate = float(self.crossover_var.get())
            mutation_rate = float(self.mutation_var.get())
            
            # Mapeo de uso (inglés a español para el algoritmo)
            usage_mapping = {
                'gaming': 'juegos',
                'office': 'ofimática',
                'graphics': 'diseño gráfico',
                'video': 'edición de video',
                'web': 'navegación web',
                'education': 'educación',
                'architecture': 'arquitectura'
            }
            
            usage = usage_mapping.get(self.usage_var.get(), 'juegos')
            
            # Obtener la aplicación objetivo seleccionada
            application_name = self.application_var.get()
            target_application = None
            
            if hasattr(self, 'app_name_to_id') and application_name in self.app_name_to_id:
                target_application = self.app_name_to_id[application_name]
            
            # Crear preferencias de usuario
            user_prefs = UserPreferences(
                min_price=min_price,
                max_price=max_price,
                usage=usage,
                priority=self.priority_var.get(),
                brand_preferences=self.brand_preferences,
                form_factor=self.form_factor_var.get(),
                aesthetic={"rgb": self.rgb_lighting_var.get(), "color": self.case_color_var.get()},
                must_include=self.must_include,
                must_exclude=self.must_exclude,
                future_proof=self.future_proof_var.get(),
                target_application=target_application,
                application_category=usage
            )
            
            # Actualizar estado de la UI
            self.generate_button.configure(state="disabled")
            self.stop_button.configure(state="normal")
            
            # Mostrar barra de progreso - USANDO GRID en lugar de PACK
            self.progress_bar.grid()  # Esto usará la configuración grid existente
            self.progress_var.set(0)
            self.status_bar.config(text="Generando configuración de computadora...")
            
            # Crear y ejecutar el generador en un hilo separado
            self.generator = ComputerGenerator(
                population_size=population_size,
                crossover_rate=crossover_rate,
                mutation_rate=mutation_rate,
                generations=generations,
                user_preferences=user_prefs,
                elitism_percentage=0.1,  # Valor por defecto
                tournament_size=3,       # Valor por defecto
                adaptive_mutation=True   # Valor por defecto
            )
            
            # Marcar que la optimización está en ejecución
            self.optimization_running = True
            
            # Iniciar el hilo de generación
            self.generation_thread = threading.Thread(target=self.run_generation)
            self.generation_thread.daemon = True
            self.generation_thread.start()
            
            # Iniciar actualización de progreso
            self.master.after(100, self.update_progress)
            
        except ValueError as e:
            messagebox.showerror("Error de entrada", f"Entrada inválida: {str(e)}")
            self.status_bar.config(text="Error en la generación")
            
    def run_generation(self):
        """Ejecuta el algoritmo genético en un hilo separado"""
        try:
            # Ejecutar el generador y obtener la mejor computadora
            self.current_computer, self.stats = self.generator.run()
            
            # Agregar al historial
            self.result_history.append({
                "computer": self.current_computer,
                "stats": self.stats,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "preferences": self.generator.user_preferences
            })
            
            # Actualizar la UI en el hilo principal
            self.master.after(0, self.update_results_ui)
        
        except Exception as e:
            # Manejar errores
            self.master.after(0, lambda: messagebox.showerror("Error de generación", f"Error durante la generación: {str(e)}"))
            self.master.after(0, self.reset_ui_after_generation)

    def update_progress(self):
        """Actualiza la barra de progreso durante la generación"""
        if not hasattr(self, 'generator') or not self.optimization_running:
            return
        
        # Calcular progreso
        if hasattr(self.generator, 'stats_tracker') and hasattr(self.generator.stats_tracker, 'best_cases'):
            best_cases = self.generator.stats_tracker.best_cases
            progress = min(100, len(best_cases) / self.generator.generations * 100)
            self.progress_var.set(progress)
            
            # Actualizar texto de estado
            if len(best_cases) > 0:
                best_fitness = best_cases[-1].fitness
                self.status_bar.config(text=f"Generación {len(best_cases)}/{self.generator.generations} - Mejor fitness: {best_fitness:.2f}")
        
        # Continuar actualizando si todavía está en ejecución
        if self.optimization_running:
            self.master.after(100, self.update_progress)

    def update_results_ui(self):
        """Actualiza la UI con los resultados de la generación"""
        if not hasattr(self, 'current_computer'):
            return
        
        # Actualizar texto de resultados
        self.update_results_text()
        
        # Actualizar árbol de componentes si existe
        if hasattr(self, 'components_tree'):
            self.update_components_tree()
        
        # Actualizar barras de rendimiento si existen
        if hasattr(self, 'performance_vars'):
            self.update_performance_display()
        
        # Restablecer estado de la UI
        self.reset_ui_after_generation()
        
        # Mostrar mensaje de éxito
        messagebox.showinfo("Generación completa", "¡Configuración de computadora generada exitosamente!")
        
        # Cambiar a la pestaña de resultados
        self.notebook.select(1)  # Índice de la pestaña Resultados

    def update_results_text(self):
        """Actualiza el texto de resultados con los detalles de la computadora"""
        if not hasattr(self, 'current_computer') or not hasattr(self, 'results_text'):
            return
        
        # Habilitar edición
        self.results_text.config(state=tk.NORMAL)
        
        # Limpiar texto existente
        self.results_text.delete(1.0, tk.END)
        
        # Agregar detalles de la computadora
        self.results_text.insert(tk.END, str(self.current_computer))
        
        # Agregar estadísticas adicionales
        self.results_text.insert(tk.END, "\n\nEstadísticas de generación:\n")
        self.results_text.insert(tk.END, f"Tiempo de ejecución: {self.stats['execution_time']:.2f} segundos\n")
        self.results_text.insert(tk.END, f"Generaciones completadas: {self.stats['generations_completed']}\n")
        self.results_text.insert(tk.END, f"Tamaño final de población: {self.stats['final_population_size']}\n")
        self.results_text.insert(tk.END, f"Diversidad final: {self.stats['final_diversity']:.2f}\n")
        
        # Deshabilitar edición
        self.results_text.config(state=tk.DISABLED)

    def update_components_tree(self):
        """Actualiza el árbol de componentes con la configuración actual"""
        if not hasattr(self, 'current_computer') or not hasattr(self, 'components_tree'):
            return
        
        # Limpiar elementos existentes
        for item in self.components_tree.get_children():
            self.components_tree.delete(item)
        
        # Agregar componentes al árbol
        self.components_tree.insert('', 'end', values=('CPU', str(self.current_computer.cpu), f"${self.current_computer.cpu.price:.2f}"))
        
        if self.current_computer.gpu:
            self.components_tree.insert('', 'end', values=('GPU', str(self.current_computer.gpu), f"${self.current_computer.gpu.price:.2f}"))
        else:
            self.components_tree.insert('', 'end', values=('GPU', 'Ninguno (Usando Gráficos Integrados)', '$0.00'))
        
        self.components_tree.insert('', 'end', values=('RAM', str(self.current_computer.ram), f"${self.current_computer.ram.price:.2f}"))
        self.components_tree.insert('', 'end', values=('Almacenamiento', str(self.current_computer.storage), f"${self.current_computer.storage.price:.2f}"))
        
        # Agregar almacenamientos adicionales si hay alguno
        for i, storage in enumerate(self.current_computer.additional_storages):
            self.components_tree.insert('', 'end', values=(f'Almacenamiento {i+2}', str(storage), f"${storage.price:.2f}"))
        
        self.components_tree.insert('', 'end', values=('Placa Base', str(self.current_computer.motherboard), f"${self.current_computer.motherboard.price:.2f}"))
        self.components_tree.insert('', 'end', values=('Fuente de Alimentación', str(self.current_computer.psu), f"${self.current_computer.psu.price:.2f}"))
        self.components_tree.insert('', 'end', values=('Refrigeración', str(self.current_computer.cooling), f"${self.current_computer.cooling.price:.2f}"))
        self.components_tree.insert('', 'end', values=('Gabinete', str(self.current_computer.case), f"${self.current_computer.case.price:.2f}"))
        
        # Agregar precio total
        self.components_tree.insert('', 'end', values=('Total', '', f"${self.current_computer.price:.2f}"))

    def update_performance_display(self):
        """Actualiza las barras de rendimiento"""
        if not hasattr(self, 'current_computer') or not hasattr(self, 'performance_vars'):
            return
        
        # Obtener métricas de rendimiento
        performance = self.current_computer.estimated_performance
        
        # Actualizar barras de progreso y etiquetas
        for metric in ['gaming', 'productivity', 'content_creation', 'development']:
            if metric in performance and metric in self.performance_vars:
                # Actualizar barra de progreso
                self.performance_vars[metric].set(performance[metric])
                
                # Actualizar etiqueta
                if f"{metric}_label" in self.performance_vars:
                    self.performance_vars[f"{metric}_label"].config(text=f"{performance[metric]:.1f}/100")
            else:
                # Métrica no disponible, establecer a 0
                if metric in self.performance_vars:
                    self.performance_vars[metric].set(0)
                    
                if f"{metric}_label" in self.performance_vars:
                    self.performance_vars[f"{metric}_label"].config(text="N/A")

    def reset_ui_after_generation(self):
        """Restablece los elementos de la UI después de completar o detener la generación"""
        if hasattr(self, 'generate_button'):
            self.generate_button.configure(state="normal")
        
        if hasattr(self, 'stop_button'):
            self.stop_button.configure(state="disabled")
        
        if hasattr(self, 'progress_bar'):
            self.progress_bar.grid_remove()  # Usamos grid_remove en lugar de pack_forget
        
        self.optimization_running = False

    def stop_generation(self):
        """Detiene el proceso de generación en curso"""
        if self.optimization_running:
            self.optimization_running = False
            
            # Restablecer estado de la UI
            self.reset_ui_after_generation()
            
            # Actualizar estado
            self.status_bar.config(text="Generación detenida por el usuario")

    def clear_results(self):
        """Limpia los resultados de la generación"""
        # Limpiar computadora actual
        if hasattr(self, 'current_computer'):
            delattr(self, 'current_computer')
        
        # Limpiar texto de resultados
        if hasattr(self, 'results_text'):
            self.results_text.config(state=tk.NORMAL)
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(tk.END, "Genera una computadora para ver resultados aquí...")
            self.results_text.config(state=tk.DISABLED)
        
        # Limpiar árbol de componentes
        if hasattr(self, 'components_tree'):
            for item in self.components_tree.get_children():
                self.components_tree.delete(item)
        
        # Actualizar estado
        self.status_bar.config(text="Resultados limpiados")

    def add_to_comparison(self):
        """Añade la computadora actual a la comparación"""
        if not hasattr(self, 'current_computer'):
            messagebox.showinfo("Sin computadora", "Por favor genera una computadora primero.")
            return
            
        # Crear un nombre para esta configuración
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        config_name = f"Config {len(self.generated_computers) + 1} ({timestamp})"
        
        # Añadir a la lista de computadoras generadas
        self.generated_computers.append({
            "name": config_name,
            "computer": self.current_computer,
            "stats": getattr(self, 'stats', {})
        })
        
        # Actualizar pestaña de comparación
        self.update_comparison_tab()
        
        # Cambiar a la pestaña de comparación
        self.notebook.select(2)  # Índice de la pestaña Comparison
        
        # Mostrar confirmación
        messagebox.showinfo("Añadido a comparación", 
                        f"Configuración '{config_name}' ha sido añadida a la comparación.")

    def update_comparison_tab(self):
        """Actualiza la pestaña de comparación con todas las computadoras generadas"""
        # Limpiar contenido existente
        for widget in self.comparison_container.winfo_children():
            widget.destroy()
            
        # Si no hay computadoras para comparar, mostrar mensaje
        if not self.generated_computers:
            ttk.Label(self.comparison_container, text="Agrega configuraciones para compararlas lado a lado...").pack(padx=20, pady=20)
            return
            
        # Crear tabla de comparación
        table_frame = ttk.Frame(self.comparison_container)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear encabezados
        ttk.Label(table_frame, text="Componente", font=("TkDefaultFont", 10, "bold")).grid(row=0, column=0, sticky="w", padx=5, pady=5)
        
        # Añadir nombres de computadoras como encabezados de columnas
        for i, config in enumerate(self.generated_computers):
            ttk.Label(table_frame, text=config["name"], font=("TkDefaultFont", 10, "bold")).grid(row=0, column=i+1, sticky="w", padx=5, pady=5)
            
            # Añadir botón de eliminar
            remove_button = ttk.Button(table_frame, text="X", width=2,
                                    command=lambda idx=i: self.remove_from_comparison(idx))
            remove_button.grid(row=0, column=i+1, sticky="e", padx=5, pady=5)
        
        # Añadir filas de componentes
        component_types = [
            "CPU", "GPU", "RAM", "Storage", "Motherboard", 
            "PSU", "Cooling", "Case", "Price", "Performance"
        ]
        
        for row, comp_type in enumerate(component_types):
            # Añadir encabezado de fila
            ttk.Label(table_frame, text=comp_type).grid(row=row+1, column=0, sticky="w", padx=5, pady=5)
            
            # Añadir detalles de componentes para cada configuración
            for col, config in enumerate(self.generated_computers):
                computer = config["computer"]
                
                # Obtener detalles del componente según el tipo
                if comp_type == "CPU":
                    value = str(computer.cpu)
                elif comp_type == "GPU":
                    value = str(computer.gpu) if computer.gpu else "Gráficos integrados"
                elif comp_type == "RAM":
                    value = str(computer.ram)
                elif comp_type == "Storage":
                    value = str(computer.storage)
                elif comp_type == "Motherboard":
                    value = str(computer.motherboard)
                elif comp_type == "PSU":
                    value = str(computer.psu)
                elif comp_type == "Cooling":
                    value = str(computer.cooling)
                elif comp_type == "Case":
                    value = str(computer.case)
                elif comp_type == "Price":
                    value = f"${computer.price:.2f}"
                elif comp_type == "Performance":
                    gaming = computer.estimated_performance.get('gaming', 0)
                    productivity = computer.estimated_performance.get('productivity', 0)
                    avg_perf = (gaming + productivity) / 2
                    value = f"Gaming: {gaming:.1f}, Prod: {productivity:.1f}, Avg: {avg_perf:.1f}"
                
                # Añadir a la tabla
                ttk.Label(table_frame, text=value, wraplength=200).grid(row=row+1, column=col+1, sticky="w", padx=5, pady=5)
        
        # Añadir gráfico de comparación de rendimiento
        self.add_comparison_chart()

    def add_comparison_chart(self):
        """Añade un gráfico que compara el rendimiento de todas las configuraciones"""
        if not self.generated_computers:
            return
            
        # Crear frame para el gráfico
        chart_frame = ttk.LabelFrame(self.comparison_container, text="Comparación de Rendimiento")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Crear figura para matplotlib
        figure = Figure(figsize=(10, 6), dpi=100)
        plot = figure.add_subplot(111)
        
        # Preparar datos
        config_names = []
        gaming_scores = []
        productivity_scores = []
        content_creation_scores = []
        development_scores = []
        
        for config in self.generated_computers:
            computer = config["computer"]
            config_names.append(config["name"])
            gaming_scores.append(computer.estimated_performance.get('gaming', 0))
            productivity_scores.append(computer.estimated_performance.get('productivity', 0))
            content_creation_scores.append(computer.estimated_performance.get('content_creation', 0))
            development_scores.append(computer.estimated_performance.get('development', 0))
        
        # Configurar posiciones para las barras
        x = np.arange(len(config_names))
        width = 0.2
        
        # Crear barras
        plot.bar(x - 1.5*width, gaming_scores, width, label='Gaming')
        plot.bar(x - 0.5*width, productivity_scores, width, label='Productividad')
        plot.bar(x + 0.5*width, content_creation_scores, width, label='Creación contenido')
        plot.bar(x + 1.5*width, development_scores, width, label='Desarrollo')
        
        # Añadir etiquetas y leyenda
        plot.set_xlabel('Configuración')
        plot.set_ylabel('Puntuación de rendimiento')
        plot.set_title('Comparación de rendimiento')
        plot.set_xticks(x)
        plot.set_xticklabels(config_names, rotation=45, ha='right')
        plot.legend()
        plot.grid(True, axis='y', linestyle='--', alpha=0.7)
        
        # Ajustar layout
        figure.tight_layout()
        
        # Crear canvas para la figura matplotlib
        canvas = FigureCanvasTkAgg(figure, chart_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def remove_from_comparison(self, index):
        """Elimina una configuración de la comparación"""
        if 0 <= index < len(self.generated_computers):
            # Obtener nombre de la configuración para el mensaje
            config_name = self.generated_computers[index]["name"]
            
            # Eliminar de la lista
            self.generated_computers.pop(index)
            
            # Actualizar pestaña de comparación
            self.update_comparison_tab()
            
            # Mostrar confirmación
            self.status_bar.config(text=f"Se eliminó '{config_name}' de la comparación")

    def clear_comparison(self):
        """Limpia todas las configuraciones de la comparación"""
        if not self.generated_computers:
            return
            
        # Confirmar limpieza
        confirm = messagebox.askyesno("Confirmar limpieza", 
                                    "¿Está seguro de que quiere eliminar todas las configuraciones de la comparación?")
        
        if confirm:
            # Limpiar la lista
            self.generated_computers = []
            
            # Actualizar pestaña de comparación
            self.update_comparison_tab()
            
            # Mostrar confirmación
            self.status_bar.config(text="Se eliminaron todas las configuraciones de la comparación")

    def export_comparison(self):
        """Exporta la comparación a un archivo"""
        if not self.generated_computers:
            messagebox.showinfo("Sin configuraciones", "No hay configuraciones para exportar.")
            return
            
        # Mostrar mensaje de que esta función será implementada
        messagebox.showinfo("Exportar", "Esta función será implementada próximamente.")
        self.status_bar.config(text="Exportar comparación (próximamente)")
    def on_usage_changed(self):
        """Manejar cambio en la selección de uso"""
        usage = self.usage_var.get()
        # Actualizar rango de precio en base al uso
        price_ranges = {
            'gaming': (10000, 30000),
            'office': (8000, 15000),
            'graphics': (15000, 40000),
            'video': (20000, 50000),
            'web': (5000, 10000),
            'education': (8000, 20000),
            'architecture': (20000, 50000)
        }
        
        if usage in price_ranges:
            min_price, max_price = price_ranges[usage]
            self.price_min_var.set(str(min_price))
            self.price_max_var.set(str(max_price))

    def toggle_advanced_options(self):
        """Mostrar u ocultar opciones avanzadas"""
        if self.advanced_options_var.get():
            self.advanced_frame.grid()  # Mostrar
        else:
            self.advanced_frame.grid_remove()  # Ocultar