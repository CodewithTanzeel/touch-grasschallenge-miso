#!/usr/bin/env python3
"""AI generation engine using transformers (pre-built binary, no C compiler needed)"""

import os

# Load model only when needed to preserve RAM
_model = None
_tokenizer = None

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "models", "transformers")
os.makedirs(MODEL_DIR, exist_ok=True)

def get_model_path():
    """Find the downloaded GGUF / model files."""
    # For transformers, we use a small pre-trained model that doesn't need compilation
    # We'll download it on first run
    return MODEL_DIR

def load_model():
    """Load the open-weight model using transformers (no compilation required)."""
    from transformers import pipeline
    # Use a small instruction-tuned model (~135MB) that runs on CPU
    # This avoids llama-cpp-python which requires MSVC/nmake (C compiler)
    generator = pipeline(
        "text-generation",
        model="HuggingFaceTB/SmolLM-135M-Instruct",
        device=-1,  # CPU only (compatible with 8GB RAM / dual-core)
        dtype="auto",
        trust_remote_code=True
    )
    return generator

def generate_demand(system_prompt: str) -> str:
    """
    Load the model, generate a short demand, then unload to flush RAM.
    Uses transformers library (pre-built binary) instead of llama-cpp-python
    to avoid C compiler (nmake/MSVC) dependency failures.
    """
    import gc
    try:
        generator = load_model()
        prompt = f"{system_prompt}\nThe timer has run out. Write exactly one funny sentence demanding the user go outside immediately."
        out = generator(
            prompt,
            max_new_tokens=64,
            temperature=0.85,
            do_sample=True,
            return_full_text=False,
        )
        result = out[0]["generated_text"].strip()
        # Clean up: unload model and flush RAM for 8GB systems
        del generator
        gc.collect()
        return result
    except Exception as e:
        # Fallback for compatibility: return a pre-written message
        # This ensures the companion always works, even if the model download fails
        return "Go outside before I bite you! Touch some grass right now!"
