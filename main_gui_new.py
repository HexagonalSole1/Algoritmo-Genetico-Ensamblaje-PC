import customtkinter as ctk
from gui.main_app import ComputerGeneratorGUI

def main():
    print("🚀 Iniciando aplicación...")

    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    window = ctk.CTk()
    app = ComputerGeneratorGUI(window)
    window.mainloop()

if __name__ == "__main__":
    main()
