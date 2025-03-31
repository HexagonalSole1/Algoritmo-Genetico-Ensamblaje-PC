# comparison_tab.py
from tkinter import ttk

def setup_comparison_tab(gui):
    frame = ttk.Frame(gui.notebook)
    gui.notebook.add(frame, text=" Comparison ")

    label = ttk.Label(frame, text="Comparación de computadoras generadas")
    label.pack(pady=10)
