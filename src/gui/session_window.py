import customtkinter as ctk
from datetime import datetime
from .components.set_dialog import SetDialog
from src.utils.database import Database

class SessionWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("New Swimming Session")
        self.geometry("600x800")
        self.minsize(500, 600)  # Set minimum size
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Initialize variables
        self.sets = []
        self.parent = parent
        
        self.setup_ui()
        self.grab_set()  # Make window modal
    
    def setup_ui(self):
        # Main container with grid
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)  # Sets frame expands
        
        # Basic info frame
        self.info_frame = ctk.CTkFrame(self.main_frame)
        self.info_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.info_frame.grid_columnconfigure(0, weight=1)
        
        # Date selector
        self.date_label = ctk.CTkLabel(self.info_frame, text="Date:")
        self.date_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        
        self.date_entry = ctk.CTkEntry(
            self.info_frame, 
            placeholder_text=datetime.now().strftime("%Y-%m-%d")
        )
        self.date_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # Pool length selector
        self.pool_label = ctk.CTkLabel(self.info_frame, text="Pool Length:")
        self.pool_label.grid(row=2, column=0, sticky="w", padx=10, pady=(10, 0))
        
        self.pool_var = ctk.StringVar(value="25")
        self.pool_selector = ctk.CTkSegmentedButton(
            self.info_frame,
            values=["25m", "50m"],
            variable=self.pool_var
        )
        self.pool_selector.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 10))
        
        # Sets frame
        self.sets_frame = ctk.CTkFrame(self.main_frame)
        self.sets_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        self.sets_frame.grid_columnconfigure(0, weight=1)
        self.sets_frame.grid_rowconfigure(1, weight=1)  # Make scrollable frame expandable
        
        # Sets label
        self.sets_label = ctk.CTkLabel(
            self.sets_frame,
            text="Swimming Sets",
            font=("Helvetica", 16, "bold")
        )
        self.sets_label.grid(row=0, column=0, pady=10)
        
        # Add scrollable frame for sets
        self.sets_container = ctk.CTkScrollableFrame(
            self.sets_frame,
            height=300
        )
        self.sets_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        
        # Add set button
        self.add_set_btn = ctk.CTkButton(
            self.sets_frame,
            text="Add Set",
            command=self.add_set,
            width=200  # Set fixed width
        )
        self.add_set_btn.grid(row=2, column=0, pady=10)
        
        # Notes
        self.notes_label = ctk.CTkLabel(self.main_frame, text="Notes:")
        self.notes_label.grid(row=2, column=0, sticky="w", padx=10)
        
        self.notes_text = ctk.CTkTextbox(
            self.main_frame,
            height=100
        )
        self.notes_text.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 20))
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        self.buttons_frame.grid_columnconfigure(1, weight=1)  # Add this line
        
        # Change pack to grid for buttons
        self.cancel_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Cancel",
            command=self.destroy
        )
        self.cancel_btn.grid(row=0, column=0, padx=10)
        
        self.save_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Save Session",
            command=self.save_session
        )
        self.save_btn.grid(row=0, column=1, padx=10, sticky="e")
    
    def add_set(self):
        dialog = SetDialog(self)
        self.wait_window(dialog)
        
        if dialog.result:
            self.sets.append(dialog.result)
            self.update_sets_display()
    
    def update_sets_display(self):
        # Clear existing widgets
        for widget in self.sets_container.winfo_children():
            widget.destroy()
        
        # Change pack to grid for set display
        for i, set_data in enumerate(self.sets, 1):
            set_frame = ctk.CTkFrame(self.sets_container)
            set_frame.grid(row=i-1, column=0, sticky="ew", padx=5, pady=2)
            set_frame.grid_columnconfigure(0, weight=1)
            
            label_text = (f"Set {i}: {set_data['distance']}m "
                         f"({set_data['stroke']}) - "
                         f"{set_data['time']}s "
                         f"Rest: {set_data['rest']}s")
            
            set_label = ctk.CTkLabel(
                set_frame,
                text=label_text
            )
            set_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
            
            delete_btn = ctk.CTkButton(
                set_frame,
                text="×",
                width=30,
                command=lambda idx=i-1: self.delete_set(idx)
            )
            delete_btn.grid(row=0, column=1, padx=5, pady=5)
    
    def delete_set(self, index):
        del self.sets[index]
        self.update_sets_display()
    
    def save_session(self):
        """Save the current session"""
        try:
            # Validate inputs
            date_str = self.date_entry.get()
            if not date_str:
                date_str = datetime.now().strftime("%Y-%m-%d")
            
            pool_length = int(self.pool_var.get().replace("m", ""))
            
            if not self.sets:
                self._show_error("Please add at least one set")
                return
            
            # Create session data
            session_data = {
                "date": date_str,
                "pool_length": pool_length,
                "sets": self.sets,
                "notes": self.notes_text.get("1.0", "end-1c"),
                "total_distance": sum(set_data["distance"] for set_data in self.sets),
                "total_time": sum(set_data["time"] for set_data in self.sets),
            }
            
            # Save to database
            db = Database()
            if db.save_session(session_data):
                self.destroy()
            else:
                self._show_error("Failed to save session")
                
        except ValueError as e:
            self._show_error(str(e))
    
    def _show_error(self, message: str):
        """Show error message to user"""
        error_label = ctk.CTkLabel(
            self.main_frame,
            text=message,
            text_color="red"
        )
        error_label.pack(before=self.buttons_frame)
        self.after(2000, error_label.destroy)

