import customtkinter as ctk
from datetime import datetime

class SessionWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        # Configure window
        self.title("New Swimming Session")
        self.geometry("600x800")
        self.resizable(False, False)
        
        # Create main container
        self.setup_ui()
        
        # Make window modal
        self.grab_set()
        
    def setup_ui(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Session details frame
        self.details_frame = ctk.CTkFrame(self.main_frame)
        self.details_frame.pack(fill="x", padx=10, pady=10)
        
        # Date picker
        self.date_label = ctk.CTkLabel(
            self.details_frame, 
            text="Date:",
            font=("Helvetica", 14)
        )
        self.date_label.pack(anchor="w", padx=5, pady=5)
        
        self.date_entry = ctk.CTkEntry(
            self.details_frame,
            placeholder_text=datetime.now().strftime("%Y-%m-%d")
        )
        self.date_entry.pack(fill="x", padx=5, pady=5)
        
        # Pool length selector
        self.pool_label = ctk.CTkLabel(
            self.details_frame,
            text="Pool Length:",
            font=("Helvetica", 14)
        )
        self.pool_label.pack(anchor="w", padx=5, pady=5)
        
        self.pool_var = ctk.StringVar(value="25")
        self.pool_length = ctk.CTkSegmentedButton(
            self.details_frame,
            values=["25", "50"],
            variable=self.pool_var
        )
        self.pool_length.pack(padx=5, pady=5)
        
        # Add set button
        self.add_set_btn = ctk.CTkButton(
            self.details_frame,
            text="Add Set",
            command=self.add_set
        )
        self.add_set_btn.pack(pady=10)
        
        # Sets frame
        self.sets_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            label_text="Swimming Sets",
            height=400
        )
        self.sets_frame.pack(fill="x", padx=10, pady=10)
        
        # Notes
        self.notes_label = ctk.CTkLabel(
            self.main_frame,
            text="Notes:",
            font=("Helvetica", 14)
        )
        self.notes_label.pack(anchor="w", padx=15, pady=5)
        
        self.notes_text = ctk.CTkTextbox(
            self.main_frame,
            height=100
        )
        self.notes_text.pack(fill="x", padx=15, pady=5)
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.pack(fill="x", pady=20)
        
        self.save_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Save Session",
            command=self.save_session
        )
        self.save_btn.pack(side="right", padx=5)
        
        self.cancel_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Cancel",
            command=self.destroy
        )
        self.cancel_btn.pack(side="right", padx=5)
    
    def add_set(self):
        # TODO: Implement add set functionality
        pass
    
    def save_session(self):
        # TODO: Implement save functionality
        pass

