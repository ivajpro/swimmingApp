import customtkinter as ctk

class SetDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Swimming Set")
        self.geometry("400x600")
        self.minsize(300, 400)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main scrollable container
        self.main_scroll = ctk.CTkScrollableFrame(self)
        self.main_scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.main_scroll.grid_columnconfigure(0, weight=1)
        
        # Bottom buttons frame (outside scrollable area)
        self.buttons_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.buttons_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=5)
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Add buttons
        self.cancel_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Cancel",
            command=self.cancel,
            width=120
        )
        self.cancel_btn.grid(row=0, column=0, padx=5, pady=10)
        
        self.save_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Add Set",
            command=self.save,
            width=120
        )
        self.save_btn.grid(row=0, column=1, padx=5, pady=10)
        
        # Initialize result
        self.result = None
        
        self.setup_ui()
        self.grab_set()
    
    def setup_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self.main_scroll)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Add repetitions input before distance
        self.reps_label = ctk.CTkLabel(
            self.main_frame,
            text="Repetitions:",
            font=("Helvetica", 14)
        )
        self.reps_label.grid(row=0, column=0, sticky="w", padx=10, pady=(10, 0))
        
        self.reps_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Number of repetitions (e.g., 4)",
            width=120
        )
        self.reps_entry.grid(row=1, column=0, sticky="w", padx=10, pady=(0, 15))
        self.reps_entry.insert(0, "1")  # Default value
        
        # Distance input (mandatory)
        self.distance_label = ctk.CTkLabel(
            self.main_frame, 
            text="Distance per repetition (meters) *:",  # Updated label
            font=("Helvetica", 14)
        )
        self.distance_label.grid(row=2, column=0, sticky="w", padx=10, pady=(0, 5))
        
        self.distance_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter distance (required)"
        )
        self.distance_entry.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 15))
        
        # Time input (optional)
        self.time_label = ctk.CTkLabel(
            self.main_frame,
            text="Time (seconds) (optional):",
            font=("Helvetica", 14)
        )
        self.time_label.grid(row=4, column=0, sticky="w", padx=10, pady=(0, 5))
        
        self.time_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter time (optional)"
        )
        self.time_entry.grid(row=5, column=0, sticky="ew", padx=10, pady=(0, 15))
        
        # Stroke selector
        self.stroke_label = ctk.CTkLabel(
            self.main_frame,
            text="Stroke:"
        )
        self.stroke_label.grid(row=6, column=0, sticky="w", padx=10, pady=(0, 5))
        
        self.stroke_var = ctk.StringVar(value="freestyle")
        self.stroke_selector = ctk.CTkSegmentedButton(
            self.main_frame,
            values=["freestyle", "backstroke", "breaststroke", "butterfly"],
            variable=self.stroke_var
        )
        self.stroke_selector.grid(row=7, column=0, sticky="ew", padx=10, pady=(0, 15))
        
        # Rest interval (optional)
        self.rest_label = ctk.CTkLabel(
            self.main_frame,
            text="Rest Interval (seconds) (optional):",
            font=("Helvetica", 14)
        )
        self.rest_label.grid(row=8, column=0, sticky="w", padx=10, pady=(0, 5))
        
        self.rest_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter rest interval (optional)"
        )
        self.rest_entry.grid(row=9, column=0, sticky="ew", padx=10, pady=(0, 20))
        
        # Add description field before buttons
        self.description_label = ctk.CTkLabel(
            self.main_frame,
            text="Set Description (optional):",
            font=("Helvetica", 14)
        )
        self.description_label.grid(row=10, column=0, sticky="w", padx=10, pady=(10, 0))
        
        self.description_entry = ctk.CTkTextbox(
            self.main_frame,
            height=60,
            width=300
        )
        self.description_entry.grid(row=11, column=0, sticky="ew", padx=10, pady=(0, 15))
    
    def validate_inputs(self) -> tuple[bool, str]:
        """Validate all input fields"""
        try:
            # Validate repetitions
            reps = int(self.reps_entry.get())
            if reps <= 0:
                return False, "Repetitions must be greater than 0"
            
            # Validate distance
            distance = int(self.distance_entry.get())
            if distance <= 0:
                return False, "Distance must be greater than 0"
            
            # Validate time if provided
            time_str = self.time_entry.get()
            if time_str:
                time = int(time_str)
                if time <= 0:
                    return False, "Time must be greater than 0"
            
            # Validate rest interval if provided
            rest_str = self.rest_entry.get()
            if rest_str:
                rest = int(rest_str)
                if rest < 0:
                    return False, "Rest interval cannot be negative"
            
            return True, ""
            
        except ValueError:
            return False, "Please enter valid numbers"

    def save(self):
        # Validate inputs before saving
        is_valid, error_message = self.validate_inputs()
        if not is_valid:
            self._show_error(error_message)
            return
        
        try:
            # Get and validate repetitions
            reps = int(self.reps_entry.get())
            if reps <= 0:
                self._show_error("Repetitions must be greater than 0")
                return
                
            # Get and validate distance (per repetition)
            distance = int(self.distance_entry.get())
            if distance <= 0:
                self._show_error("Distance must be greater than 0")
                return
            
            # Get time (per repetition, optional)
            time_str = self.time_entry.get()
            time = int(time_str) if time_str else 0
            
            # Get rest interval (optional)
            rest_str = self.rest_entry.get()
            rest = int(rest_str) if rest_str else 0
            
            self.result = {
                "distance": distance,
                "time": time,
                "stroke": self.stroke_var.get(),
                "repetitions": reps,
                "rest": rest,
                "description": self.description_entry.get("1.0", "end-1c").strip()
            }
            self.destroy()
            
        except ValueError:
            self._show_error("Please enter valid numbers")
    
    def cancel(self):
        self.result = None
        self.destroy()
    
    def _show_error(self, message: str):
        error_label = ctk.CTkLabel(
            self.main_frame,
            text=message,
            text_color="red"
        )
        error_label.grid(row=13, column=0, pady=(0, 10))
        self.after(2000, error_label.destroy())