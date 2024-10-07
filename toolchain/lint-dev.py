import os
import subprocess
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            proc = subprocess.Popen(
                ["mypy", "."], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            output, error = proc.communicate()
            output = output.decode("utf-8")
            error = error.decode("utf-8")
            if "error" in output or "error" in error:
                lines = output.splitlines()
                os.system("clear" if os.name == "posix" else "cls")
                for line in lines[:6]:
                    print(line)
                proc.terminate()
            else:
                print("No errors found.")


if __name__ == "__main__":
    path = "."  # Watch the current directory
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
