# generator_tab.py
import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

def setup_generator_tab(gui):
    generator_frame = ttk.Frame(gui.notebook)
    gui.notebook.add(generator_frame, text=" Generator ")

    # Configurar la cuadrícula
    for i in range(12):
        generator_frame.grid_columnconfigure(i, weight=1)
    generator_frame.grid_rowconfigure(10, weight=1)  # Fila inferior expandible

    # 1. Sección de Requisitos de Usuario
    requirements_frame = ctk.CTkFrame(generator_frame)
    requirements_frame.grid(row=0, column=0, columnspan=12, sticky="ew", padx=10, pady=10)
    
    ttk.Label(requirements_frame, text="User Requirements", font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    
    # Selección de uso
    ttk.Label(requirements_frame, text="Primary Usage:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    gui.usage_var = tk.StringVar(value="gaming")
    gui.computer_usages = {
        'gaming': 'Gaming',
        'office': 'Office Work',
        'graphics': 'Graphic Design',
        'video': 'Video Editing',
        'web': 'Web Browsing',
        'education': 'Education',
        'architecture': 'Architecture/CAD'
    }
    
    usage_frame = ttk.Frame(requirements_frame)
    usage_frame.grid(row=1, column=1, columnspan=3, sticky="w", padx=10, pady=5)
    
    for i, (key, value) in enumerate(gui.computer_usages.items()):
        col = i % 4
        row = i // 4 + 1
        ttk.Radiobutton(usage_frame, text=value, variable=gui.usage_var, value=key, 
                        command=lambda: gui.on_usage_changed() if hasattr(gui, 'on_usage_changed') else None).grid(row=row, column=col, sticky="w", padx=10, pady=2)
    
    # Rango de precio
    ttk.Label(requirements_frame, text="Price Range:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    price_frame = ttk.Frame(requirements_frame)
    price_frame.grid(row=3, column=1, columnspan=3, sticky="w", padx=10, pady=5)
    
    ttk.Label(price_frame, text="Min:").grid(row=0, column=0, sticky="w")
    gui.price_min_var = tk.StringVar(value="8000")
    gui.price_min_entry = ttk.Entry(price_frame, textvariable=gui.price_min_var, width=10)
    gui.price_min_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    
    ttk.Label(price_frame, text="Max:").grid(row=0, column=2, sticky="w")
    gui.price_max_var = tk.StringVar(value="15000")
    gui.price_max_entry = ttk.Entry(price_frame, textvariable=gui.price_max_var, width=10)
    gui.price_max_entry.grid(row=0, column=3, sticky="w", padx=5, pady=5)
    
    # Slider de precio
    gui.price_range_slider = ctk.CTkSlider(requirements_frame, from_=0, to=50000,
                                           number_of_steps=50, width=400)
    gui.price_range_slider.grid(row=3, column=4, columnspan=4, sticky="ew", padx=10, pady=5)
    gui.price_range_slider.set(15000)  # Valor por defecto
    
    # Selección de prioridad
    ttk.Label(requirements_frame, text="Priority:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    gui.priority_var = tk.StringVar(value="balanced")
    priority_frame = ttk.Frame(requirements_frame)
    priority_frame.grid(row=4, column=1, columnspan=3, sticky="w", padx=10, pady=5)
    
    ttk.Radiobutton(priority_frame, text="Performance", variable=gui.priority_var, value="performance").grid(row=0, column=0, sticky="w", padx=10)
    ttk.Radiobutton(priority_frame, text="Value", variable=gui.priority_var, value="value").grid(row=0, column=1, sticky="w", padx=10)
    ttk.Radiobutton(priority_frame, text="Balanced", variable=gui.priority_var, value="balanced").grid(row=0, column=2, sticky="w", padx=10)
    
    # Factor de forma
    ttk.Label(requirements_frame, text="Form Factor:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    gui.form_factor_var = tk.StringVar(value="ATX")
    form_factor_frame = ttk.Frame(requirements_frame)
    form_factor_frame.grid(row=5, column=1, columnspan=3, sticky="w", padx=10, pady=5)
    
    ttk.Radiobutton(form_factor_frame, text="ATX", variable=gui.form_factor_var, value="ATX").grid(row=0, column=0, sticky="w", padx=10)
    ttk.Radiobutton(form_factor_frame, text="Micro-ATX", variable=gui.form_factor_var, value="Micro-ATX").grid(row=0, column=1, sticky="w", padx=10)
    ttk.Radiobutton(form_factor_frame, text="Mini-ITX", variable=gui.form_factor_var, value="Mini-ITX").grid(row=0, column=2, sticky="w", padx=10)
    
    # Future-proofing
    gui.future_proof_var = tk.BooleanVar(value=False)
    future_proof_check = ttk.Checkbutton(requirements_frame, text="Prioritize Future-Proofing", 
                                        variable=gui.future_proof_var)
    future_proof_check.grid(row=5, column=4, sticky="w", padx=10, pady=5)
    
    # 2. Sección de Parámetros del Algoritmo
    algo_frame = ctk.CTkFrame(generator_frame)
    algo_frame.grid(row=1, column=0, columnspan=12, sticky="ew", padx=10, pady=10)
    
    ttk.Label(algo_frame, text="Algorithm Parameters", font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    
    # Tamaño de población
    ttk.Label(algo_frame, text="Population Size:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    gui.population_var = tk.StringVar(value="50")
    population_size_entry = ttk.Entry(algo_frame, textvariable=gui.population_var, width=10)
    population_size_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
    
    ttk.Label(algo_frame, text="Generations:").grid(row=1, column=2, sticky="w", padx=10, pady=5)
    gui.generations_var = tk.StringVar(value="100")
    generations_entry = ttk.Entry(algo_frame, textvariable=gui.generations_var, width=10)
    generations_entry.grid(row=1, column=3, sticky="w", padx=5, pady=5)
    
    ttk.Label(algo_frame, text="Crossover Rate:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    gui.crossover_var = tk.StringVar(value="0.8")
    crossover_rate_entry = ttk.Entry(algo_frame, textvariable=gui.crossover_var, width=10)
    crossover_rate_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
    
    ttk.Label(algo_frame, text="Mutation Rate:").grid(row=2, column=2, sticky="w", padx=10, pady=5)
    gui.mutation_var = tk.StringVar(value="0.1")
    mutation_rate_entry = ttk.Entry(algo_frame, textvariable=gui.mutation_var, width=10)
    mutation_rate_entry.grid(row=2, column=3, sticky="w", padx=5, pady=5)
    
    ttk.Label(algo_frame, text="Elitism %:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    gui.elitism_var = tk.StringVar(value="10")
    elitism_entry = ttk.Entry(algo_frame, textvariable=gui.elitism_var, width=10)
    elitism_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)
    
    # Opciones avanzadas toggle
    gui.advanced_options_var = tk.BooleanVar(value=False)
    advanced_options_check = ttk.Checkbutton(algo_frame, text="Show Advanced Options", 
                                           variable=gui.advanced_options_var,
                                           command=lambda: gui.toggle_advanced_options() if hasattr(gui, 'toggle_advanced_options') else None)
    advanced_options_check.grid(row=3, column=2, columnspan=2, sticky="w", padx=10, pady=5)
    
    # Advanced options frame (initially hidden)
    gui.advanced_frame = ttk.Frame(algo_frame)
    gui.advanced_frame.grid(row=4, column=0, columnspan=6, sticky="ew", padx=10, pady=5)
    gui.advanced_frame.grid_remove()  # Hide initially
    
    ttk.Label(gui.advanced_frame, text="Tournament Size:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    gui.tournament_size_var = tk.StringVar(value="3")
    tournament_size_entry = ttk.Entry(gui.advanced_frame, textvariable=gui.tournament_size_var, width=10)
    tournament_size_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
    
    gui.adaptive_mutation_var = tk.BooleanVar(value=True)
    adaptive_mutation_check = ttk.Checkbutton(gui.advanced_frame, text="Adaptive Mutation", 
                                            variable=gui.adaptive_mutation_var)
    adaptive_mutation_check.grid(row=0, column=2, sticky="w", padx=10, pady=5)
    
    # Fitness weights button
    fitness_weights_button = ctk.CTkButton(gui.advanced_frame, text="Fitness Weights", 
                                          command=lambda: gui.show_fitness_weights() if hasattr(gui, 'show_fitness_weights') else None)
    fitness_weights_button.grid(row=0, column=3, sticky="w", padx=10, pady=5)
    
    # 3. Sección de Preferencias de Componentes
    components_frame = ctk.CTkFrame(generator_frame)
    components_frame.grid(row=2, column=0, columnspan=12, sticky="ew", padx=10, pady=10)
    
    ttk.Label(components_frame, text="Component Preferences", font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    
    # Preferencias de marca
    ttk.Label(components_frame, text="Brand Preferences:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    
    # Crear un marco para preferencias de marca
    brands_frame = ttk.Frame(components_frame)
    brands_frame.grid(row=1, column=1, columnspan=5, sticky="w", padx=10, pady=5)
    
    # Etiquetas de tipo de componente
    component_types = ["CPU", "GPU", "Motherboard", "RAM", "Storage"]
    for i, comp_type in enumerate(component_types):
        ttk.Label(brands_frame, text=comp_type + ":").grid(row=0, column=i, sticky="w", padx=5, pady=2)
    
    # Listas desplegables de preferencias de marca
    gui.brand_preferences = {}
    for i, comp_type in enumerate(component_types):
        gui.brand_preferences[comp_type.lower()] = tk.StringVar(value="No Preference")
        brands = ["No Preference", "Intel", "AMD"] if comp_type == "CPU" else ["No Preference", "ASUS", "MSI", "Gigabyte", "EVGA"]
        brand_dropdown = ttk.Combobox(brands_frame, textvariable=gui.brand_preferences[comp_type.lower()], values=brands, width=12)
        brand_dropdown.grid(row=1, column=i, sticky="w", padx=5, pady=2)
        brand_dropdown.state(["readonly"])
    
    # Botón para incluir/excluir componentes
    include_exclude_button = ctk.CTkButton(components_frame, text="Include/Exclude Components", 
                                         command=lambda: gui.show_include_exclude() if hasattr(gui, 'show_include_exclude') else None)
    include_exclude_button.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)
    
    # Preferencias estéticas
    ttk.Label(components_frame, text="Aesthetics:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    
    # Marco de estética
    aesthetics_frame = ttk.Frame(components_frame)
    aesthetics_frame.grid(row=3, column=1, columnspan=5, sticky="w", padx=10, pady=5)
    
    # Preferencia de iluminación RGB
    gui.rgb_lighting_var = tk.BooleanVar(value=False)
    rgb_check = ttk.Checkbutton(aesthetics_frame, text="RGB Lighting", variable=gui.rgb_lighting_var)
    rgb_check.grid(row=0, column=0, sticky="w", padx=10, pady=2)
    
    # Preferencia de color del gabinete
    ttk.Label(aesthetics_frame, text="Color:").grid(row=0, column=1, sticky="w", padx=10, pady=2)
    gui.case_color_var = tk.StringVar(value="Black")
    case_colors = ["Black", "White", "Red", "Blue", "Green", "Custom"]
    case_color_dropdown = ttk.Combobox(aesthetics_frame, textvariable=gui.case_color_var, values=case_colors, width=10)
    case_color_dropdown.grid(row=0, column=2, sticky="w", padx=5, pady=2)
    case_color_dropdown.state(["readonly"])
    
    # Botón de color personalizado
    color_button = ctk.CTkButton(aesthetics_frame, text="Choose Color", 
                               command=lambda: gui.choose_custom_color() if hasattr(gui, 'choose_custom_color') else None, 
                               width=20)
    color_button.grid(row=0, column=3, sticky="w", padx=5, pady=2)
    
    # 4. Botones de Acción
    actions_frame = ctk.CTkFrame(generator_frame)
    actions_frame.grid(row=3, column=0, columnspan=12, sticky="ew", padx=10, pady=10)
    
    # Botón generar
    gui.generate_button = ctk.CTkButton(actions_frame, text="Generate Computer", 
                                      command=gui.generate_computers,
                                      height=40, width=200,
                                      font=("TkDefaultFont", 14))
    gui.generate_button.grid(row=0, column=0, padx=10, pady=10)
    
    # Botón detener (inicialmente desactivado)
    gui.stop_button = ctk.CTkButton(actions_frame, text="Stop", 
                                  command=gui.stop_generation,
                                  height=40, width=100,
                                  state="disabled",
                                  font=("TkDefaultFont", 14))
    gui.stop_button.grid(row=0, column=1, padx=10, pady=10)
    
    # Botón reset
    reset_button = ctk.CTkButton(actions_frame, text="Reset", 
                               command=gui.reset_form,
                               height=40, width=100)
    reset_button.grid(row=0, column=2, padx=10, pady=10)
    
    # Barra de progreso (inicialmente oculta)
    gui.progress_var = tk.DoubleVar(value=0)
    gui.progress_bar = ttk.Progressbar(actions_frame, orient="horizontal", 
                                     length=400, mode="determinate", 
                                     variable=gui.progress_var)
    gui.progress_bar.grid(row=1, column=0, columnspan=3, sticky="ew", padx=10, pady=10)
    gui.progress_bar.grid_remove()  # Ocultar inicialmente
    
    # Etiqueta de estado
    gui.status_label = ttk.Label(actions_frame, text="")
    gui.status_label.grid(row=2, column=0, columnspan=3, sticky="w", padx=10, pady=5)
    
    # 5. Vista previa de resultados
    results_preview_frame = ctk.CTkFrame(generator_frame)
    results_preview_frame.grid(row=4, column=0, columnspan=12, sticky="nsew", padx=10, pady=10)
    results_preview_frame.grid_rowconfigure(1, weight=1)
    results_preview_frame.grid_columnconfigure(0, weight=1)
    
    ttk.Label(results_preview_frame, text="Results Preview", font=("TkDefaultFont", 14, "bold")).grid(
        row=0, column=0, sticky="w", padx=10, pady=5)
    
    # Área de texto de resultados
    gui.results_preview_text = tk.scrolledtext.ScrolledText(results_preview_frame, wrap=tk.WORD, height=15, width=80)
    gui.results_preview_text.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)
    gui.results_preview_text.insert(tk.END, "Generate a computer to see results here...")
    gui.results_preview_text.config(state=tk.DISABLED)