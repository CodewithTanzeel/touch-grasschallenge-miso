#!/usr/bin/env python3
# Auto-downloads open-weight models for the desktop companion
# Designed to work locally without internet after first run

import os
from huggingface_hub import hf_hub_download

MODEL_DIR = os.path.join(os.path.dirname(__file__), '..', 'assets', 'models')
os.makedirs(MODEL_DIR, exist_ok=True)

# Small open-weight model for 8GB RAM / dual-core CPU
# 135M params fits in ~200MB RAM
MODEL_FILE = "SmolLM-135M-Instruct-q4_k_m.gguf"
REPO_ID = "HuggingFaceTB/SmolLM2-135M-Instruct"

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
