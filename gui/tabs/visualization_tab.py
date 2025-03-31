# visualization_tab.py
from tkinter import ttk

def setup_visualization_tab(gui):
    frame = ttk.Frame(gui.notebook)
    gui.notebook.add(frame, text=" Visualization ")

    label = ttk.Label(frame, text="Visualización de componentes y datos")
    label.pack(pady=10)
