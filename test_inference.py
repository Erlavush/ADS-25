
import os
import sys
import time

# Add current dir to sys.path
sys.path.append(os.getcwd())

from app import load_models, separate_audio
import torch

try:
    print("Initializing models...")
    mixer, d_model, m_model = load_models()
    
    test_file = r"c:\Users\user\Downloads\JRoa - Byahe.mp3"
    if not os.path.exists(test_file):
        print(f"Test file not found: {test_file}")
        sys.exit(1)
        
    print(f"Running separation on {test_file}...")
    # Mocking streamlit functions since app.py uses them
    import streamlit as st
    class MockProgress:
        def progress(self, *args, **kwargs): pass
    st.progress = lambda x, text=None: MockProgress()
    
    start_time = time.time()
    outputs = separate_audio(test_file, mixer, d_model, m_model)
    end_time = time.time()
    
    print("Separation successful!")
    print(f"Time taken: {end_time - start_time:.2f}s")
    print("Output files:", outputs)
    
except Exception as e:
    print(f"TEST FAILED: {e}")
    import traceback
    traceback.print_exc()
