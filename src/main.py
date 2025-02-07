import sys
import os
import customtkinter as ctk

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gui.main_window import MainWindow

def main():
    # Initialize the app
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Create main window
    app = MainWindow()
    app.mainloop()

if __name__ == "__main__":
    main()

