"""Deteccion de impresoras y envio de trabajos crudos (Windows y Linux/Mac)."""

import shutil
import subprocess
import sys

if sys.platform == "win32":
    try:
        import win32print
    except ImportError:
        win32print = None


def infer_language(printer_name):
    """Deduce el lenguaje EPL o ZPL a partir del nombre de la cola."""
    lowered = printer_name.lower()
    if "epl" in lowered:
        return "epl"
    if "zpl" in lowered:
        return "zpl"
    return "zpl"


def list_printers():
    """Lista las impresoras disponibles en el sistema.

    Returns:
        Lista de dicts con 'name', 'language' y 'ready' (bool).
    """
    if sys.platform == "win32":
        return _list_printers_windows()
    return _list_printers_cups()


def send_raw(raw_bytes, printer_name):
    """Envia un flujo crudo (EPL o ZPL) a la impresora indicada.

    Args:
        raw_bytes: contenido a imprimir, en bytes.
        printer_name: nombre de la impresora de destino.

    Returns:
        Identificador del trabajo enviado.

    Raises:
        RuntimeError: si falta el backend de impresion o el envio falla.
    """
    if sys.platform == "win32":
        return _send_raw_windows(raw_bytes, printer_name)
    return _send_raw_cups(raw_bytes, printer_name)


# --- Linux / Mac (CUPS) ---

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
            "language": infer_language(name),
            "ready": "disabled" not in line,
        })
    return printers


def _send_raw_cups(raw_bytes, printer_name):
    if shutil.which("lp") is None:
        raise RuntimeError("No se encontro el comando 'lp' (CUPS no instalado).")
    try:
        result = subprocess.run(
            ["lp", "-d", printer_name, "-o", "raw"],
            input=raw_bytes,
            capture_output=True,
            timeout=60,
        )
    except subprocess.SubprocessError as e:
        raise RuntimeError(f"Fallo al ejecutar lp: {e}") from e

    if result.returncode != 0:
        error = result.stderr.decode("utf-8", errors="replace").strip()
        raise RuntimeError(f"La impresora rechazo el trabajo: {error}")

    job_id = result.stdout.decode("utf-8", errors="replace").strip()
    print(f"Trabajo enviado a '{printer_name}': {job_id}")
    return job_id


# --- Windows (win32print) ---

def _list_printers_windows():
    if win32print is None:
        return []
    printers = []
    flags = win32print.PRINTER_ENUM_LOCAL | win32print.PRINTER_ENUM_CONNECTIONS
    for _, _, name, _ in win32print.EnumPrinters(flags):
        printers.append({
            "name": name,
            "language": infer_language(name),
            "ready": True,
        })
    return printers


def _send_raw_windows(raw_bytes, printer_name):
    if win32print is None:
        raise RuntimeError(
            "Modulo win32print no instalado. Ejecuta: pip install pywin32"
        )
    hprinter = win32print.OpenPrinter(printer_name)
    try:
        job = win32print.StartDocPrinter(hprinter, 1, ("Label Job", None, "RAW"))
        try:
            win32print.StartPagePrinter(hprinter)
            win32print.WritePrinter(hprinter, raw_bytes)
            win32print.EndPagePrinter(hprinter)
        finally:
            win32print.EndDocPrinter(hprinter)
    finally:
        win32print.ClosePrinter(hprinter)
    print(f"Trabajo enviado a '{printer_name}': job {job}")
    return str(job)
