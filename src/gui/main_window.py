import customtkinter as ctk
from datetime import datetime
from src.gui.session_window import SessionWindow  # Update to absolute import
from src.utils.database import Database

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Swimming Training Tracker")
        self.geometry("1024x768")
        self.minsize(800, 600)  # Set minimum window size
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Create main container
        self.setup_ui()
        
        # Load initial sessions
        self.refresh_sessions_list()
    
    def setup_ui(self):
        # Main frame with grid
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)  # Sessions frame expands
        
        # Title frame
        self.title_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.title_frame.grid_columnconfigure(1, weight=1)  # Space between title and date
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.title_frame,
            text="Swimming Training Tracker",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, padx=20)
        
        # Date display
        self.date_label = ctk.CTkLabel(
            self.title_frame,
            text=datetime.now().strftime("%d %B %Y"),
            font=("Helvetica", 16)
        )
        self.date_label.grid(row=0, column=2, padx=20)
        
        # Buttons frame
        self.buttons_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.buttons_frame.grid(row=1, column=0, sticky="ew", pady=20)
        self.buttons_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)  # Equal space distribution
        
        # Add main buttons
        self.new_session_btn = ctk.CTkButton(
            self.buttons_frame,
            text="New Session",
            font=("Helvetica", 14),
            width=200,
            height=40,
            command=self.open_new_session
        )
        self.new_session_btn.grid(row=0, column=0, padx=10)
        
        self.view_stats_btn = ctk.CTkButton(
            self.buttons_frame,
            text="View Statistics",
            font=("Helvetica", 14),
            width=200,
            height=40,
            command=self.open_statistics
        )
        self.view_stats_btn.grid(row=0, column=1, padx=10)
        
        # Add export button
        self.export_btn = ctk.CTkButton(
            self.buttons_frame,
            text="Export Data",
            font=("Helvetica", 14),
            width=200,
            height=40,
            command=self.export_data
        )
        self.export_btn.grid(row=0, column=2, padx=10)
        
        # Sessions frame
        self.sessions_frame = ctk.CTkFrame(self.main_frame)
        self.sessions_frame.grid(row=2, column=0, sticky="nsew", pady=20)
        self.sessions_frame.grid_columnconfigure(0, weight=1)
        self.sessions_frame.grid_rowconfigure(1, weight=1)  # Make list expandable
        
        # Sessions title
        self.sessions_label = ctk.CTkLabel(
            self.sessions_frame,
            text="Recent Sessions",
            font=("Helvetica", 18, "bold")
        )
        self.sessions_label.grid(row=0, column=0, pady=10)
        
        # Sessions list
        self.sessions_list = ctk.CTkTextbox(
            self.sessions_frame,
            font=("Helvetica", 14),
            wrap="none"
        )
        self.sessions_list.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        self.sessions_list.insert("1.0", "No recent sessions")
        self.sessions_list.configure(state="disabled")
    
    def open_new_session(self):
        session_window = SessionWindow(self)
        self.wait_window(session_window)
        self.refresh_sessions_list()  # Refresh after window closes
    
    def open_statistics(self):
        from src.gui.stats_window import StatsWindow
        stats_window = StatsWindow(self)
        self.wait_window(stats_window)

    def refresh_sessions_list(self):
        """Update the sessions list display"""
        self.sessions_list.configure(state="normal")
        self.sessions_list.delete("1.0", "end")
        
        db = Database()
        sessions = db.get_sessions()
        
        if not sessions:
            self.sessions_list.insert("1.0", "No recent sessions")
        else:
            # Clear existing frame contents
            self.sessions_list.pack_forget()
            
            # Create scrollable frame for sessions
            self.sessions_container = ctk.CTkScrollableFrame(
                self.sessions_frame,
                fg_color="transparent"
            )
            self.sessions_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
            self.sessions_container.grid_columnconfigure(0, weight=1)
            
            # Sort sessions by date, most recent first
            sessions.sort(key=lambda x: x.get("date", ""), reverse=True)
            
            for session in sessions:
                # Create frame for each session
                session_frame = ctk.CTkFrame(self.sessions_container)
                session_frame.grid(sticky="ew", pady=5, padx=5)
                session_frame.grid_columnconfigure(0, weight=1)
                
                # Session info
                info_text = (
                    f"Date: {session.get('date', 'No date')}\n"
                    f"Pool Length: {session.get('pool_length', 0)}m\n"
                    f"Total Distance: {session.get('total_distance', 0)}m\n"
                    f"Total Time: {session.get('total_time', 0)}s"
                )
                
                info_label = ctk.CTkLabel(
                    session_frame,
                    text=info_text,
                    font=("Helvetica", 14),
                    justify="left"
                )
                info_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")
                
                # Buttons frame
                buttons_frame = ctk.CTkFrame(session_frame, fg_color="transparent")
                buttons_frame.grid(row=0, column=1, padx=10, pady=5)
                
                # Edit button
                edit_btn = ctk.CTkButton(
                    buttons_frame,
                    text="Edit",
                    width=60,
                    command=lambda s=session: self.edit_session(s)
                )
                edit_btn.grid(row=0, column=0, padx=5)
                
                # Delete button
                delete_btn = ctk.CTkButton(
                    buttons_frame,
                    text="×",
                    width=30,
                    fg_color="red",
                    hover_color="darkred",
                    command=lambda s=session: self.delete_session(s)
                )
                delete_btn.grid(row=0, column=1, padx=5)

    def edit_session(self, session):
        """Open session for editing"""
        edit_window = SessionWindow(self, session=session)
        self.wait_window(edit_window)
        self.refresh_sessions_list()

    def delete_session(self, session):
        """Delete a session"""
        from tkinter import messagebox
        
        if messagebox.askyesno(
            "Delete Session",
            "Are you sure you want to delete this session?"
        ):
            db = Database()
            if db.delete_session(session['id']):
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

