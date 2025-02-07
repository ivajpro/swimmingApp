import customtkinter as ctk

class SetDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Swimming Set")
        self.geometry("400x500")
        self.minsize(300, 400)
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Initialize result
        self.result = None
        
        self.setup_ui()
        self.grab_set()
    
    def setup_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Distance input (mandatory)
        self.distance_label = ctk.CTkLabel(
            self.main_frame, 
            text="Distance (meters) *:",  # Added asterisk to indicate required field
            font=("Helvetica", 14)
        )
        self.distance_label.grid(row=0, column=0, sticky="w", padx=10, pady=(0, 5))
        
        self.distance_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter distance (required)"
        )
        self.distance_entry.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 15))
        
        # Time input (optional)
        self.time_label = ctk.CTkLabel(
            self.main_frame,
            text="Time (seconds) (optional):",
            font=("Helvetica", 14)
        )
        self.time_label.grid(row=2, column=0, sticky="w", padx=10, pady=(0, 5))
        
        self.time_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter time (optional)"
        )
        self.time_entry.grid(row=3, column=0, sticky="ew", padx=10, pady=(0, 15))
        
        # Stroke selector
        self.stroke_label = ctk.CTkLabel(
            self.main_frame,
            text="Stroke:"
        )
        self.stroke_label.grid(row=4, column=0, sticky="w", padx=10, pady=(0, 5))
        
        self.stroke_var = ctk.StringVar(value="freestyle")
        self.stroke_selector = ctk.CTkSegmentedButton(
            self.main_frame,
            values=["freestyle", "backstroke", "breaststroke", "butterfly"],
            variable=self.stroke_var
        )
        self.stroke_selector.grid(row=5, column=0, sticky="ew", padx=10, pady=(0, 15))
        
        # Rest interval (optional)
        self.rest_label = ctk.CTkLabel(
            self.main_frame,
            text="Rest Interval (seconds) (optional):",
            font=("Helvetica", 14)
        )
        self.rest_label.grid(row=6, column=0, sticky="w", padx=10, pady=(0, 5))
        
        self.rest_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Enter rest interval (optional)"
        )
        self.rest_entry.grid(row=7, column=0, sticky="ew", padx=10, pady=(0, 20))
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.grid(row=8, column=0, sticky="ew", pady=(0, 10))
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.cancel_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Cancel",
            command=self.cancel
        )
        self.cancel_btn.grid(row=0, column=0, padx=5)
        
        self.save_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Add Set",
            command=self.save
        )
        self.save_btn.grid(row=0, column=1, padx=5)
    
    def save(self):
        # Get distance (mandatory)
        try:
            distance = int(self.distance_entry.get())
            if distance <= 0:
                self._show_error("Distance must be greater than 0")
                return
        except ValueError:
            self._show_error("Please enter a valid distance")
            return

        # Get time (optional)
        try:
            time_str = self.time_entry.get()
            time = int(time_str) if time_str else 0
        except ValueError:
            time = 0

        # Get rest interval (optional)
        try:
            rest_str = self.rest_entry.get()
            rest = int(rest_str) if rest_str else 0
        except ValueError:
            rest = 0

        self.result = {
            "distance": distance,
            "time": time,
            "stroke": self.stroke_var.get(),
            "rest": rest
        }
        self.destroy()
    
    def cancel(self):
        self.result = None
        self.destroy()
    
    def _show_error(self, message: str):
        error_label = ctk.CTkLabel(
            self.main_frame,
            text=message,
            text_color="red"
        )
        error_label.grid(row=9, column=0, pady=(0, 10))
        self.after(2000, error_label.destroy)