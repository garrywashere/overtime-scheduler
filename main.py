# Author: Garry Ivanovs
# Created: 06-03-2025
# Modified 06-03-2025

import subprocess

if __name__ == "__main__":
    try:
        subprocess.run(["gunicorn", "-w", "1", "-b", "127.0.0.1", "frontend:app"])
    except KeyboardInterrupt:
        print("Server Stopped.")