import customtkinter as ctk
from datetime import datetime
from src.utils.database import Database

class StatsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Swimming Statistics")
        self.geometry("800x600")
        self.minsize(600, 400)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_ui()
        self.calculate_stats()
        self.grab_set()
    
    def setup_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Swimming Statistics",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=20)
        
        # Stats container
        self.stats_frame = ctk.CTkFrame(self.main_frame)
        self.stats_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.stats_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Labels for statistics (will be populated in calculate_stats)
        self.total_distance_label = ctk.CTkLabel(
            self.stats_frame,
            text="Total Distance: ",
            font=("Helvetica", 16)
        )
        self.total_distance_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        
        self.total_sessions_label = ctk.CTkLabel(
            self.stats_frame,
            text="Total Sessions: ",
            font=("Helvetica", 16)
        )
        self.total_sessions_label.grid(row=1, column=0, pady=10, padx=20, sticky="w")
        
        self.avg_distance_label = ctk.CTkLabel(
            self.stats_frame,
            text="Average Distance per Session: ",
            font=("Helvetica", 16)
        )
        self.avg_distance_label.grid(row=2, column=0, pady=10, padx=20, sticky="w")
        
        self.avg_time_label = ctk.CTkLabel(
            self.stats_frame,
            text="Average Time per Session: ",
            font=("Helvetica", 16)
        )
        self.avg_time_label.grid(row=3, column=0, pady=10, padx=20, sticky="w")
    
    def calculate_stats(self):
        db = Database()
        sessions = db.get_sessions()
        
        if not sessions:
            self._show_no_data()
            return
        
        # Calculate statistics
        total_sessions = len(sessions)
        total_distance = sum(session.get("total_distance", 0) for session in sessions)
        total_time = sum(session.get("total_time", 0) for session in sessions)
        
        avg_distance = total_distance / total_sessions if total_sessions > 0 else 0
        avg_time = total_time / total_sessions if total_sessions > 0 else 0
        
        # Update labels
        self.total_distance_label.configure(
            text=f"Total Distance: {total_distance}m"
        )
        self.total_sessions_label.configure(
            text=f"Total Sessions: {total_sessions}"
        )
        self.avg_distance_label.configure(
            text=f"Average Distance per Session: {avg_distance:.1f}m"
        )
        self.avg_time_label.configure(
            text=f"Average Time per Session: {avg_time:.1f}s"
        )
    
    def _show_no_data(self):
        """Display message when no data is available"""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        no_data_label = ctk.CTkLabel(
            self.stats_frame,
            text="No session data available",
            font=("Helvetica", 16)
        )
        no_data_label.grid(row=0, column=0, pady=20)

