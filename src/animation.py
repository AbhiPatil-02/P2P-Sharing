# animations.py

import tkinter as tk
from tkinter import ttk
import threading
import time
import math
from typing import Callable, Optional
from config import config
from utils import get_random_emoji

class Animator:
    def __init__(self):
        self.active_animations = []
        self.root = None

    def init_root(self, root):
        self.root = root

    def show_animation(self, animation_type="success", message=None, duration=2.5):
        if not self.root:
            return

        thread = threading.Thread(
            target=self._run_animation,
            args=(animation_type, message, duration),
            daemon=True
        )
        thread.start()

    def _run_animation(self, animation_type, message, duration):
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-alpha", 0.0)
        popup.attributes("-topmost", True)

        # Default messages per animation type
        if not message:
            message = {
                "success": "🎉 Operation Completed!",
                "error": "❌ Operation Failed",
                "transfer": "📁 File Transfer Complete",
                "connection": "🔗 Connection Established",
                "notification": "💬 New Message"
            }.get(animation_type, "🔔 Notification")

        # Color theme per animation type
        color_scheme = {
            "success": {"bg": "#e8f5e9", "fg": "#2e7d32"},      # Green
            "error": {"bg": "#ffebee", "fg": "#c62828"},        # Red
            "transfer": {"bg": "#e3f2fd", "fg": "#1565c0"},     # Blue
            "connection": {"bg": "#e0f7fa", "fg": "#00838f"},   # Cyan
            "notification": {"bg": "#f3e5f5", "fg": "#6a1b9a"}  # Purple
        }

        colors = color_scheme.get(animation_type, {"bg": "#f5f5f5", "fg": "#424242"})
        bg_color = colors["bg"]
        fg_color = colors["fg"]

        canvas = tk.Canvas(popup, bg=bg_color, highlightthickness=0, width=300, height=150)
        canvas.pack()

        canvas.create_oval(10, 10, 50, 50, fill=fg_color, outline="")
        canvas.create_rectangle(250, 100, 290, 140, fill=fg_color, outline="")

        text_id = canvas.create_text(
            150, 60,
            text=message,
            font=("Segoe UI", 12, "bold"),
            fill=fg_color,
            width=280
        )

        self._fade_in(popup)
        self._float_effect(canvas, text_id)
        self._particle_effect(canvas, fg_color)

        time.sleep(duration)
        self._fade_out(popup)

    def _fade_in(self, window, duration=0.5):
        for i in range(1, 11):
            window.attributes("-alpha", i / 10)
            time.sleep(duration / 10)

    def _fade_out(self, window, duration=0.5):
        for i in range(9, -1, -1):
            window.attributes("-alpha", i / 10)
            time.sleep(duration / 10)
        window.destroy()

    def _float_effect(self, canvas, text_id, amplitude=5, period=2):
        start_time = time.time()
        original_y = canvas.coords(text_id)[1]

        while time.time() - start_time < period:
            elapsed = time.time() - start_time
            offset = amplitude * math.sin(2 * math.pi * elapsed / period)
            canvas.coords(text_id, 150, original_y + offset)
            canvas.update()
            time.sleep(0.02)

        canvas.coords(text_id, 150, original_y)

    def _particle_effect(self, canvas, color, count=15):
        particles = []
        for _ in range(count):
            x, y = 150, 75
            size = 3
            dx = (0.5 - (1 / 10)) * 10
            dy = (0.5 - (1 / 10)) * 10
            particle = canvas.create_oval(x, y, x + size, y + size, fill=color, outline="")
            particles.append((particle, dx, dy))

        for _ in range(20):
            for i, (particle, dx, dy) in enumerate(particles):
                canvas.move(particle, dx, dy)
                dy += 0.2
                particles[i] = (particle, dx, dy)
            canvas.update()
            time.sleep(0.03)

        for particle, _, _ in particles:
            canvas.delete(particle)

    def show_loading(self, message="Processing...", callback=None):
        popup = tk.Toplevel(self.root)
        popup.overrideredirect(True)
        popup.attributes("-alpha", 0.9)
        popup.attributes("-topmost", True)

        w, h = 300, 100
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        popup.geometry(f"{w}x{h}+{x}+{y}")

        canvas = tk.Canvas(popup, bg="#333333", highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)

        canvas.create_text(
            w // 2, h // 2 - 10,
            text=message,
            font=("Segoe UI", 11),
            fill="#ffffff"
        )

        spinner = canvas.create_arc(
            w // 2 - 20, h // 2 + 10,
            w // 2 + 20, h // 2 + 50,
            start=0,
            extent=0,
            outline="#4CAF50",
            width=3,
            style=tk.ARC
        )

        def animate_spinner(angle=0):
            canvas.itemconfig(spinner, start=angle)
            angle = (angle + 10) % 360
            popup.after(50, animate_spinner, angle)

        animate_spinner()

        if callback:
            def wrapped_callback():
                callback()
                popup.destroy()
            popup.after(100, wrapped_callback)

        return popup

    def show_progress_bar(self, title="Progress", max_value=100):
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.resizable(False, False)
        popup.attributes("-topmost", True)

        w, h = 400, 120
        x = (self.root.winfo_screenwidth() - w) // 2
        y = (self.root.winfo_screenheight() - h) // 2
        popup.geometry(f"{w}x{h}+{x}+{y}")

        tk.Label(popup, text=title, font=("Segoe UI", 12)).pack(pady=5)

        progress = ttk.Progressbar(
            popup,
            orient=tk.HORIZONTAL,
            length=300,
            mode='determinate',
            maximum=max_value
        )
        progress.pack(pady=10)

        return popup, progress

# Global animator instance
animator = Animator()

# Helper methods for use in the app
def show_animation():
    animator.show_animation("success")

def show_startup_animation():
    if animator.root:
        animator.show_loading("Starting P2P Share...")

def show_connection_animation(message):
    if animator.root:
        animator.show_animation("connection", message)

def show_chat_notification(message):
    if animator.root:
        animator.show_animation("notification", message, duration=2.0)
