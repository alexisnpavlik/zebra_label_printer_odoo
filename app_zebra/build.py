"""Empaqueta la app en un ejecutable standalone con PyInstaller.

Uso:
    python build.py

El ejecutable queda en dist/ZebraLabelPrinter  (Linux/Mac)
                  o  dist/ZebraLabelPrinter.exe (Windows)
"""

import os
import subprocess
import sys


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "ZebraLabelPrinter",
        "--add-data", f"{os.path.join(script_dir, 'assets')}:assets",
        "--collect-all", "customtkinter",
        "--collect-all", "fitz",
        os.path.join(script_dir, "main.py"),
    ]

    print("Construyendo ejecutable...")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True, cwd=script_dir)
    print("\nListo. El ejecutable esta en la carpeta dist/")


if __name__ == "__main__":
    main()
