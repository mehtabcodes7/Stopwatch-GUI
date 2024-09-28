import tkinter as tk
import time

class StopwatchApp:
    def __init__(self, master):
        self.master = master
        master.title("Stopwatch")

        # Configure dark theme
        master.configure(bg="#2E2E2E")

        self.is_running = False
        self.start_time = 0
        self.elapsed_time = 0
        self.lap_times = []

        # Display for the stopwatch
        self.display = tk.Label(master, text="00:00:00.00", font=("Helvetica", 48), bg="#2E2E2E", fg="#FF5733")
        self.display.pack(pady=20)

        # Frame for buttons
        self.button_frame = tk.Frame(master, bg="#2E2E2E")
        self.button_frame.pack(pady=10)

        # Create control buttons with circular appearance
        self.start_button = self.create_button("Start", self.start)
        self.stop_button = self.create_button("Stop", self.stop)
        self.lap_button = self.create_button("Lap", self.record_lap)
        self.reset_button = self.create_button("Reset", self.reset)

        # Frame for lap display with scrollbar
        self.lap_frame = tk.Frame(master)
        self.lap_frame.pack(pady=20)

        self.lap_display = tk.Text(self.lap_frame, height=10, width=40, font=("Helvetica", 14), bg="#3A3A3A", fg="#FF5733", bd=0, wrap=tk.WORD)
        self.lap_display.pack(side=tk.LEFT, fill=tk.BOTH)

        self.scrollbar = tk.Scrollbar(self.lap_frame, orient="vertical", command=self.lap_display.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.lap_display.config(yscrollcommand=self.scrollbar.set)

        # Style for the scrollbar
        self.style_scrollbar()

    def create_button(self, text, command):
        button = tk.Button(self.button_frame, text=text, command=command, font=("Helvetica", 14), bg="#FF5733", fg="#2E2E2E", borderwidth=0, padx=10, pady=10, relief="flat")
        button.pack(pady=5, fill=tk.X)
        return button

    def style_scrollbar(self):
        self.scrollbar.config(bg="#1A1A1A", troughcolor="#2E2E2E", borderwidth=0)  # Darker background for the scrollbar

    def update(self):
        if self.is_running:
            self.elapsed_time = time.time() - self.start_time
            self.display.config(text=self.format_time(self.elapsed_time))
            self.master.after(10, self.update)

    def start(self):
        if not self.is_running:
            self.start_time = time.time() - self.elapsed_time
            self.is_running = True
            self.update()

    def stop(self):
        self.is_running = False

    def reset(self):
        self.stop()
        self.elapsed_time = 0
        self.display.config(text="00:00:00.00")
        self.lap_times.clear()
        self.lap_display.delete(1.0, tk.END)

    def record_lap(self):
        if self.is_running:
            lap_time = self.elapsed_time
            self.lap_times.append(lap_time)
            lap_time_str = self.format_time(lap_time)
            lap_duration = lap_time - (self.lap_times[-2] if len(self.lap_times) > 1 else 0)
            lap_duration_str = self.format_time(lap_duration)
            self.lap_display.insert(tk.END, f"Lap {len(self.lap_times)}: {lap_time_str} (Duration: {lap_duration_str})\n")

    def format_time(self, elapsed):
        hours, remainder = divmod(int(elapsed), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((elapsed - int(elapsed)) * 100)
        return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:02}"

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()
