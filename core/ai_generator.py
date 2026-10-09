#!/usr/bin/env python3
"""AI generation engine using open-weight LLM via llama-cpp-python"""

import os
import ctypes

# We only load the model when needed to preserve RAM on low-end PCs
_llm_instance = None
_MODEL_PATH = None

def get_model_path():
    """Find the downloaded GGUF model."""
    global _MODEL_PATH
    if _MODEL_PATH and os.path.exists(_MODEL_PATH):
        return _MODEL_PATH
    candidates = [
        os.path.join(os.path.dirname(__file__), "..", "assets", "models", "SmolLM-135M-Instruct-q4_k_m.gguf"),
        os.path.join(os.path.dirname(__file__), "..", "assets", "models", "SmolLM2-360M-Instruct-q4_k_m.gguf"),
    ]
    for path in candidates:
        if os.path.exists(path):
            _MODEL_PATH = os.path.abspath(path)
            return _MODEL_PATH
    return None

def load_model():
    """Dynamically import and load the model. Done lazily to save memory."""
    from llama_cpp import Llama
    path = get_model_path()
    if not path:
        raise RuntimeError("No model file found! Run scripts/download_models.py first.")
    lib = Llama(
        model_path=path,
        n_ctx=512,       # Keep context small for RAM constraints
        n_threads=2,     # Match 2 cores but leave room for UI
        n_threads_batch=2,
        n_gpu_layers=0,
        verbose=False
    )
    return lib

def generate_demand(system_prompt: str, user_prompt: str = "The timer has run out.") -> str:
    """
    Load the model, generate a short demand, then unload to flush RAM.
    """
    global _llm_instance
    try:
        _llm_instance = load_model()
        out = _llm_instance(
            system_prompt=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=64,
            temperature=0.85,
            stop=["\n"],
        )
        result = out['choices'][0]['message']['content'].strip()
        return result
    finally:
        # Aggressive memory cleanup to free RAM on 8GB systems
        _llm_instance = None
        del _llm_instance
        try:
            import gc
            gc.collect()
        except Exception:
            pass
