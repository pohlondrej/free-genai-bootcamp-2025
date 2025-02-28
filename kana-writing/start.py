import subprocess
import sys
from pathlib import Path
from multiprocessing import Process, Queue
from queue import Empty
from threading import Thread
import time

def print_output(proc, prefix):
    """Print output from subprocess with prefix"""
    for line in iter(proc.stdout.readline, b''):
        print(f"{prefix}:", line.encode().rstrip())

def run_service(cmd, cwd, prefix, queue):
    """Run a service and capture its output"""
    try:
        proc = subprocess.Popen(
            cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True
        )
        
        # Start thread to print output
        printer = Thread(target=print_output, args=(proc, prefix))
        printer.daemon = True
        printer.start()
        
        # Wait for process to complete
        proc.wait()
        
    except Exception as e:
        queue.put((prefix, e))
    finally:
        queue.put((prefix, "stopped"))

def main():
    root_dir = Path(__file__).parent.absolute()
    error_queue = Queue()
    
    # Define services
    services = [
        {
            'name': 'Backend',
            'cmd': ['uvicorn', 'main:app', '--reload', '--port', '8000'],
            'cwd': root_dir / 'backend'
        },
        {
            'name': 'Frontend',
            'cmd': ['streamlit', 'run', 'app.py'],
            'cwd': root_dir / 'frontend'
        }
    ]
    
    # Start all services
    processes = []
    try:
        for service in services:
            p = Process(
                target=run_service,
                args=(service['cmd'], service['cwd'], service['name'], error_queue)
            )
            p.start()
            processes.append(p)
        
        # Monitor services
        while any(p.is_alive() for p in processes):
            try:
                name, msg = error_queue.get(timeout=0.1)
                if msg != "stopped":
                    print(f"Error in {name}: {msg}")
                    break
            except Empty:
                continue
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # Cleanup
        for p in processes:
            if p.is_alive():
                p.terminate()
                p.join(timeout=1)

if __name__ == "__main__":
    main()
