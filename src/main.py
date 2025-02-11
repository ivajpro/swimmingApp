import sys
import os
import customtkinter as ctk
from src.data.database import Database

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.gui.main_window import MainWindow

def main():
    # Initialize the app
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    # Initialize database
    db = Database()
    
    # Create main window with database instance
    app = MainWindow(db)
    app.mainloop()

if __name__ == "__main__":
    main()

