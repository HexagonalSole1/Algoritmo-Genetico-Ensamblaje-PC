# results_tab.py
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

def setup_results_tab(gui):
    frame = ttk.Frame(gui.notebook)
    gui.notebook.add(frame, text=" Results ")

    label = ttk.Label(frame, text="Resultados de computadoras generadas")
    label.pack(pady=10)

    gui.results_text = ScrolledText(frame, height=20, width=100)
    gui.results_text.pack(padx=10, pady=10)

    gui.results_text.insert("end", "Aquí aparecerán los resultados...\n")
    gui.results_text.config(state="disabled")
