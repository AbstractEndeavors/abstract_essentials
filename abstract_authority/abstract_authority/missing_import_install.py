import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def install_missing_imports(error_log):
    with open(error_log, 'r') as file:
        content = file.read()

    missing_imports = []
    for line in content.splitlines():
        if "No module named" in line:
            missing_import = line.split("No module named ")[1].strip()
            if missing_import not in missing_imports:
                missing_imports.append(missing_import)

    if missing_imports:
        print("Installing missing imports...")
        for module in missing_imports:
            os.system(f"pip install {module}")
            print(f"Installed {module}")
        print("All missing imports have been installed.")

class LogEventHandler(FileSystemEventHandler):
    def __init__(self, error_log):
        self.error_log = error_log

    def on_modified(self, event):
        if event.src_path == self.error_log:
            install_missing_imports(self.error_log)

def monitor_error_log(error_log):
    event_handler = LogEventHandler(error_log)
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(error_log), recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    error_log = "error_log.txt"  # Replace this with the path to your error log
    monitor_error_log(error_log)
