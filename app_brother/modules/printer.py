"""Módulo de detección de impresoras e impresión nativa de PDFs (Brother y estándar)."""

import shutil
import subprocess
import sys

if sys.platform == "win32":
    try:
        import win32print
        import win32api
    except ImportError:
        win32print = None
        win32api = None


def list_printers():
    """Lista todas las impresoras disponibles en el sistema.

    Returns:
        Lista de dicts con 'name' y 'ready' (bool).
    """
    if sys.platform == "win32":
        return _list_printers_windows()
    return _list_printers_cups()


def print_pdf(pdf_path, printer_name, auto_cut=True):
    """Envía un archivo PDF a la impresora seleccionada a través del controlador del sistema.

    Args:
        pdf_path: ruta absoluta o relativa al archivo PDF.
        printer_name: nombre de la cola de impresión de destino.
        auto_cut: True para cortar después de cada etiqueta, False para cortar sólo al final de la tira.

    Returns:
        Identificador o mensaje del trabajo enviado.

    Raises:
        RuntimeError: si el envío falla o no se cuenta con los comandos necesarios.
    """
    if sys.platform == "win32":
        return _print_pdf_windows(pdf_path, printer_name)
    return _print_pdf_cups(pdf_path, printer_name, auto_cut)


# --- Linux / macOS (CUPS) ---

def _list_printers_cups():
    if shutil.which("lpstat") is None:
        return []
    try:
        result = subprocess.run(
            ["lpstat", "-p"], capture_output=True, text=True, timeout=10
        )
    except (subprocess.SubprocessError, OSError):
        return []

    printers = []
    for line in result.stdout.splitlines():
        if not line.startswith("printer "):
            continue
        name = line.split()[1]
        printers.append({
            "name": name,
            "ready": "disabled" not in line,
        })
    return printers


def _print_pdf_cups(pdf_path, printer_name, auto_cut=True):
    if shutil.which("lp") is None:
        raise RuntimeError("No se encontró el comando 'lp' (CUPS no está instalado).")
    
    cut_opt = "AutoCut=True" if auto_cut else "AutoCut=False"
    try:
        result = subprocess.run(
            ["lp", "-d", printer_name, "-o", "PageSize=29mm", "-o", cut_opt, pdf_path],
            capture_output=True,
            timeout=60,
        )
    except subprocess.SubprocessError as e:
        raise RuntimeError(f"Fallo al ejecutar lp: {e}") from e

    if result.returncode != 0:
        error = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"La impresora rechazó el trabajo: {error}")

    job_id = result.stdout.decode("utf-8", errors="replace").strip()
    print(f"PDF enviado a '{printer_name}': {job_id}")
    return job_id


# --- Windows (ShellExecute / win32api) ---

def _list_printers_windows():
    if win32print is None:
        return []
    printers = []
    flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    for _, _, name, _ in win32print.EnumPrinters(flags):
        printers.append({
            "name": name,
            "ready": True,
        })
    return printers


def _print_pdf_windows(pdf_path, printer_name):
    if win32api is None:
        raise RuntimeError(
            "Módulo pywin32 no instalado. Ejecuta: pip install pywin32"
        )
    # Envía a imprimir de manera silenciosa usando la aplicación predeterminada del OS
    try:
        win32api.ShellExecute(
            0,
            "printto",
            pdf_path,
            f'"{printer_name}"',
            ".",
            0
        )
        return "Trabajo enviado a cola de impresión de Windows"
    except Exception as e:
        raise RuntimeError(f"Error al enviar trabajo a través de ShellExecute: {e}") from e
