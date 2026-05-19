"""Empaqueta la app en un ejecutable standalone con PyInstaller.

Uso:
    python build.py

El ejecutable queda en dist/ZebraLabelPrinter  (Linux/Mac)
                  o  dist/ZebraLabelPrinter.exe (Windows)
"""

import subprocess
import sys


def main():
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "ZebraLabelPrinter",
        "--collect-all", "customtkinter",
        "--collect-all", "fitz",
        "main.py",
    ]

    print("Construyendo ejecutable...")
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)
    print("\nListo. El ejecutable esta en la carpeta dist/")


if __name__ == "__main__":
    main()
