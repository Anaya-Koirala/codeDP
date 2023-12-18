import sys
from PyInstaller.__main__ import run

if __name__ == "__main__":
    options = [
        "--onefile",  # Single executable file
        "--name=codeDP",  # Name
        "--icon=ui/icons/icon.svg",  # Icon
        "--hidden-import=ibdp_classes",  # Manage Import
        "--windowed", # Windowed mode without the console
    ]

    scripts = ["editor.py"]
    sys.exit(run(options + scripts))
