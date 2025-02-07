import customtkinter as ctk
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from src.utils.database import Database

class StatsWindow(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Swimming Statistics")
        self.geometry("1000x800")
        self.minsize(800, 600)
        
        # Store reference to figure and canvas
        self.current_figure = None
        self.current_canvas = None
        
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)  # Make charts expandable
        
        self.setup_ui()
        self.calculate_stats()
        self.create_charts()
        self.grab_set()
        
        # Bind cleanup to window close
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        """Clean up resources when window is closed"""
        if self.current_figure:
            plt.close(self.current_figure)
        self.destroy()
    
    def setup_ui(self):
        # Main container
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="Swimming Statistics",
            font=("Helvetica", 24, "bold")
        )
        self.title_label.grid(row=0, column=0, pady=20)
        
        # Stats container
        self.stats_frame = ctk.CTkFrame(self.main_frame)
        self.stats_frame.grid(row=1, column=0, sticky="nsew", pady=10)
        self.stats_frame.grid_columnconfigure((0, 1), weight=1)
        
        # Labels for statistics (will be populated in calculate_stats)
        self.total_distance_label = ctk.CTkLabel(
            self.stats_frame,
            text="Total Distance: ",
            font=("Helvetica", 16)
        )
        self.total_distance_label.grid(row=0, column=0, pady=10, padx=20, sticky="w")
        
        self.total_sessions_label = ctk.CTkLabel(
            self.stats_frame,
            text="Total Sessions: ",
            font=("Helvetica", 16)
        )
        self.total_sessions_label.grid(row=1, column=0, pady=10, padx=20, sticky="w")
        
        self.avg_distance_label = ctk.CTkLabel(
            self.stats_frame,
            text="Average Distance per Session: ",
            font=("Helvetica", 16)
        )
        self.avg_distance_label.grid(row=2, column=0, pady=10, padx=20, sticky="w")
        
        self.avg_time_label = ctk.CTkLabel(
            self.stats_frame,
            text="Average Time per Session: ",
            font=("Helvetica", 16)
        )
        self.avg_time_label.grid(row=3, column=0, pady=10, padx=20, sticky="w")
        
        # Add charts frame
        self.charts_frame = ctk.CTkFrame(self.main_frame)
        self.charts_frame.grid(row=2, column=0, sticky="nsew", pady=10)
        self.charts_frame.grid_columnconfigure((0, 1), weight=1)
        self.charts_frame.grid_rowconfigure(0, weight=1)
        
        # Add chart controls
        self.controls_frame = ctk.CTkFrame(self.main_frame)
        self.controls_frame.grid(row=3, column=0, sticky="ew", pady=10)
        
        # Time range selector
        self.range_var = ctk.StringVar(value="all")
        self.range_selector = ctk.CTkSegmentedButton(
            self.controls_frame,
            values=["1w", "1m", "3m", "6m", "1y", "all"],
            variable=self.range_var,
            command=self.update_charts
        )
        self.range_selector.grid(row=0, column=0, padx=10, pady=5)
        
        # Export button
        self.export_btn = ctk.CTkButton(
            self.controls_frame,
            text="Export Data",
            command=self.export_data
        )
        self.export_btn.grid(row=0, column=1, padx=10, pady=5)
    
    def create_charts(self):
        if self.current_figure:
            plt.close(self.current_figure)
        
        db = Database()
        sessions = db.get_sessions()
        
        if not sessions:
            return
        
        # Sort sessions by date
        sessions.sort(key=lambda x: datetime.strptime(x.get("date", ""), "%Y-%m-%d"))
        
        # Prepare data
        dates = [datetime.strptime(s.get("date", ""), "%Y-%m-%d") for s in sessions]
        distances = [s.get("total_distance", 0) for s in sessions]
        times = [s.get("total_time", 0) for s in sessions]
        
        # Create figure with two subplots
        fig = plt.figure(figsize=(12, 5))
        
        # Distance over time plot
        ax1 = fig.add_subplot(121)
        ax1.plot(dates, distances, 'b-o')
        ax1.set_title('Distance Over Time')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Distance (m)')
        ax1.grid(True)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Time over distance scatter plot
        ax2 = fig.add_subplot(122)
        ax2.scatter(distances, times)
        ax2.set_title('Time vs Distance')
        ax2.set_xlabel('Distance (m)')
        ax2.set_ylabel('Time (s)')
        ax2.grid(True)
        
        # Adjust layout
        plt.tight_layout()
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, self.charts_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        self.current_figure = fig
        self.current_canvas = canvas
    
    def update_charts(self, time_range=None):
        """Update charts based on selected time range"""
        # Clear previous charts
        if self.current_figure:
            plt.close(self.current_figure)
        
        for widget in self.charts_frame.winfo_children():
            widget.destroy()
            
        db = Database()
        sessions = db.get_sessions()
        
        if not sessions:
            return
            
        # Filter sessions based on time range
        if time_range and time_range != "all":
            current_date = datetime.now()
            range_days = {
                "1w": 7,
                "1m": 30,
                "3m": 90,
                "6m": 180,
                "1y": 365
            }.get(time_range)
            
            if range_days:
                sessions = [
                    s for s in sessions 
                    if (current_date - datetime.strptime(s.get("date", ""), "%Y-%m-%d")).days <= range_days
                ]
        
        # Sort sessions by date
        sessions.sort(key=lambda x: datetime.strptime(x.get("date", ""), "%Y-%m-%d"))
        
        # Prepare data
        dates = [datetime.strptime(s.get("date", ""), "%Y-%m-%d") for s in sessions]
        distances = [s.get("total_distance", 0) for s in sessions]
        times = [s.get("total_time", 0) for s in sessions]
        
        # Create figure with two subplots
        fig = plt.figure(figsize=(12, 5))
        
        # Distance over time plot
        ax1 = fig.add_subplot(121)
        ax1.plot(dates, distances, 'b-o')
        ax1.set_title('Distance Over Time')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Distance (m)')
        ax1.grid(True)
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.setp(ax1.xaxis.get_majorticklabels(), rotation=45)
        
        # Time over distance scatter plot
        ax2 = fig.add_subplot(122)
        ax2.scatter(distances, times)
        ax2.set_title('Time vs Distance')
        ax2.set_xlabel('Distance (m)')
        ax2.set_ylabel('Time (s)')
        ax2.grid(True)
        
        # Adjust layout
        plt.tight_layout()
        
        # Create canvas
        canvas = FigureCanvasTkAgg(fig, self.charts_frame)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        self.current_figure = fig
        self.current_canvas = canvas
    
    def calculate_stats(self):
        db = Database()
        sessions = db.get_sessions()
        
        if not sessions:
            self._show_no_data()
            return
        
        # Calculate statistics
        total_sessions = len(sessions)
        total_distance = sum(session.get("total_distance", 0) for session in sessions)
        total_time = sum(session.get("total_time", 0) for session in sessions)
        
        avg_distance = total_distance / total_sessions if total_sessions > 0 else 0
        avg_time = total_time / total_sessions if total_sessions > 0 else 0
        
        # Update labels
        self.total_distance_label.configure(
            text=f"Total Distance: {total_distance}m"
        )
        self.total_sessions_label.configure(
            text=f"Total Sessions: {total_sessions}"
        )
        self.avg_distance_label.configure(
            text=f"Average Distance per Session: {avg_distance:.1f}m"
        )
        self.avg_time_label.configure(
            text=f"Average Time per Session: {avg_time:.1f}s"
        )
        
        # Add progress tracking
        if len(sessions) >= 2:
            first_distance = sessions[0].get("total_distance", 0)
            last_distance = sessions[-1].get("total_distance", 0)
            progress = ((last_distance - first_distance) / first_distance * 100 
                       if first_distance > 0 else 0)
            
            self.progress_label = ctk.CTkLabel(
                self.stats_frame,
                text=f"Progress: {progress:+.1f}% from first session",
                font=("Helvetica", 16)
            )
            self.progress_label.grid(row=4, column=0, pady=10, padx=20, sticky="w")
    
    def _show_no_data(self):
        """Display message when no data is available"""
        for widget in self.stats_frame.winfo_children():
            widget.destroy()
        
        no_data_label = ctk.CTkLabel(
            self.stats_frame,
            text="No session data available",
            font=("Helvetica", 16)
        )
        no_data_label.grid(row=0, column=0, pady=20)

    def export_data(self):
        from tkinter import filedialog
        import csv
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        
        if filename:
            db = Database()
            sessions = db.get_sessions()
            
            with open(filename, 'w', newline='') as file:
                writer = csv.DictWriter(
                    file, 
                    fieldnames=["date", "pool_length", "total_distance", "total_time"]
                )
                writer.writeheader()
                writer.writerows(sessions)

