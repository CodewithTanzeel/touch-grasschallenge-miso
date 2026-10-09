#!/usr/bin/env python3
"""Concurrent AI work in a QThread to prevent UI freeze"""

from PyQt6.QtCore import QThread, pyqtSignal
from core.ai_generator import generate_demand

class GenerationWorker(QThread):
    finished = pyqtSignal(str)  # Emits generated text

    def __init__(self, config):
        super().__init__()
        self.config = config

    def run(self):
        try:
            result = generate_demand(
                system_prompt=self.config.get("system_prompt", "Demand they go outside."),
            )
            self.finished.emit(result)
        except Exception as e:
            self.finished.emit(f"Go outside before I bite you! ({str(e)})")
