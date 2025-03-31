# visualization_tab.py
import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import os

# Define todas las funciones primero, antes de usarlas
def update_visualization(gui, event=None):
    """Actualiza la visualización según el tipo de gráfico seleccionado"""
    gui.status_bar.config(text="Actualizando visualización...")

def create_radar_chart(gui):
    """Crea un gráfico radar de métricas de rendimiento"""
    gui.status_bar.config(text="Creando gráfico radar...")

def create_bar_chart(gui):
    """Crea un gráfico de barras de métricas de rendimiento"""
    gui.status_bar.config(text="Creando gráfico de barras...")

def create_heatmap_chart(gui):
    """Crea un mapa de calor comparando calidad de componentes"""
    gui.status_bar.config(text="Creando mapa de calor...")

def create_evolution_chart(gui):
    """Crea un gráfico mostrando la evolución del fitness durante la optimización"""
    gui.status_bar.config(text="Creando gráfico de evolución...")

def export_chart(gui):
    """Exporta el gráfico actual a un archivo"""
    gui.status_bar.config(text="Exportando gráfico...")

def setup_visualization_tab(gui):
    """Set up the visualization tab for displaying charts and graphs"""
    # Create the tab
    visualization_frame = ttk.Frame(gui.notebook)
    gui.notebook.add(visualization_frame, text=" Visualization ")
    
    # Configure the grid
    visualization_frame.grid_columnconfigure(0, weight=1)
    visualization_frame.grid_rowconfigure(1, weight=1)
    
    # Top controls frame
    controls_frame = ttk.Frame(visualization_frame)
    controls_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
    
    ttk.Label(controls_frame, text="Performance Visualization", font=("TkDefaultFont", 14, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
    
    # Chart type selection
    ttk.Label(controls_frame, text="Chart Type:").pack(side=tk.LEFT, padx=10, pady=5)
    gui.chart_type_var = tk.StringVar(value="radar")
    chart_types = ["radar", "bar", "heatmap", "evolution"]
    chart_type_dropdown = ttk.Combobox(controls_frame, textvariable=gui.chart_type_var, 
                                     values=chart_types, width=10,
                                     state="readonly")
    chart_type_dropdown.pack(side=tk.LEFT, padx=5, pady=5)
    chart_type_dropdown.bind("<<ComboboxSelected>>", lambda e: update_visualization(gui, e))
    
    # Export button
    export_button = ctk.CTkButton(controls_frame, text="Export Chart", 
                                command=lambda: export_chart(gui))
    export_button.pack(side=tk.RIGHT, padx=5, pady=5)
    
    # Main visualization area
    gui.visualization_area = ttk.Frame(visualization_frame)
    gui.visualization_area.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    
    # Create a figure for matplotlib
    gui.figure = Figure(figsize=(10, 6), dpi=100)
    gui.plot = gui.figure.add_subplot(111)
    
    # Create canvas for matplotlib figure
    gui.chart_canvas = FigureCanvasTkAgg(gui.figure, gui.visualization_area)
    gui.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    # Add placeholder text on the plot
    gui.plot.text(0.5, 0.5, "Generate a computer to visualize performance data", 
                 horizontalalignment='center', verticalalignment='center',
                 transform=gui.plot.transAxes, fontsize=14)
    gui.plot.axis('off')
    gui.chart_canvas.draw()
    
    # Asignar funciones al objeto gui
    gui.update_visualization = update_visualization
    gui.create_radar_chart = create_radar_chart
    gui.create_bar_chart = create_bar_chart
    gui.create_heatmap_chart = create_heatmap_chart
    gui.create_evolution_chart = create_evolution_chart
    gui.export_chart = export_chart