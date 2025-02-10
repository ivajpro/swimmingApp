import customtkinter as ctk
from datetime import datetime
from src.gui.session_window import SessionWindow  # Update to absolute import
from src.utils.database import Database

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Enhanced window properties
        self.title("🏊 Swimming Training Tracker")
        self.geometry("1000x700")  # Larger default size
        self.minsize(800, 600)
        
        # Create main container with padding
        self.main_container = ctk.CTkFrame(self)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Add title section
        self.setup_title()
        self.setup_ui()
        self.refresh_sessions_list()

    def setup_title(self):
        """Setup app title and header section"""
        title_frame = ctk.CTkFrame(self.main_container)
        title_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="Swimming Training Tracker",
            font=("Helvetica", 24, "bold"),
        )
        title_label.pack(pady=10)
        
        subtitle_label = ctk.CTkLabel(
            title_frame,
            text="Track your swimming progress and analyze your performance",
            font=("Helvetica", 14),
            text_color="gray"
        )
        subtitle_label.pack(pady=(0, 10))

    def setup_ui(self):
        """Setup enhanced UI components"""
        # Buttons frame with modern styling and glass effect
        self.buttons_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=("gray85", "gray25"),
            corner_radius=15
        )
        self.buttons_frame.pack(fill="x", pady=(0, 20))
        
        # Grid configuration for centering
        self.buttons_frame.grid_columnconfigure((0, 4), weight=1)
        
        # Enhanced button styles
        button_hover_color = ("gray75", "gray35")
        button_style = {
            "font": ("Helvetica", 14, "bold"),
            "width": 200,
            "height": 45,
            "corner_radius": 12,
            "border_width": 2,
            "border_color": ("gray70", "gray40"),
            "hover_color": button_hover_color
        }
        
        # New Session Button with enhanced styling
        self.new_session_btn = ctk.CTkButton(
            self.buttons_frame,
            text="➕ New Session",
            fg_color=("gray80", "gray30"),
            **button_style,
            command=self.open_new_session
        )
        self.new_session_btn.grid(row=0, column=1, padx=15, pady=15)
        
        # Statistics Button with icon
        self.view_stats_btn = ctk.CTkButton(
            self.buttons_frame,
            text="📊 Statistics",
            font=("Helvetica", 14, "bold"),
            width=200,
            height=40,
            corner_radius=10,
            command=self.open_statistics
        )
        self.view_stats_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Export Button with icon
        self.export_btn = ctk.CTkButton(
            self.buttons_frame,
            text="📥 Export Data",
            font=("Helvetica", 14, "bold"),
            width=200,
            height=40,
            corner_radius=10,
            command=self.export_data
        )
        self.export_btn.grid(row=0, column=3, padx=10, pady=10)
        
        # Enhanced Sessions Frame
        self.sessions_frame = ctk.CTkFrame(self.main_container)
        self.sessions_frame.pack(fill="both", expand=True)
        
        # Sessions Header with Search
        self.setup_sessions_header()
        
        # Scrollable Sessions Container
        self.setup_scrollable_sessions()

    def setup_sessions_header(self):
        """Setup enhanced sessions header with search"""
        header_frame = ctk.CTkFrame(self.sessions_frame)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Title with icon
        title_label = ctk.CTkLabel(
            header_frame,
            text="🏊 Recent Sessions",
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(side="left", padx=10)
        
        # Search frame (for future implementation)
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.pack(side="right", padx=10)
        
        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search sessions...",
            width=200
        )
        self.search_entry.pack(side="left", padx=5)

    def setup_scrollable_sessions(self):
        """Setup enhanced scrollable sessions container"""
        # Create scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            self.sessions_frame,
            label_text="",
            corner_radius=0
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Session container
        self.sessions_container = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="transparent"
        )
        self.sessions_container.pack(fill="both", expand=True)
    
    def open_new_session(self):
        session_window = SessionWindow(self)
        self.wait_window(session_window)
        self.refresh_sessions_list()  # Refresh after window closes
    
    def open_statistics(self):
        from src.gui.stats_window import StatsWindow
        stats_window = StatsWindow(self)
        self.wait_window(stats_window)

    def refresh_sessions_list(self):
        """Refresh the sessions list with enhanced display"""
        # Clear existing sessions
        for widget in self.sessions_container.winfo_children():
            widget.destroy()
            
        db = Database()
        sessions = db.get_sessions()
        
        if not sessions:
            self.show_empty_state()
            return
        
        for session in sessions:
            # Create session card
            session_frame = ctk.CTkFrame(
                self.sessions_container,
                fg_color=("gray95", "gray20"),
                corner_radius=15
            )
            session_frame.pack(fill="x", pady=8, padx=10)
            
            # Header frame (date and buttons)
            header_frame = ctk.CTkFrame(session_frame, fg_color="transparent")
            header_frame.pack(fill="x", padx=15, pady=(10, 0))
            
            # Date and total info
            date_text = f"📅 {session['date']}"
            total_distance = f"🏊 {session['total_distance']}m total"
            total_sets = f"📝 {len(session['sets'])} sets"
            
            info_text = f"{date_text}  |  {total_distance}  |  {total_sets}"
            
            header_label = ctk.CTkLabel(
                header_frame,
                text=info_text,
                font=("Helvetica", 14, "bold")
            )
            header_label.pack(side="left")
            
            # Sets summary frame
            sets_frame = ctk.CTkFrame(session_frame, fg_color="transparent")
            sets_frame.pack(fill="x", padx=15, pady=(5, 10))
            
            # Display set summaries
            for i, set_data in enumerate(session['sets'], 1):
                set_text = f"Set {i}: {set_data['repetitions']}x{set_data['distance']}m ({set_data['stroke']})"
                if set_data.get('description'):
                    set_text += f" - {set_data['description']}"
                    
                set_label = ctk.CTkLabel(
                    sets_frame,
                    text=set_text,
                    font=("Helvetica", 12),
                    justify="left",
                    text_color=("gray40", "gray70")
                )
                set_label.pack(anchor="w", pady=2)
            
            # Actions frame
            actions_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            actions_frame.pack(side="right")
            
            # Edit button
            edit_btn = ctk.CTkButton(
                actions_frame,
                text="Edit",
                width=60,
                height=25,
                corner_radius=8,
                command=lambda s=session: self.edit_session(s)
            )
            edit_btn.pack(side="left", padx=2)
            
            # Delete button
            delete_btn = ctk.CTkButton(
                actions_frame,
                text="×",
                width=25,
                height=25,
                corner_radius=8,
                fg_color="red",
                hover_color="darkred",
                command=lambda sid=session.get('id'): self.delete_session(sid)
            )
            delete_btn.pack(side="left", padx=2)

    def edit_session(self, session):
        """Open session for editing"""
        edit_window = SessionWindow(self, session=session)
        self.wait_window(edit_window)
        self.refresh_sessions_list()

    def delete_session(self, session_id):
        """Delete a session with visual feedback"""
        from tkinter import messagebox
        import tkinter as tk
        
        def fade_out(frame, alpha=1.0):
            if alpha > 0:
                # Reduce opacity
                frame.configure(fg_color=(f"gray{int(95*alpha)}", f"gray{int(20*alpha)}"))
                self.after(20, lambda: fade_out(frame, alpha - 0.1))
            else:
                # Actually delete the session
                db = Database()
                if db.delete_session(session_id):
                    self.refresh_sessions_list()
        
        if messagebox.askyesno("Delete Session", "Are you sure you want to delete this session?"):
            # Find the session frame
            for widget in self.sessions_container.winfo_children():
                if hasattr(widget, 'session_id') and widget.session_id == session_id:
                    fade_out(widget)
                    break

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

    def show_empty_state(self):
        """Show enhanced empty state message"""
        no_sessions_frame = ctk.CTkFrame(
            self.sessions_container,
            fg_color=("gray95", "gray20"),
            corner_radius=15
        )
        no_sessions_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Swimming icon
        icon_label = ctk.CTkLabel(
            no_sessions_frame,
            text="🏊",
            font=("Helvetica", 48)
        )
        icon_label.pack(pady=(30, 10))
        
        # Title
        title_label = ctk.CTkLabel(
            no_sessions_frame,
            text="No Swimming Sessions Yet",
            font=("Helvetica", 20, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Description
        desc_label = ctk.CTkLabel(
            no_sessions_frame,
            text="Start tracking your swimming progress\nby adding your first session",
            font=("Helvetica", 14),
            text_color="gray"
        )
        desc_label.pack(pady=(0, 20))
        
        # Add session button
        ctk.CTkButton(
            no_sessions_frame,
            text="➕ Add First Session",
            command=self.open_new_session,
            width=200,
            height=40,
            corner_radius=12,
            hover_color=("gray75", "gray35")
        ).pack(pady=(0, 30))

