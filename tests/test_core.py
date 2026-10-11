#!/usr/bin/env python3
"""Basic smoke tests for Miso core components"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_ai_import():
    from core.ai_generator import generate_demand, load_model
    msg = generate_demand("Test prompt.")
    assert isinstance(msg, str) and len(msg) > 0
    print("PASS: ai_generator import + generate_demand")

def test_tracker():
    from core.tracker import IdleTracker
    t = IdleTracker(idle_threshold_sec=10)
    t.start()
    assert t.is_idle() is False  # just started
    t.stop()
    print("PASS: tracker start/stop")

def test_config():
    import json
    path = "assets/characters/miso/config.json"
    assert os.path.exists(path)
    with open(path) as f:
        cfg = json.load(f)
    assert cfg.get("name") == "Miso"
    assert cfg.get("voice_pitch") == 1.3
    print("PASS: config loaded + voice_pitch 1.3")

def test_assets():
    for gif in ["idle.gif", "dance.gif", "angry.gif"]:
        p = os.path.join("assets/characters/miso", gif)
        assert os.path.exists(p), f"missing {gif}"
    print("PASS: 3 GIF assets present")

if __name__ == "__main__":
    test_ai_import()
    test_tracker()
    test_config()
    test_assets()
    print("\nAll tests passed.")
