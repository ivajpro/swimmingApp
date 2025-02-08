import customtkinter as ctk
from datetime import datetime
from src.gui.session_window import SessionWindow  # Update to absolute import
from src.utils.database import Database

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Initialize window properties
        self.title("Swimming Training Tracker")
        self.geometry("800x600")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Setup UI components
        self.setup_ui()
        
        # Initialize sessions list
        self.refresh_sessions_list()
    
    def setup_ui(self):
        """Setup all UI components"""
        # Buttons frame with center alignment
        self.buttons_frame = ctk.CTkFrame(self.main_frame)
        self.buttons_frame.pack(fill="x", pady=10)
        
        # Configure grid columns for centering
        self.buttons_frame.grid_columnconfigure(0, weight=1)  # Left padding
        self.buttons_frame.grid_columnconfigure(4, weight=1)  # Right padding
        
        # Add new session button
        self.new_session_btn = ctk.CTkButton(
            self.buttons_frame,
            text="New Session",
            font=("Helvetica", 14),
            width=200,
            height=40,
            command=self.open_new_session
        )
        self.new_session_btn.grid(row=0, column=1, padx=10, pady=10)
        
        # Add view stats button
        self.view_stats_btn = ctk.CTkButton(
            self.buttons_frame,
            text="View Stats",
            font=("Helvetica", 14),
            width=200,
            height=40,
            command=self.open_statistics
        )
        self.view_stats_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Add export button
        self.export_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Export Data",
            font=("Helvetica", 14),
            width=200,
            height=40,
            command=self.export_data
        )
        self.export_btn.grid(row=0, column=3, padx=10, pady=10)
        
        # Sessions frame
        self.sessions_frame = ctk.CTkFrame(self.main_frame)
        self.sessions_frame.pack(fill="both", expand=True, pady=20)
        
        # Sessions title
        self.sessions_label = ctk.CTkLabel(
            self.sessions_frame,
            text="Recent Sessions",
            font=("Helvetica", 18, "bold")
        )
        self.sessions_label.pack(pady=10)
        
        # Sessions container for scrollable content
        self.sessions_container = ctk.CTkFrame(self.sessions_frame)
        self.sessions_container.pack(fill="both", expand=True, padx=10, pady=10)
    
    def open_new_session(self):
        session_window = SessionWindow(self)
        self.wait_window(session_window)
        self.refresh_sessions_list()  # Refresh after window closes
    
    def open_statistics(self):
        from src.gui.stats_window import StatsWindow
        stats_window = StatsWindow(self)
        self.wait_window(stats_window)

    def refresh_sessions_list(self):
        """Refresh the sessions list display"""
        # Clear existing sessions
        for widget in self.sessions_container.winfo_children():
            widget.destroy()
        
        # Get sessions from database
        db = Database()
        sessions = db.get_sessions()
        
        if not sessions:
            # Show message when no sessions exist
            no_sessions_label = ctk.CTkLabel(
                self.sessions_container,
                text="No sessions yet. Click 'New Session' to add one.",
                font=("Helvetica", 14)
            )
            no_sessions_label.pack(pady=20)
            return
        
        # Display sessions
        for session in sessions:
            session_frame = ctk.CTkFrame(self.sessions_container)
            session_frame.pack(fill="x", pady=5)
            
            # Session info
            info_text = f"Date: {session['date']} - {session.get('description', 'No description')}"
            info_label = ctk.CTkLabel(
                session_frame,
                text=info_text,
                font=("Helvetica", 12)
            )
            info_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)
            
            # Delete button
            delete_btn = ctk.CTkButton(
                session_frame,
                text="×",
                width=30,
                fg_color="red",
                hover_color="darkred",
                command=lambda sid=session.get('id'): self.delete_session(sid)
            )
            delete_btn.grid(row=0, column=1, padx=5, pady=5)
            
            # Make session frame clickable for editing
            session_frame.bind("<Button-1>", 
                lambda e, s=session: self.edit_session(s))
    
    def edit_session(self, session):
        """Open session for editing"""
        edit_window = SessionWindow(self, session=session)
        self.wait_window(edit_window)
        self.refresh_sessions_list()

    def delete_session(self, session_id):
        """Delete a session"""
        from tkinter import messagebox
        
        if messagebox.askyesno("Delete Session", "Are you sure you want to delete this session?"):
            db = Database()
            if db.delete_session(session_id):
                self.refresh_sessions_list()

    def export_data(self):
        """Export sessions data to CSV file"""
        from tkinter import filedialog
        import csv
        from datetime import datetime
        
        # Get save file location
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
            initialfile=f"swimming_sessions_{datetime.now().strftime('%Y%m%d')}"
        )
        
        if filename:
            try:
                db = Database()
                sessions = db.get_sessions()
                
                if not sessions:
                    return
                
                # Sort sessions by date
                sessions.sort(key=lambda x: x.get("date", ""), reverse=True)
                
                # Define CSV headers
                fieldnames = [
                    "date", "pool_length", "total_distance", 
                    "total_time", "sets", "notes"
                ]
                
                with open(filename, 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    for session in sessions:
                        # Clean up data for CSV export
                        export_data = {
                            "date": session.get("date", ""),
                            "pool_length": session.get("pool_length", 0),
                            "total_distance": session.get("total_distance", 0),
                            "total_time": session.get("total_time", 0),
                            "sets": str(session.get("sets", [])),
                            "notes": session.get("notes", "").replace("\n", " ")
                        }
                        writer.writerow(export_data)
                
                # Show success message in sessions list
                self.sessions_list.configure(state="normal")
                self.sessions_list.insert("1.0", f"Data exported to {filename}\n{'-' * 40}\n\n")
                self.sessions_list.configure(state="disabled")
                
            except Exception as e:
                # Show error message in sessions list
                self.sessions_list.configure(state="normal")
                self.sessions_list.insert("1.0", f"Error exporting data: {str(e)}\n{'-' * 40}\n\n")
                self.sessions_list.configure(state="disabled")

