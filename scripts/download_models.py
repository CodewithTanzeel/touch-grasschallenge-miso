#!/usr/bin/env python3
# Auto-downloads open-weight models for the desktop companion
# Designed to work locally without internet after first run

import os
from huggingface_hub import hf_hub_download

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

# Small open-weight model for 8GB RAM / dual-core CPU
# 135M params fits in ~200MB RAM
# Note: transformers pipeline downloads its own weights from HuggingFace
# on first use (model="HuggingFaceTB/SmolLM-135M-Instruct").
# No GGUF required. This script ensures the assets directory exists.
MODULE_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models', 'transformers')
os.makedirs(MODULE_DIR, exist_ok=True)
print("Pipeline model directory ready. First run will download "
      "HuggingFaceTB/SmolLM-135M-Instruct via transformers pipeline.")

print("Checking for model file...")
if not os.path.exists(os.path.join(MODEL_DIR, MODEL_FILE)):
    print("Downloading open-weight model for local AI brain...")
    try:
        hf_hub_download(
            repo_id=REPO_ID,
            filename=MODEL_FILE,
            local_dir=MODEL_DIR,
            local_dir_use_symlinks=False
        )
        print(f"Model downloaded to: {MODEL_DIR}/{MODEL_FILE}")
    except Exception as e:
        print(f"Download failed: {e}")
else:
    print("Model already exists locally.")
