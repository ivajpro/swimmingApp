import customtkinter as ctk

class SessionWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("New Session")
        self.geometry("600x400")

