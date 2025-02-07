import customtkinter as ctk

class StatsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Statistics")
        self.geometry("800x600")

