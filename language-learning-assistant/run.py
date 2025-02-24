import multiprocessing
import subprocess
import sys
import os
from pathlib import Path

def run_backend():
    """Run the FastAPI backend server"""
    subprocess.run([
        "uvicorn",
        "backend.app.main:app",
        "--reload",
        "--port", "8000"
    ])

def run_frontend():
    """Run the Streamlit frontend"""
    subprocess.run([
        "streamlit",
        "run",
        "frontend/app.py",
        "--server.port", "8501"
    ])

if __name__ == "__main__":
    # Start backend and frontend in parallel
    backend = multiprocessing.Process(target=run_backend)
    frontend = multiprocessing.Process(target=run_frontend)

    try:
        print("Starting backend server...")
        backend.start()
        print("Starting frontend server...")
        frontend.start()

        # Wait for both processes
        backend.join()
        frontend.join()

    except KeyboardInterrupt:
        print("\nShutting down servers...")
        backend.terminate()
        frontend.terminate()
        backend.join()
        frontend.join()
        sys.exit(0)
