import subprocess
import sys
import os
from pathlib import Path

def start_services():
    root_dir = Path(__file__).parent.absolute()
    
    try:
        # Start backend
        print("Starting backend server at http://localhost:8000 ...")
        backend = subprocess.Popen(
            ["uvicorn", "main:app", "--reload", "--port", "8000"],
            cwd=root_dir / "backend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Start frontend
        print("Starting frontend at http://localhost:8501 ...")
        frontend = subprocess.Popen(
            ["streamlit", "run", "app.py"],
            cwd=root_dir / "frontend",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Monitor both processes
        while True:
            b_output = backend.stdout.readline()
            f_output = frontend.stdout.readline()
            if b_output:
                print("Backend:", b_output.strip())
            if f_output:
                print("Frontend:", f_output.strip())
            if backend.poll() is not None or frontend.poll() is not None:
                break
        
    except FileNotFoundError:
        print("Error: uvicorn not found. Make sure you have activated your conda environment and installed requirements.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down services...")
        if backend.poll() is None:
            backend.terminate()
        if frontend.poll() is None:
            frontend.terminate()
        sys.exit(0)

if __name__ == "__main__":
    start_services()
