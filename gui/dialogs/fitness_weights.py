# fitness_weights.py
import tkinter as tk
from tkinter import ttk

def show_fitness_weights(gui):
    window = tk.Toplevel(gui.master)
    window.title("Ajustar pesos de fitness")
    window.geometry("300x250")

    entries = {}

    for i, criterio in enumerate(gui.fitness_weights.keys()):
        ttk.Label(window, text=criterio).grid(row=i, column=0, padx=10, pady=5, sticky='w')
        entry = ttk.Entry(window)
        entry.insert(0, str(gui.fitness_weights[criterio]))
        entry.grid(row=i, column=1, padx=10, pady=5)
        entries[criterio] = entry

    def apply_weights():
        for k, v in entries.items():
            try:
                gui.fitness_weights[k] = float(v.get())
            except ValueError:
                pass  # puedes mostrar una advertencia si lo deseas
        window.destroy()

    def reset_weights():
        for k, v in entries.items():
            v.delete(0, tk.END)
            v.insert(0, "1.0")

    ttk.Button(window, text="Aplicar", command=apply_weights).grid(row=len(entries), column=0, pady=10)
    ttk.Button(window, text="Reset", command=reset_weights).grid(row=len(entries), column=1, pady=10)
