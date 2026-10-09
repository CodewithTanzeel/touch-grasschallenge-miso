#!/usr/bin/env python3
"""Cross-platform idle detection using pynput"""

import time
import threading
from pynput import mouse, keyboard

class IdleTracker:
    def __init__(self, idle_threshold_sec=300):  # 5 minutes
        self.idle_threshold = idle_threshold_sec
        self._last_activity = time.time()
        self._listener = None
        self._running = False

    def _on_activity(self):
        self._last_activity = time.time()

    def start(self):
        if self._running:
            return
        self._running = True
        self._last_activity = time.time()

        def on_move(x, y): self._on_activity()
        def on_click(x, y, button, pressed): self._on_activity()
        def on_scroll(x, y, dx, dy): self._on_activity()
        def on_press(key): self._on_activity()
        def on_release(key): self._on_activity()

        mouse_listener = mouse.Listener(
            on_move=on_move,
            on_click=on_click,
            on_scroll=on_scroll
        )
        keyboard_listener = keyboard.Listener(
            on_press=on_press,
            on_release=on_release
        )

        mouse_listener.start()
        keyboard_listener.start()
        self._listener = (mouse_listener, keyboard_listener)

    def stop(self):
        self._running = False
        if self._listener:
            mouse_listener, keyboard_listener = self._listener
            mouse_listener.stop()
            keyboard_listener.stop()
            self._listener = None

    def get_idle_time(self):
        if not self._running:
            return self.idle_threshold  # Treat as idle if not started
        return time.time() - self._last_activity

    def is_idle(self):
        return self.get_idle_time() >= self.idle_threshold
