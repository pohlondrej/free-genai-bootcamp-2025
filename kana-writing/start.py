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
            # Add these for better error visibility
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        
        # Print output in real-time
        while True:
            output = backend.stdout.readline()
            if output:
                print(output.strip())
            # Check if process is still running
            if backend.poll() is not None:
                error = backend.stderr.read()
                if error:
                    print("Error:", error, file=sys.stderr)
                break
        
    except FileNotFoundError:
        print("Error: uvicorn not found. Make sure you have activated your conda environment and installed requirements.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down services...")
        if backend.poll() is None:
            backend.terminate()
        sys.exit(0)

if __name__ == "__main__":
    start_services()
