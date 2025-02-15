import customtkinter as ctk
from datetime import datetime

class HistoryFrame(ctk.CTkFrame):
    def __init__(self, master, db, **kwargs):
        super().__init__(master, **kwargs)
        self.db = db
        
        # Create table headers
        headers = ["Date", "Duration (min)", "Distance (m)", "Stroke", "Notes"]
        for i, header in enumerate(headers):
            label = ctk.CTkLabel(self, text=header, font=("Arial", 12, "bold"))
            label.grid(row=0, column=i, padx=5, pady=5, sticky="w")
        
        self.update_history()
    
    def update_history(self):
        """Update the history view with latest data"""
        # Clear existing items
        for widget in self.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.destroy()
        
        # Get and display sessions
        sessions = self.db.get_all_sessions()
        for i, session in enumerate(sessions, start=1):
            for j, value in enumerate(session):
                text = value
                if j == 0:  # Format date
                    text = datetime.fromisoformat(value).strftime("%Y-%m-%d %H:%M")
                label = ctk.CTkLabel(self, text=str(text))
                label.grid(row=i, column=j, padx=5, pady=2, sticky="w")