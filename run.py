import subprocess
import os
import signal
import sys
import time

def start_flask_app():
    """
    Start the Flask backend app.
    Assumes Flask app is in backend/app.py and uses Python 3.
    """
    try:
        print("Starting Flask backend...")
        flask_process = subprocess.Popen([
            sys.executable,  # Use the current Python interpreter
            "app.py"
        ], cwd=os.path.join(os.getcwd(), "backend"))
        return flask_process
    except Exception as e:
        print(f"Failed to start Flask app: {e}")
        return None

def start_react_app():
    """
    Start the React frontend app.
    Assumes React app is in frontend/ and uses npm run dev.
    """
    try:
        print("Starting React frontend...")
        # Use shell=True for Windows to ensure npm is found via PATH
        # Capture output to debug issues
        react_process = subprocess.Popen([
            "npm", "run", "dev"
        ], cwd=os.path.join(os.getcwd(), "frontend"), shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check for immediate errors (optional: remove if too slow)
        stdout, stderr = react_process.communicate(timeout=None)
        if stderr:
            print(f"React startup error: {stderr}")
            return None

        return react_process
    except Exception as e:
        print(f"Failed to start React app: {e}")
        return None

def shutdown(processes):
    """
    Shut down all running processes gracefully.
    Handle Windows compatibility for signals.
    """
    print("\nShutting down apps...")
    for process in processes:
        if process:
            try:
                # Use terminate for Windows, SIGINT for Unix-like systems
                if os.name == 'nt':  # Windows
                    process.terminate()  # More reliable on Windows
                else:  # Unix/Linux/Mac
                    process.send_signal(signal.SIGINT)
                process.wait(timeout=5)  # Wait up to 5 seconds for clean shutdown
            except Exception as e:
                print(f"Error during shutdown: {e}")
                try:
                    process.kill()  # Force kill if graceful shutdown fails
                except Exception as kill_error:
                    print(f"Failed to force kill process: {kill_error}")

    print("All apps shut down.")

def main():
    # Store processes to manage them later
    processes = []

    # Start Flask app
    flask_proc = start_flask_app()
    if flask_proc:
        processes.append(flask_proc)
    else:
        print("Exiting due to Flask startup failure.")
        sys.exit(1)

    # Give Flask a moment to start
    time.sleep(2)

    # Start React app
    react_proc = start_react_app()
    if react_proc:
        processes.append(react_proc)
    else:
        print("Exiting due to React startup failure.")
        shutdown(processes[:1])  # Shut down Flask if React fails
        sys.exit(1)

    try:
        # Keep the script running to monitor processes
        print("Both apps are running. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)  # Keep the main process alive

    except KeyboardInterrupt:
        # Handle Ctrl+C to shut down cleanly
        shutdown(processes)

if __name__ == "__main__":
    main()