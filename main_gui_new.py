import customtkinter as ctk
from gui.main_app import ComputerGeneratorGUI

def main():
    print("🚀 Iniciando aplicación...")

    # Set appearance mode and theme
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    # Create main window
    window = ctk.CTk()
    window.title("Computer Generator Pro")
    window.geometry("1200x800")
    
    # Create the GUI
    app = ComputerGeneratorGUI(window)
    
    # Start main loop
    window.mainloop()

if __name__ == "__main__":
    main()