import customtkinter as ctk

class SetDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Set")
        self.geometry("400x600")
        self.minsize(300, 400)
        
        # Initialize variables
        self.result = None
        self.distance_var = ctk.StringVar(value="")
        self.reps_var = ctk.StringVar(value="1")
        self.strokes = ["freestyle", "backstroke", "breaststroke", "butterfly", "mix"]
        self.stroke_var = ctk.StringVar(value=self.strokes[0])
        
        # Initialize mixed strokes
        self.mixed_strokes = {
            "freestyle": ctk.BooleanVar(value=False),
            "backstroke": ctk.BooleanVar(value=False),
            "breaststroke": ctk.BooleanVar(value=False),
            "butterfly": ctk.BooleanVar(value=False)
        }
        
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
            textvariable=self.reps_var,
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
            textvariable=self.distance_var,
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
        
        self.stroke_selector = ctk.CTkOptionMenu(
            self.main_frame,
            variable=self.stroke_var,
            values=self.strokes,
            command=self.on_stroke_change
        )
        self.stroke_selector.grid(row=7, column=0, sticky="ew", padx=10, pady=(0, 15))
        
        # Mixed strokes frame (initially hidden)
        self.mix_frame = ctk.CTkFrame(self.main_frame)
        for stroke, var in self.mixed_strokes.items():
            ctk.CTkCheckBox(
                self.mix_frame,
                text=stroke.capitalize(),
                variable=var
            ).grid(sticky="w", padx=10, pady=2)
        
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
    
    def on_stroke_change(self, choice):
        if choice == "mix":
            self.mix_frame.grid(row=12, column=0, sticky="ew", padx=10, pady=10)
        else:
            self.mix_frame.grid_forget()
    
    def get_result(self) -> dict:
        """Get the set data with validation"""
        try:
            distance = int(self.distance_var.get())
            reps = int(self.reps_var.get())
            
            if distance <= 0:
                raise ValueError("Distance must be greater than 0")
            if reps <= 0:
                raise ValueError("Repetitions must be greater than 0")
            
            result = {
                "distance": distance,
                "repetitions": reps,
                "stroke": self.stroke_var.get()
            }
            
            if result["stroke"] == "mix":
                selected_strokes = [
                    stroke for stroke, var in self.mixed_strokes.items()
                    if var.get()
                ]
                if not selected_strokes:
                    raise ValueError("Please select at least one stroke for mix")
                result["mixed_strokes"] = selected_strokes
            
            return result
            
        except ValueError as e:
            raise ValueError(str(e))
    
    def save(self):
        """Save button handler"""
        try:
            self.result = self.get_result()
            self.destroy()
        except ValueError as e:
            self._show_error(str(e))
    
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