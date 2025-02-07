import customtkinter as ctk
from datetime import datetime
from src.gui.session_window import SessionWindow  # Update to absolute import
from src.utils.database import Database

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Swimming Training Tracker")
        self.geometry("1024x768")
        self.minsize(800, 600)  # Set minimum window size
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main container
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame with grid
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)  # Sessions frame expands
        
        # Title frame
        self.title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.title_frame.grid_columnconfigure(1, weight=1)  # Space between title and date
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="Swimming Training Tracker",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=20)
        
        # Date display
        self.date_label = ctk.CTkLabel(
            self.title_frame,
            text=datetime.now().strftime("%d %B %Y"),
            font=("Helvetica", 16)
        )
        self.date_label.grid(row=0, column=2, padx=20)
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.grid(row=1, column=0, sticky="ew", pady=20)
        self.buttons_frame.grid_columnconfigure((0, 1, 2), weight=1)  # Equal space distribution
        
        # Add main buttons
        self.new_session_btn = ctk.CTkButton(
            self.buttons_frame,
            text="New Session",
            font=("Helvetica", 14),
            width=200,
            height=40,
            command=self.open_new_session
        )
        self.new_session_btn.grid(row=0, column=0, padx=10)
        
        self.view_stats_btn = ctk.CTkButton(
            self.buttons_frame,
            text="View Statistics",
            font=("Helvetica", 14),
            width=200,
            height=40,
            command=self.open_statistics
        )
        self.view_stats_btn.grid(row=0, column=1, padx=10)
        
        # Sessions frame
        self.sessions_frame = ctk.CTkFrame(self.main_frame)
        self.sessions_frame.grid(row=2, column=0, sticky="nsew", pady=20)
        self.sessions_frame.grid_columnconfigure(0, weight=1)
        self.sessions_frame.grid_rowconfigure(1, weight=1)  # Make list expandable
        
        # Sessions title
        self.sessions_label = ctk.CTkLabel(
            self.sessions_frame,
            text="Recent Sessions",
            font=("Helvetica", 18, "bold")
        )
        self.sessions_label.grid(row=0, column=0, pady=10)
        
        # Sessions list
        self.sessions_list = ctk.CTkTextbox(
            self.sessions_frame,
            font=("Helvetica", 14),
            wrap="none"
        )
        self.sessions_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.sessions_list.insert("1.0", "No recent sessions")
        self.sessions_list.configure(state="disabled")
    
    def open_new_session(self):
        session_window = SessionWindow(self)
        self.wait_window(session_window)
        self.refresh_sessions_list()  # Refresh after window closes
    
    def open_statistics(self):
        # TODO: Implement statistics window
        pass

    def refresh_sessions_list(self):
        """Update the sessions list display"""
        self.sessions_list.configure(state="normal")
        self.sessions_list.delete("1.0", "end")
        
        db = Database()
        sessions = db.get_sessions()
        
        if not sessions:
            self.sessions_list.insert("1.0", "No recent sessions")
        else:
            for session in reversed(sessions):  # Show most recent first
                date = session["date"]
                distance = session["total_distance"]
                time = session["total_time"]
                
                session_text = (f"Date: {date}\n"
                              f"Distance: {distance}m\n"
                              f"Time: {time}s\n"
                              f"{'-' * 40}\n\n")
                
                self.sessions_list.insert("end", session_text)
        
        self.sessions_list.configure(state="disabled")

