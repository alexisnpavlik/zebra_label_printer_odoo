"""Deteccion de impresoras y envio de trabajos crudos via CUPS."""

import shutil
import subprocess


def infer_language(printer_name):
    """Deduce el lenguaje de una impresora a partir del nombre de su cola.

    Las colas de Zebra suelen incluir 'EPL' o 'ZPL' en el nombre. Si no se
    puede deducir, se asume ZPL (lenguaje moderno por defecto).
    """
    lowered = printer_name.lower()
    if "epl" in lowered:
        return "epl"
    if "zpl" in lowered:
        return "zpl"
    return "zpl"


def list_printers():
    """Lista las impresoras configuradas en CUPS.

    Returns:
        Lista de dicts con 'name', 'language' y 'ready' (bool), una por cola.
    """
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


def send_raw(raw_bytes, printer_name):
    """Envia un flujo crudo (EPL o ZPL) a una impresora.

    Args:
        raw_bytes: contenido a imprimir, en bytes.
        printer_name: nombre de la cola CUPS de destino.

    Returns:
        El id de trabajo informado por CUPS.

    Raises:
        RuntimeError: si falta el comando lp o si el envio falla.
    """
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
