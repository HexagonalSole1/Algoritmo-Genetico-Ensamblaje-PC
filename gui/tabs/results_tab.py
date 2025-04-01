# results_tab.py
from tkinter import ttk, scrolledtext
import tkinter as tk
import customtkinter as ctk

def setup_results_tab(gui):
    frame = ttk.Frame(gui.notebook)
    gui.notebook.add(frame, text=" Results ")
    
    # Configurar grid
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=3)
    frame.grid_rowconfigure(0, weight=1)
    
    # Crear paneles izquierdo y derecho
    left_pane = ttk.Frame(frame)
    left_pane.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    right_pane = ttk.Frame(frame)
    right_pane.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    
    # Panel izquierdo - Lista de componentes
    ttk.Label(left_pane, text="Componentes", font=("TkDefaultFont", 14, "bold")).pack(anchor="w", padx=10, pady=5)
    
    # Árbol de componentes
    columns = ('component', 'details', 'price')
    gui.components_tree = ttk.Treeview(left_pane, columns=columns, show='headings', height=20)
    
    # Definir encabezados y columnas
    gui.components_tree.heading('component', text='Componente')
    gui.components_tree.heading('details', text='Detalles')
    gui.components_tree.heading('price', text='Precio')
    
    gui.components_tree.column('component', width=120, anchor='w')
    gui.components_tree.column('details', width=300, anchor='w')
    gui.components_tree.column('price', width=80, anchor='e')
    
    # Añadir barra de desplazamiento
    scrollbar = ttk.Scrollbar(left_pane, orient=tk.VERTICAL, command=gui.components_tree.yview)
    gui.components_tree.configure(yscroll=scrollbar.set)
    
    # Empaquetar componentes
    gui.components_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=0, pady=5)
    
    # Panel derecho - Detalles del componente
    gui.details_frame = ttk.LabelFrame(right_pane, text="Detalles del componente")
    gui.details_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Área de texto para detalles del componente
    gui.results_text = scrolledtext.ScrolledText(gui.details_frame, wrap=tk.WORD, height=25, width=60)
    gui.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    gui.results_text.insert(tk.END, "Genera una computadora para ver resultados aquí...")
    gui.results_text.config(state=tk.DISABLED)
    
    # Marco de botones
    buttons_frame = ttk.Frame(right_pane)
    buttons_frame.pack(fill=tk.X, padx=10, pady=5)
    
    # Botón para agregar a comparación
    add_to_comparison_button = ctk.CTkButton(
        buttons_frame, 
        text="Agregar a comparación", 
        command=lambda: gui.add_to_comparison() if hasattr(gui, 'add_to_comparison') else None
    )
    add_to_comparison_button.pack(side=tk.LEFT, padx=5, pady=5)
    
    # Botón para guardar configuración
    save_button = ctk.CTkButton(
        buttons_frame, 
        text="Guardar configuración", 
        command=lambda: gui.save_configuration() if hasattr(gui, 'save_configuration') else None
    )
    save_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    # Marco para resumen de rendimiento
    performance_frame = ttk.LabelFrame(right_pane, text="Resumen de rendimiento")
    performance_frame.pack(fill=tk.X, padx=10, pady=10)
    
    # Rejilla para métricas de rendimiento
    for i in range(4):
        performance_frame.grid_columnconfigure(i, weight=1)
    
    # Métricas de rendimiento
    metrics = ["Gaming", "Productivity", "Content Creation", "Development"]
    gui.performance_vars = {}
    
    for i, metric in enumerate(metrics):
        ttk.Label(performance_frame, text=metric).grid(row=0, column=i, padx=5, pady=5)
        gui.performance_vars[metric.lower()] = tk.DoubleVar(value=0)
        
        performance_bar = ttk.Progressbar(
            performance_frame, 
            orient="horizontal", 
            length=100, 
            mode="determinate", 
            variable=gui.performance_vars[metric.lower()]
        )
        performance_bar.grid(row=1, column=i, padx=5, pady=5, sticky="ew")
        
        score_label = ttk.Label(performance_frame, text="0/100")
        score_label.grid(row=2, column=i, padx=5, pady=5)
        gui.performance_vars[f"{metric.lower()}_label"] = score_label
def update_results_text(self):
    # Después de mostrar los detalles de la computadora
    
    # Verificar compatibilidad con aplicación
    if hasattr(self, 'current_computer') and hasattr(self, 'application_var'):
        app_name = self.application_var.get()
        
        if app_name and app_name != "Ninguna":
            from algorithm.utils.application_requirements_validator import validate_application_requirements, display_validation_results
            from application_data import get_application_requirements
            
            # Obtener categoría
            usage_mapping = {
                'gaming': 'juegos',
                'office': 'ofimática',
                'graphics': 'diseño gráfico',
                'video': 'edición de video',
                'web': 'navegación web',
                'education': 'educación',
                'architecture': 'arquitectura'
            }
            usage = self.usage_var.get()
            category = usage_mapping.get(usage, '')
            
            # Obtener requisitos de la aplicación
            app_id = self.app_name_to_id.get(app_name)
            app_data = get_application_requirements(category, app_id)
            
            if app_data and 'requirements' in app_data:
                validation_results = validate_application_requirements(
                    self.current_computer, 
                    app_data['requirements']
                )
                
                # Agregar resultado de compatibilidad al texto de resultados
                self.results_text.insert(tk.END, "\n\nCompatibilidad con Aplicación:\n")
                compatibility_message = display_validation_results(validation_results)
                self.results_text.insert(tk.END, compatibility_message)