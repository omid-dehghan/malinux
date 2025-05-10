import matplotlib.pyplot as plt
from Develops.Deepwork.database import Database
from matplotlib.animation import FuncAnimation
from datetime import datetime

class Chart:
    def __init__(self, db: Database):
        self.db = db
        self.fig, self.ax = plt.subplots(figsize=(8, 6))
      
        
    
    def format_minutes(self, m):
        hours = int(m) // 60
        minutes = int(m) % 60
        return f"{hours}h {minutes}m" if hours else f"{minutes}m"

    def update_chart(self, frame):
        self.ax.clear()  # Clear old bars
        dates, durations = self.db.get_dates_and_durations()
        if not dates:
            return  # Avoid crash on empty chart
        formatted_dates = [
            datetime.strptime(d, "%Y-%m-%d").strftime("%a, %y-%m-%d")
            for d in dates
        ]
        bars = self.ax.bar(dates, durations)
        self.ax.set_xticks(range(len(dates)))
        self.ax.set_xticklabels(formatted_dates, rotation=90)

        # Format Y-axis ticks as HH:MM
        locs = self.ax.get_yticks()
        self.ax.set_yticks(locs)
        self.ax.set_yticklabels([self.format_minutes(m) for m in locs])
        self.ax.grid(axis='y')
        self.ax.bar_label(bars, labels=[self.format_minutes(d) for d in durations], padding=3, fontsize=8)
        self.fig.tight_layout(pad=2.0)
        self.fig.canvas.manager.set_window_title("Deepwork")
        
        self.fig.canvas.draw_idle()  # Redraw canvas
        

    def bar_chart(self, interval=3000):
        self.ani = FuncAnimation(self.fig, self.update_chart, interval=interval, cache_frame_data=False)
        plt.show()