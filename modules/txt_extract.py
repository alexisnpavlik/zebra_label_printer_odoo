"""Extraccion de datos de etiqueta desde un TXT con bloques ZPL de Odoo."""

import re

# Cada etiqueta ZPL esta delimitada por ^XA ... ^XZ.
_BLOCK_RE = re.compile(r'\^XA(.*?)\^XZ', re.DOTALL)

# Texto de fuente grande (altura >= 35): es el nombre del producto.
_NAME_RE = re.compile(r'\^A0N,(\d+),\d+\^FD(.*?)\^FS')

# Barcode: digitos que siguen a un comando ^BC.
_BARCODE_RE = re.compile(r'\^BC.*?\^FD(\d+)\^FS', re.DOTALL)

# Precio: campo que contiene "$" o simbolo monetario.
_PRICE_RE = re.compile(r'\^FD([^F]*\$[^F]*)\^FS')


def extract_labels(txt_path):
    """Extrae los datos de etiqueta de un archivo TXT con bloques ZPL.

    Args:
        txt_path: ruta al archivo TXT generado por Odoo.

    Returns:
        Lista de dicts con claves 'barcode', 'name' y 'price', una por bloque.
    """
    with open(txt_path, encoding="utf-8", errors="replace") as f:
        content = f.read()

    labels = []
    for m in _BLOCK_RE.finditer(content):
        label = _parse_block(m.group(1))
        if label["barcode"] or label["name"]:
            labels.append(label)

    if not labels:
        raise ValueError("No se encontraron etiquetas ZPL en el archivo.")

    print(f"TXT leido: {len(labels)} etiqueta(s)")
    return labels


def _parse_block(block):
    """Extrae barcode, nombre y precio de un bloque ^XA...^XZ."""
    barcode = ""
    bc_m = _BARCODE_RE.search(block)
    if bc_m:
        barcode = bc_m.group(1)

    name = ""
    for m in _NAME_RE.finditer(block):
        if int(m.group(1)) >= 35:
            name = m.group(2)
            break

    price = ""
    price_m = _PRICE_RE.search(block)
    if price_m:
        price = price_m.group(1).strip()

    return {"barcode": barcode, "name": name, "price": price}
