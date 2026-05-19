"""Funciones de texto compartidas por los generadores de etiqueta."""

import re

# Largo maximo del nombre antes de truncar (cabe en una etiqueta de 27 mm).
NAME_MAX_CHARS = 20

# Prefijo entre comillas que agrega Odoo al nombre (ej: '"DTO30%P"').
# Elimina desde la primera comilla hasta la ultima del bloque inicial.
_QUOTED_PREFIX_RE = re.compile(r'^\s*".*"\s*')


def clean_text(text):
    """Quita caracteres que romperian la sintaxis EPL o ZPL."""
    for char in ('"', "^", "~"):
        text = text.replace(char, "")
    return text.strip()


def normalize_price(price):
    """Quita los centavos en cero para que el precio entre mas grande."""
    price = clean_text(price)
    for cents in (",00", ".00"):
        if price.endswith(cents):
            return price[:-3]
    return price


def truncate_name(name):
    """Quita el prefijo entre comillas y trunca el nombre si es largo."""
    name = _QUOTED_PREFIX_RE.sub("", name)
    name = clean_text(name)
    if len(name) > NAME_MAX_CHARS:
        return name[:NAME_MAX_CHARS - 1].rstrip() + "."
    return name


def barcode_digits(barcode):
    """Devuelve solo los digitos de un codigo de barras."""
    return "".join(char for char in barcode if char.isdigit())
