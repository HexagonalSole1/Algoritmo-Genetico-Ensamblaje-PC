# include_exclude.py
import tkinter as tk
from tkinter import ttk

def show_include_exclude(gui):
    window = tk.Toplevel(gui.master)
    window.title("Incluir/Excluir componentes")
    window.geometry("400x300")

    include_label = ttk.Label(window, text="Componentes a incluir:")
    include_label.pack(pady=5)
    include_entry = ttk.Entry(window, width=50)
    include_entry.pack(pady=5)
    include_entry.insert(0, ", ".join(gui.include_components))

    exclude_label = ttk.Label(window, text="Componentes a excluir:")
    exclude_label.pack(pady=5)
    exclude_entry = ttk.Entry(window, width=50)
    exclude_entry.pack(pady=5)
    exclude_entry.insert(0, ", ".join(gui.exclude_components))

    def apply():
        gui.include_components = [c.strip() for c in include_entry.get().split(",") if c.strip()]
        gui.exclude_components = [c.strip() for c in exclude_entry.get().split(",") if c.strip()]
        window.destroy()

    def clear_all():
        include_entry.delete(0, tk.END)
        exclude_entry.delete(0, tk.END)

    button_frame = ttk.Frame(window)
    button_frame.pack(pady=10)

    ttk.Button(button_frame, text="Aplicar", command=apply).grid(row=0, column=0, padx=5)
    ttk.Button(button_frame, text="Limpiar", command=clear_all).grid(row=0, column=1, padx=5)
