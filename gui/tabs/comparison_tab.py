# Actualizar gui/tabs/comparison_tab.py
from tkinter import ttk, Frame, Label, Canvas, Scrollbar
import tkinter as tk
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

def setup_comparison_tab(gui):
    frame = ttk.Frame(gui.notebook)
    gui.notebook.add(frame, text=" Comparison ")
    
    # Configurar grid
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    
    # Frame de controles superiores
    controls_frame = ttk.Frame(frame)
    controls_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    
    ttk.Label(controls_frame, text="Comparación de Configuraciones", font=("TkDefaultFont", 14, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
    
    # Botones
    gui.clear_comparison_button = ctk.CTkButton(controls_frame, text="Limpiar Comparación", 
                                             command=gui.clear_comparison)
    gui.clear_comparison_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    gui.export_comparison_button = ctk.CTkButton(controls_frame, text="Exportar Comparación", 
                                              command=gui.export_comparison)
    gui.export_comparison_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    # Área principal de comparación
    comparison_area = ttk.Frame(frame)
    comparison_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    
    # Configurar canvas desplazable para la comparación
    canvas = tk.Canvas(comparison_area, borderwidth=0)
    scrollbar = ttk.Scrollbar(comparison_area, orient=tk.VERTICAL, command=canvas.yview)
    gui.comparison_container = ttk.Frame(canvas)
    
    canvas.configure(yscrollcommand=scrollbar.set)
    
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    canvas_window = canvas.create_window((0, 0), window=gui.comparison_container, anchor=tk.NW)
    
    # Configurar desplazamiento
    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))
    
    def configure_canvas_width(event):
        canvas.itemconfig(canvas_window, width=event.width)
    
    gui.comparison_container.bind("<Configure>", configure_scroll_region)
    canvas.bind("<Configure>", configure_canvas_width)
    
    # Texto de marcador de posición inicial
    ttk.Label(gui.comparison_container, text="Agrega configuraciones para compararlas lado a lado...").pack(padx=20, pady=20)