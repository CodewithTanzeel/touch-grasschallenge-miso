# UI Design Note

The `ui/` directory is intentionally empty. All user interface code lives in `main.py` (`PetWindow` class) to keep the desktop companion lightweight (single-file launch, no import overhead). If the project grows (multiple windows, settings dialogs, or theme editors), this directory should contain `window.py`, `bubble.py`, and `styles.py`.

## Why this gap existed
The initial prompt asked for a "desktop companion" but did not specify architecture. A modular UI was assumed but never requested. To prevent this gap in future prompts: explicitly ask "should UI be split into modules or kept in main.py?"
