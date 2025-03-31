# menu.py
import tkinter as tk

def create_menu(gui):
    menubar = tk.Menu(gui.master)

    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="New Configuration", command=gui.new_configuration)
    file_menu.add_command(label="Open Configuration", command=gui.open_configuration)
    file_menu.add_command(label="Save Configuration", command=gui.save_configuration)
    file_menu.add_separator()
    file_menu.add_command(label="Export Results", command=gui.export_results)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=gui.master.quit)
    menubar.add_cascade(label="File", menu=file_menu)

    edit_menu = tk.Menu(menubar, tearoff=0)
    edit_menu.add_command(label="Preferences", command=gui.show_preferences)
    menubar.add_cascade(label="Edit", menu=edit_menu)

    view_menu = tk.Menu(menubar, tearoff=0)
    theme_menu = tk.Menu(view_menu, tearoff=0)
    theme_menu.add_command(label="Light Mode", command=lambda: gui.change_theme("Light"))
    theme_menu.add_command(label="Dark Mode", command=lambda: gui.change_theme("Dark"))
    theme_menu.add_command(label="System Default", command=lambda: gui.change_theme("System"))
    view_menu.add_cascade(label="Theme", menu=theme_menu)
    menubar.add_cascade(label="View", menu=view_menu)

    help_menu = tk.Menu(menubar, tearoff=0)
    help_menu.add_command(label="Documentation", command=gui.show_documentation)
    help_menu.add_command(label="About", command=gui.show_about)
    menubar.add_cascade(label="Help", menu=help_menu)

    gui.master.config(menu=menubar)
