import os
import platform

from pathlib import Path

APPDIR: Path = None

if   platform.system() == "Windows":
    APPDIR = Path(os.getenv("APPDATA")) / "Lekco" / "Visurus"
elif platform.system() in ["Linux", "Darwin"]:
    APPDIR = Path.home() / ".config" / "Lekco" / "Visurus"
