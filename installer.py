import sys
from PyInstaller.__main__ import run

if __name__ == "__main__":
    options = [
        "--onefile",  # Create a single executable file
        "--name=codeDP",  # Name of the executable file
        "--icon=ui/icons/icon.svg",  # Set icon
        "--hidden-import=ibdp_classes",  # Manage Import
        "--windowed",
    ]

    # Add your main script
    scripts = ["editor.py"]

    # Run PyInstaller
    sys.exit(run(options + scripts))
