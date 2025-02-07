import customtkinter as ctk
from datetime import datetime
from gui.session_window import SessionWindow  # Update import path

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Swimming Training Tracker")
        self.geometry("1024x768")
        
        # Set theme
        self.configure(fg_color=("#FFFFFF", "#333333"))  # Light/Dark mode colors
        
        # Create main container
        self.setup_ui()
    
    def setup_ui(self):
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title frame
        self.title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.title_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="Swimming Training Tracker",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.pack(side="left", padx=20)
        
        # Date display
        self.date_label = ctk.CTkLabel(
            self.title_frame,
            text=datetime.now().strftime("%d %B %Y"),
            font=("Helvetica", 16)
        )
        self.date_label.pack(side="right", padx=20)
        
        # Create buttons frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.pack(fill="x", pady=20)
        
        # Add main buttons
        self.new_session_btn = ctk.CTkButton(
            self.buttons_frame,
            text="New Session",
            font=("Helvetica", 14),
            width=200,
            height=40,
            command=self.open_new_session
        )
        self.new_session_btn.pack(side="left", padx=10)
        
        self.view_stats_btn = ctk.CTkButton(
            self.buttons_frame,
            text="View Statistics",
            font=("Helvetica", 14),
            width=200,
            height=40,
            command=self.open_statistics
        )
        self.view_stats_btn.pack(side="left", padx=10)
        
        # Create recent sessions frame
        self.sessions_frame = ctk.CTkFrame(self.main_frame)
        self.sessions_frame.pack(fill="both", expand=True, pady=20)
        
        # Recent sessions title
        self.sessions_label = ctk.CTkLabel(
            self.sessions_frame,
            text="Recent Sessions",
            font=("Helvetica", 18, "bold")
        )
        self.sessions_label.pack(pady=10)
        
        # Placeholder for sessions list
        self.sessions_list = ctk.CTkTextbox(
            self.sessions_frame,
            font=("Helvetica", 14),
            wrap="none"
        )
        self.sessions_list.pack(fill="both", expand=True, padx=10, pady=10)
        self.sessions_list.insert("1.0", "No recent sessions")
        self.sessions_list.configure(state="disabled")
    
    def open_new_session(self):
        session_window = SessionWindow(self)
        self.wait_window(session_window)
        # TODO: Refresh sessions list after window closes
    
    def open_statistics(self):
        # TODO: Implement statistics window
        pass

