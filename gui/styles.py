# styles.py
import customtkinter as ctk
import matplotlib.pyplot as plt
from tkinter import ttk

def setup_style(gui):
    """Configura el estilo general y modo de apariencia"""
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")
    gui.style = ttk.Style()
    gui.style.theme_use('clam')
    update_colors(gui)

def update_colors(gui):
    """Actualiza los colores según el modo actual (Dark o Light)"""
    mode = ctk.get_appearance_mode()

    if mode == "Dark":
        gui.bg_color = "#2b2b2b"
        gui.fg_color = "#e0e0e0"
        gui.accent_color = "#3a7ebf"
        gui.subtle_color = "#3c3c3c"
    else:
        gui.bg_color = "#f0f0f0"
        gui.fg_color = "#202020"
        gui.accent_color = "#3a7ebf"
        gui.subtle_color = "#e0e0e0"

    gui.style.configure('TFrame', background=gui.bg_color)
    gui.style.configure('TLabel', background=gui.bg_color, foreground=gui.fg_color)
    gui.style.configure('TButton', background=gui.accent_color, foreground=gui.fg_color)
    gui.style.configure('TNotebook', background=gui.bg_color, foreground=gui.fg_color)
    gui.style.configure('TNotebook.Tab', background=gui.subtle_color, foreground=gui.fg_color)

    if mode == "Dark":
        plt.style.use('dark_background')
    else:
        plt.style.use('default')
