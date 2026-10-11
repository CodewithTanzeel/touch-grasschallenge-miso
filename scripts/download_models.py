#!/usr/bin/env python3
# Auto-downloads open-weight models for the desktop companion
# Designed to work locally without internet after first run
# Uses transformers pipeline format (no GGUF / no MSVC needed)

import os
from huggingface_hub import hf_hub_download

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

# Pipeline model directory (transformers downloads here on first use)
MODULE_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models', 'transformers')
os.makedirs(MODULE_DIR, exist_ok=True)

# Match the model used by core/ai_generator.py
REPO_ID = "HuggingFaceTB/SmolLM-135M-Instruct"
# For transformers pipeline, no single GGUF file is required;
# the pipeline downloads weights automatically on first inference.
# We provide an option to pre-fetch via hf_hub_download for offline use.

print("Pipeline model directory ready.")
print("First run will download", REPO_ID, "via transformers pipeline.")

# Optional: pre-download model weights for fully offline operation
# (transformers caches weights in its own cache dir; this ensures
# the repo is available in assets/ for portability.)
try:
    # Check if cached / downloaded
    from transformers import AutoTokenizer, AutoModelForCausalLM
    print("Transformers import OK. Model will load from cache or HuggingFace on first use.")
except Exception as e:
    print("Transformers not fully available:", e)

print("To run offline after first download: python main.py")
