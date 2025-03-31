import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

def setup_generator_tab(app):
    generator_frame = ttk.Frame(app.notebook)
    app.notebook.add(generator_frame, text=" Generator ")

    generator_frame.grid_columnconfigure(0, weight=1)
    generator_frame.grid_rowconfigure(3, weight=1)

    # --- Sección: User Requirements ---
    user_frame = ctk.CTkFrame(generator_frame)
    user_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)

    ttk.Label(user_frame, text="User Requirements", font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)

    app.usage_var = tk.StringVar(value="gaming")
    app.computer_usages = {
        'gaming': 'Gaming',
        'office': 'Office Work',
        'graphics': 'Graphic Design',
        'video': 'Video Editing',
        'web': 'Web Browsing',
        'education': 'Education',
        'architecture': 'Architecture/CAD'
    }

    usage_frame = ttk.Frame(user_frame)
    usage_frame.grid(row=1, column=0, sticky="w", padx=10, pady=5)

    for i, (key, label) in enumerate(app.computer_usages.items()):
        ttk.Radiobutton(
            usage_frame, text=label, variable=app.usage_var, value=key
        ).grid(row=i//4, column=i%4, sticky="w", padx=5, pady=2)

    # --- Sección: Algorithm Parameters ---
    algorithm_frame = ctk.CTkFrame(generator_frame)
    algorithm_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=10)

    ttk.Label(algorithm_frame, text="Algorithm Parameters", font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)

    param_labels = ["Population Size", "Generations", "Crossover Rate", "Mutation Rate"]
    app.population_var = tk.IntVar(value=30)
    app.generations_var = tk.IntVar(value=50)
    app.crossover_var = tk.DoubleVar(value=0.7)
    app.mutation_var = tk.DoubleVar(value=0.1)
    param_vars = [app.population_var, app.generations_var, app.crossover_var, app.mutation_var]

    for i, (label, var) in enumerate(zip(param_labels, param_vars)):
        ttk.Label(algorithm_frame, text=label + ":").grid(row=i+1, column=0, sticky="w", padx=10, pady=3)
        ttk.Entry(algorithm_frame, textvariable=var).grid(row=i+1, column=1, sticky="w", padx=10, pady=3)

    # --- Sección: Component Preferences ---
    preferences_frame = ctk.CTkFrame(generator_frame)
    preferences_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)

    ttk.Label(preferences_frame, text="Component Preferences", font=("TkDefaultFont", 14, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)

    app.brand_var = tk.StringVar()
    ttk.Label(preferences_frame, text="Preferred Brand:").grid(row=1, column=0, sticky="w", padx=10, pady=3)
    ttk.Entry(preferences_frame, textvariable=app.brand_var).grid(row=1, column=1, padx=10, pady=3)

    app.max_budget_var = tk.DoubleVar(value=2000.0)
    ttk.Label(preferences_frame, text="Max Budget ($):").grid(row=2, column=0, sticky="w", padx=10, pady=3)
    ttk.Entry(preferences_frame, textvariable=app.max_budget_var).grid(row=2, column=1, padx=10, pady=3)

    # --- Botones de Control ---
    button_frame = ctk.CTkFrame(generator_frame)
    button_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=10)

    generate_button = ctk.CTkButton(button_frame, text="Generate", command=app.generate_computers)
    generate_button.pack(side="left", padx=10)

    stop_button = ctk.CTkButton(button_frame, text="Stop", command=app.stop_generation)
    stop_button.pack(side="left", padx=10)

    clear_button = ctk.CTkButton(button_frame, text="Clear", command=app.clear_results)
    clear_button.pack(side="left", padx=10)
