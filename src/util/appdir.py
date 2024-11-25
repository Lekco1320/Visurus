import os
import platform

from pathlib import Path

APPDIR: Path = None

def check_appdir():
    global APPDIR
    system = platform.system()
    if system == "Windows":
        app_resource = Path(os.getenv("APPDATA")) / "Lekco" / "Visurus"
    elif system in ["Linux", "Darwin"]:
        app_resource = Path.home() / ".config" / "Lekco" / "Visurus"
    APPDIR = app_resource

check_appdir()
