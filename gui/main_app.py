import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from tkinter.scrolledtext import ScrolledText

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

        # Estilo y tema
        setup_style(self)

        # Ventana principal
        self.setup_main_window()

        # Variables de estado
        self.current_computer = None
        self.generated_computers = []
        self.optimization_running = False
        self.result_history = []

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
        # Puedes implementar lógica al cambiar de pestaña aquí
        pass

    def load_application_settings(self):
        """Carga configuraciones si es necesario"""
        pass

    def change_theme(self, mode):
        """Cambia el tema (claro/oscuro/sistema)"""
        ctk.set_appearance_mode(mode)
        update_colors(self)

    # Métodos de navegación que pueden ser usados por menu.py
    def new_configuration(self):
        self.reset_form()
        self.status_bar.config(text="New configuration started.")

    def open_configuration(self):
        print("Abrir configuración (por implementar)")

    def save_configuration(self):
        print("Guardar configuración (por implementar)")

    def export_results(self):
        print("Exportar resultados (por implementar)")

    def show_preferences(self):
        print("Mostrar preferencias (por implementar)")

    def show_documentation(self):
        print("Abrir documentación (por implementar)")

    def show_about(self):
        tk.messagebox.showinfo("About", "Computer Generator Pro\nDesarrollado con ♥")

    def reset_form(self):
        print("Resetear formulario (implementación futura)")
    def generate_computers(self):
        print("🔧 Generando computadoras... (lógica aún no implementada)")

    def stop_generation(self):
        print("⛔ Generación detenida.")

    def clear_results(self):
        print("🧹 Resultados limpiados.")
