# component_browser_tab.py
from tkinter import ttk

def setup_component_browser_tab(gui):
    frame = ttk.Frame(gui.notebook)
    gui.notebook.add(frame, text=" Component Browser ")

    label = ttk.Label(frame, text="Explorador de componentes disponibles")
    label.pack(pady=10)
