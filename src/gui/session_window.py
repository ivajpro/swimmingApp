import customtkinter as ctk
from datetime import datetime
from .components.set_dialog import SetDialog

class SessionWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("New Swimming Session")
        self.geometry("600x800")
        self.resizable(False, False)
        
        # Initialize variables
        self.sets = []
        self.parent = parent
        
        self.setup_ui()
        self.grab_set()  # Make window modal
    
    def setup_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Basic info frame
        self.info_frame = ctk.CTkFrame(self.main_frame)
        self.info_frame.pack(fill="x", pady=(0, 20))
        
        # Date selector
        self.date_label = ctk.CTkLabel(self.info_frame, text="Date:")
        self.date_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.date_entry = ctk.CTkEntry(
            self.info_frame, 
            placeholder_text=datetime.now().strftime("%Y-%m-%d")
        )
        self.date_entry.pack(fill="x", padx=10, pady=(0, 10))
        
        # Pool length selector
        self.pool_label = ctk.CTkLabel(self.info_frame, text="Pool Length:")
        self.pool_label.pack(anchor="w", padx=10, pady=(10, 0))
        
        self.pool_var = ctk.StringVar(value="25")
        self.pool_selector = ctk.CTkSegmentedButton(
            self.info_frame,
            values=["25m", "50m"],
            variable=self.pool_var
        )
        self.pool_selector.pack(padx=10, pady=(0, 10))
        
        # Sets frame
        self.sets_frame = ctk.CTkFrame(self.main_frame)
        self.sets_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Sets label
        self.sets_label = ctk.CTkLabel(
            self.sets_frame,
            text="Swimming Sets",
            font=("Helvetica", 16, "bold")
        )
        self.sets_label.pack(pady=10)
        
        # Add scrollable frame for sets
        self.sets_container = ctk.CTkScrollableFrame(
            self.sets_frame,
            height=300
        )
        self.sets_container.pack(fill="x", padx=10, pady=(0, 10))
        
        # Add set button
        self.add_set_btn = ctk.CTkButton(
            self.sets_frame,
            text="Add Set",
            command=self.add_set
        )
        self.add_set_btn.pack(pady=10)
        
        # Notes
        self.notes_label = ctk.CTkLabel(self.main_frame, text="Notes:")
        self.notes_label.pack(anchor="w", padx=10)
        
        self.notes_text = ctk.CTkTextbox(
            self.main_frame,
            height=100
        )
        self.notes_text.pack(fill="x", padx=10, pady=(0, 20))
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.pack(fill="x", pady=(0, 10))
        
        self.save_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Save Session",
            command=self.save_session
        )
        self.save_btn.pack(side="right", padx=10)
        
        self.cancel_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Cancel",
            command=self.destroy
        )
        self.cancel_btn.pack(side="right", padx=10)
    
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
        
        # Add sets
        for i, set_data in enumerate(self.sets, 1):
            set_frame = ctk.CTkFrame(self.sets_container)
            set_frame.pack(fill="x", padx=5, pady=2)
            
            label_text = (f"Set {i}: {set_data['distance']}m "
                         f"({set_data['stroke']}) - "
                         f"{set_data['time']}s "
                         f"Rest: {set_data['rest']}s")
            
            set_label = ctk.CTkLabel(
                set_frame,
                text=label_text
            )
            set_label.pack(side="left", padx=5, pady=5)
            
            delete_btn = ctk.CTkButton(
                set_frame,
                text="×",
                width=30,
                command=lambda idx=i-1: self.delete_set(idx)
            )
            delete_btn.pack(side="right", padx=5, pady=5)
    
    def delete_set(self, index):
        del self.sets[index]
        self.update_sets_display()
    
    def save_session(self):
        # TODO: Implement save functionality
        pass

