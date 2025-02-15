import customtkinter as ctk
from datetime import datetime
from .components.set_dialog import SetDialog
from src.utils.database import Database

class SessionWindow(ctk.CTkToplevel):
    def __init__(self, parent, session=None):
        super().__init__(parent)
        self.title("Edit Session" if session else "New Swimming Session")
        self.geometry("600x800")
        self.minsize(500, 600)
        
        # Configure main window grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main scrollable container
        self.main_scroll = ctk.CTkScrollableFrame(self)
        self.main_scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_scroll.grid_columnconfigure(0, weight=1)
        
        # Store session data if editing
        self.editing_session = session
        
        # Initialize variables
        self.sets = session.get('sets', []) if session else []
        self.parent = parent
        
        self.setup_ui()
        
        # Fill form if editing
        if session:
            self.date_entry.insert(0, session.get('date', ''))
            self.pool_var.set(f"{session.get('pool_length', 25)}m")
            self.notes_text.insert("1.0", session.get('notes', ''))
            self.update_sets_display()
        
        self.grab_set()  # Make window modal
    
    def setup_ui(self):
        # Main container with grid (now inside scrollable frame)
        self.main_frame = ctk.CTkFrame(self.main_scroll)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
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
        
        # Sets frame with fixed height
        self.sets_frame = ctk.CTkFrame(self.main_frame)
        self.sets_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 20))
        self.sets_frame.grid_columnconfigure(0, weight=1)
        
        # Sets label
        self.sets_label = ctk.CTkLabel(
            self.sets_frame,
            text="Swimming Sets",
            font=("Helvetica", 16, "bold")
        )
        self.sets_label.grid(row=0, column=0, pady=10)
        
        # Create container frame for sets
        self.sets_container = ctk.CTkFrame(self.sets_frame)
        self.sets_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))
        self.sets_container.grid_columnconfigure(0, weight=1)

        # Add set button below container
        self.add_set_btn = ctk.CTkButton(
            self.sets_frame,
            text="➕ Add Set",
            command=self.add_set,
            width=200
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
        """Update the sets display"""
        # Clear existing sets
        for widget in self.sets_container.winfo_children():
            widget.destroy()
        
        # Check for empty sets list
        if not self.sets:
            # Show empty state
            empty_label = ctk.CTkLabel(
                self.sets_container,
                text="No sets added yet",
                text_color="gray"
            )
            empty_label.pack(pady=20)
            return
        
        # Display sets
        for i, set_data in enumerate(self.sets, 1):
            set_frame = ctk.CTkFrame(
                self.sets_container,
                fg_color=("gray95", "gray20")
            )
            set_frame.pack(fill="x", pady=5, padx=5)
            
            # Set info
            label_text = f"Set {i}: {set_data['repetitions']}x{set_data['distance']}m ({set_data['stroke']})"
            if set_data.get('description'):
                label_text += f"\n{set_data['description']}"
            
            info_frame = ctk.CTkFrame(
                set_frame,
                fg_color="transparent"
            )
            info_frame.pack(fill="x", expand=True, side="left", padx=10, pady=5)
            
            set_label = ctk.CTkLabel(
                info_frame,
                text=label_text,
                font=("Helvetica", 12),
                justify="left"
            )
            set_label.pack(anchor="w")
            
            # Buttons frame
            buttons_frame = ctk.CTkFrame(
                set_frame,
                fg_color="transparent"
            )
            buttons_frame.pack(side="right", padx=5, pady=5)
            
            # Edit button
            edit_btn = ctk.CTkButton(
                buttons_frame,
                text="✎",
                width=30,
                height=25,
                command=lambda idx=i-1: self.edit_set(idx)
            )
            edit_btn.pack(side="left", padx=2)
            
            # Delete button
            delete_btn = ctk.CTkButton(
                buttons_frame,
                text="×",
                width=30,
                height=25,
                command=lambda idx=i-1: self.delete_set(idx),
                fg_color="red",
                hover_color="darkred"
            )
            delete_btn.pack(side="left", padx=2)
    
    def delete_set(self, index):
        del self.sets[index]
        self.update_sets_display()
    
    def edit_set(self, index):
        """Edit an existing set"""
        current_set = self.sets[index]
        dialog = SetDialog(self, edit_data=current_set)  # Pass existing set data
        self.wait_window(dialog)
        
        if dialog.result:
            self.sets[index] = dialog.result  # Replace the set with edited data
            self.update_sets_display()
    
    def save_session(self):
        """Save new or update existing session"""
        try:
            # Validate if there are any sets
            if not self.sets:
                self._show_error("Please add at least one set")
                return
            
            # Get pool length (remove 'm' from the string)
            pool_length = int(self.pool_var.get().replace('m', ''))
            
            # Create session data with correct total distance calculation
            session_data = {
                "date": self.date_entry.get() or datetime.now().strftime("%Y-%m-%d"),
                "pool_length": pool_length,
                "sets": self.sets,
                "total_distance": sum(
                    set_data["distance"] * set_data.get("repetitions", 1) 
                    for set_data in self.sets
                ),
                "total_time": sum(
                    set_data["time"] * set_data.get("repetitions", 1) 
                    for set_data in self.sets
                ) if all(set_data.get("time") for set_data in self.sets) else 0,
                "notes": self.notes_text.get("1.0", "end-1c").strip()
            }
            
            # Save to database
            db = Database()
            if self.editing_session:
                session_data['id'] = self.editing_session['id']
                success = db.update_session(session_data)
            else:
                success = db.save_session(session_data)
            
            if success:
                self.destroy()  # Close window on successful save
            else:
                self._show_error("Failed to save session")
                
        except Exception as e:
            self._show_error(f"Error saving session: {str(e)}")

    def _show_error(self, message: str):
        """Display error message to user"""
        error_label = ctk.CTkLabel(
            self.main_frame,
            text=message,
            text_color="red",
            font=("Helvetica", 12)
        )
        error_label.grid(row=5, column=0, pady=(0, 10))
        self.after(2000, error_label.destroy)

