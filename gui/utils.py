# utils.py
from tkinter import END
import matplotlib.pyplot as plt

def update_results_text(gui, text):
    gui.results_text.config(state="normal")
    gui.results_text.delete("1.0", END)
    gui.results_text.insert(END, text)
    gui.results_text.config(state="disabled")

def update_progress(gui, value):
    gui.progress_bar.set(value / 100.0)
    gui.status_bar.config(text=f"Progreso: {value}%")
    gui.master.update_idletasks()

def update_components_tree(gui, components):
    for item in gui.components_tree.get_children():
        gui.components_tree.delete(item)
    
    for comp in components:
        gui.components_tree.insert("", "end", values=(
            comp.name,
            comp.brand,
            comp.price,
            comp.performance,
            comp.category
        ))

def update_performance_display(gui, performance_data):
    gui.performance_canvas.figure.clear()
    ax = gui.performance_canvas.figure.add_subplot(111)
    
    labels = list(performance_data.keys())
    values = list(performance_data.values())

    ax.bar(labels, values, color=gui.accent_color)
    ax.set_title("Rendimiento por categoría")
    ax.set_ylabel("Puntaje")
    ax.set_xlabel("Categoría")

    gui.performance_canvas.draw()

def format_price(value):
    return f"${value:,.2f}"
