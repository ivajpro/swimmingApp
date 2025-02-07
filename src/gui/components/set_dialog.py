import customtkinter as ctk

class SetDialog(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Swimming Set")
        self.geometry("400x500")
        self.resizable(False, False)
        
        self.result = None
        self.setup_ui()
        self.grab_set()
    
    def setup_ui(self):
        # Main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Distance input
        self.distance_label = ctk.CTkLabel(self.main_frame, text="Distance (meters):")
        self.distance_label.pack(anchor="w", pady=(0, 5))
        
        self.distance_entry = ctk.CTkEntry(self.main_frame)
        self.distance_entry.pack(fill="x", pady=(0, 15))
        
        # Time input
        self.time_label = ctk.CTkLabel(self.main_frame, text="Time (seconds):")
        self.time_label.pack(anchor="w", pady=(0, 5))
        
        self.time_entry = ctk.CTkEntry(self.main_frame)
        self.time_entry.pack(fill="x", pady=(0, 15))
        
        # Stroke selector
        self.stroke_label = ctk.CTkLabel(self.main_frame, text="Stroke:")
        self.stroke_label.pack(anchor="w", pady=(0, 5))
        
        self.stroke_var = ctk.StringVar(value="freestyle")
        self.stroke_selector = ctk.CTkSegmentedButton(
            self.main_frame,
            values=["freestyle", "backstroke", "breaststroke", "butterfly"],
            variable=self.stroke_var
        )
        self.stroke_selector.pack(fill="x", pady=(0, 15))
        
        # Rest interval
        self.rest_label = ctk.CTkLabel(self.main_frame, text="Rest Interval (seconds):")
        self.rest_label.pack(anchor="w", pady=(0, 5))
        
        self.rest_entry = ctk.CTkEntry(self.main_frame)
        self.rest_entry.pack(fill="x", pady=(0, 20))
        
        # Buttons
        self.button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.button_frame.pack(fill="x")
        
        self.cancel_btn = ctk.CTkButton(
            self.button_frame,
            text="Cancel",
            command=self.cancel
        )
        self.cancel_btn.pack(side="left", padx=5, expand=True)
        
        self.save_btn = ctk.CTkButton(
            self.button_frame,
            text="Add Set",
            command=self.save
        )
        self.save_btn.pack(side="left", padx=5, expand=True)
    
    def save(self):
        try:
            self.result = {
                "distance": int(self.distance_entry.get()),
                "time": int(self.time_entry.get()),
                "stroke": self.stroke_var.get(),
                "rest": int(self.rest_entry.get() or 0)
            }
            self.destroy()
        except ValueError:
            # Show error message
            error = ctk.CTkLabel(
                self.main_frame,
                text="Please enter valid numbers",
                text_color="red"
            )
            error.pack(before=self.button_frame)
            self.after(2000, error.destroy)
    
    def cancel(self):
        self.result = None
        self.destroy()