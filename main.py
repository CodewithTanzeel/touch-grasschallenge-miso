#!/usr/bin/env python3
"""Main PyQt6 UI for the transparent desktop companion"""

import sys
import os
import json
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QMenu
from PyQt6.QtGui import QMovie, QPixmap, QCursor, QAction
from PyQt6.QtCore import Qt, QTimer, QSize, pyqtSignal, QObject, QPoint
import pyttsx3
from core.thread_worker import GenerationWorker
from core.tracker import IdleTracker

class PetSignals(QObject):
    update_bubble = pyqtSignal(str)

class PetWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Miso - Touch Grass Companion")
        self.signals = PetSignals()
        self.signals.update_bubble.connect(self.show_speech_bubble)

        # Config
        self.character_dir = self._find_character()
        self.config = self._load_config()
        self.scale = self.config.get("scale", 1.0)
        self.base_size = QSize(128, 128)  # Base sprite size

        # UI State
        self.is_dragging = False
        self.drag_start_pos = QPoint()
        self.timer_minutes = 45  # Work session
        self.is_angry = False
        self.speech_bubble = None
        self.worker = None

        # Idle detection
        self.idle_tracker = IdleTracker(idle_threshold_sec=300)  # 5 minutes

        self._init_ui()
        self._init_timer()
        self._init_tts()
        self._start_idle_animation()
        self._start_idle_tracking()

    def _find_character(self):
        """Allow user to override via env, else default to miso."""
        override = os.getenv("MISO_CHARACTER")
        if override:
            path = Path("assets/characters") / override
            if path.exists():
                return path
        return Path("assets/characters/miso")

    def _load_config(self):
        config_path = self.character_dir / "config.json"
        if config_path.exists():
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _init_ui(self):
        # Window flags for transparent overlay
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Label for sprite/GIF
        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setScaledContents(False)
        self.setCentralWidget(self.label)

        # Position at bottom-right corner (above taskbar)
        screen = QApplication.primaryScreen().availableGeometry()
        w = int(self.base_size.width() * self.scale)
        h = int(self.base_size.height() * self.scale)
        self.move(screen.right() - w - 20, screen.bottom() - h - 40)
        self.resize(w, h)

        # Context menu for character swap
        self.label.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.label.customContextMenuRequested.connect(self._show_context_menu)

        # Enable dragging
        self.label.mousePressEvent = self._mouse_press_event
        self.label.mouseMoveEvent = self._mouse_move_event
        self.label.mouseReleaseEvent = self._mouse_release_event

    def _init_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._on_timer_finished)
        self.timer.start(self.timer_minutes * 60 * 1000)  # Convert to ms

    def _init_tts(self):
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[-1].id)
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.9)
        except Exception:
            self.tts_engine = None  # Silent fail if no TTS engine installed

    def _start_idle_animation(self):
        self._play_animation("idle.gif")

    def _start_idle_tracking(self):
        self.idle_tracker.start()

    def _play_animation(self, gif_name: str):
        gif_path = self.character_dir / gif_name
        if gif_path.exists():
            movie = QMovie(str(gif_path))
            # Scale movie to widget size
            movie.setScaledSize(QSize(
                int(self.base_size.width() * self.scale),
                int(self.base_size.height() * self.scale)
            ))
            self.label.setMovie(movie)
            movie.start()
        else:
            # Fallback to static image
            pixmap = QPixmap(str(self.character_dir / "idle.png"))
            if not pixmap.isNull():
                self.label.setPixmap(pixmap.scaled(
                    self.base_size * self.scale,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))

    def _on_timer_finished(self):
        """Called when work timer expires - check if user is actually present"""
        # If user has been idle for > 5 minutes, they likely walked away - don't get angry
        if self.idle_tracker.is_idle():
            # Reset timer since they're not actually at the desk
            self.timer.start(self.timer_minutes * 60 * 1000)
            return

        if self.is_angry:
            return  # Prevent duplicate triggers
        self.is_angry = True
        self._play_animation("angry.gif")
        self._trigger_generation()

    def _trigger_generation(self):
        """Offload AI + TTS to worker thread to prevent UI freeze"""
        if self.worker and self.worker.isRunning():
            return  # Already processing
        self.worker = GenerationWorker(self.config)
        self.worker.finished.connect(self._on_generation_finished)
        self.worker.start()

    def _on_generation_finished(self, text: str):
        """Handle result from AI worker thread"""
        self.signals.update_bubble.emit(text)
        self._speak_text(text)
        # Stay angry until user interacts or walks away

    def show_speech_bubble(self, text: str):
        """Display transient speech bubble"""
        if self.speech_bubble:
            self.speech_bubble.deleteLater()
        bubble = QLabel(text, self)
        bubble.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 255, 200, 220);
                border: 2px solid #8B4513;
                border-radius: 8px;
                padding: 8px;
                font-family: 'Comic Sans MS', cursive;
                font-size: 10pt;
            }
        """)
        bubble.adjustSize()
        # Position above the pet
        pet_pos = self.label.pos()
        bubble.move(pet_pos.x() - bubble.width()//2 + self.label.width()//2,
                    pet_pos.y() - bubble.height() - 10)
        bubble.show()
        self.speech_bubble = bubble
        # Auto-hide after 4 seconds
        QTimer.singleShot(4000, bubble.deleteLater)

    def _speak_text(self, text: str):
        """Speak using pyttsx3 (non-blocking); silent if engine unavailable."""
        if self.tts_engine is None:
            return  # No TTS engine installed — graceful fallback
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            print(f"TTS error: {e}")

    def enterEvent(self, event):
        """Mouse hover: switch to dancing if not angry"""
        if not self.is_angry:
            self._play_animation("dance.gif")
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Mouse leave: revert to idle"""
        if not self.is_angry:
            self._play_animation("idle.gif")
        super().leaveEvent(event)

    def _mouse_press_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = True
            self.drag_start_pos = event.pos()

    def _mouse_move_event(self, event):
        if self.is_dragging:
            diff = event.pos() - self.drag_start_pos
            new_pos = self.pos() + diff
            self.move(new_pos)

    def _mouse_release_event(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.is_dragging = False

    def _show_context_menu(self, pos):
        """Right-click to swap characters or quit"""
        menu = QMenu(self)
        reset_action = QAction("Reset to Miso", self)
        reset_action.triggered.connect(self._reset_to_default)
        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(QApplication.instance().quit)
        menu.addAction(reset_action)
        menu.addAction(quit_action)
        menu.exec(self.mapToGlobal(pos))

    def _reset_to_default(self):
        self.character_dir = Path("assets/characters/miso")
        self.config = self._load_config()
        self._start_idle_animation()


def main():
    app = QApplication(sys.argv)
    window = PetWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
