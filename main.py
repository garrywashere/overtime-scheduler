import subprocess

if __name__ == "__main__":
    try:
        subprocess.run(["gunicorn", "-w", "1", "-b", "127.0.0.1", "frontend:app"])
    except KeyboardInterrupt:
        print("Server Stopped.")