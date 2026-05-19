"""Generacion de etiquetas en lenguaje EPL (Zebra GC420t y similares)."""

from config import config
from modules.label_text import (
    barcode_digits,
    clean_text,
    normalize_price,
    truncate_name,
)

# Posiciones dentro de una etiqueta, en dots (relativas a la columna).
_BARCODE_X = 8
_BARCODE_Y = 4
_TEXT_X = 14
_NAME_Y = 72
_PRICE_Y = 95

# Hasta esta longitud el precio se imprime en doble ancho.
_PRICE_WIDE_MAX_CHARS = 8


def row_header():
    """Comandos EPL que abren una fila de etiquetas."""
    return (
        "N\r\n"
        f"q{config.ROW_WIDTH_DOTS}\r\n"
        f"Q{config.LABEL_HEIGHT_DOTS},{config.GAP_V_DOTS}\r\n"
    )


def row_footer():
    """Comando EPL que imprime la fila."""
    return "P1\r\n"


def build_label(label, x):
    """Comandos EPL de una etiqueta en la columna que inicia en x."""
    return (
        _barcode(label["barcode"], x)
        + _name(label["name"], x)
        + _price(label["price"], x)
    )


def _barcode(barcode, x):
    digits = barcode_digits(barcode)
    bx = x + _BARCODE_X
    if len(digits) >= 12:
        # E30 = EAN-13; usa 12 digitos, el 13ro es verificador calculado.
        return f'B{bx},{_BARCODE_Y},0,E30,2,2,40,B,"{digits[:12]}"\r\n'
    # Sin un EAN valido se cae a Code 128.
    data = clean_text(barcode) or "0"
    return f'B{bx},{_BARCODE_Y},0,1,2,2,40,B,"{data}"\r\n'


def _name(name, x):
    return f'A{x + _TEXT_X},{_NAME_Y},0,2,1,1,N,"{truncate_name(name)}"\r\n'


def _price(price, x):
    text = normalize_price(price)
    h_mult = 2 if len(text) <= _PRICE_WIDE_MAX_CHARS else 1
    return f'A{x + _TEXT_X},{_PRICE_Y},0,3,{h_mult},2,N,"{text}"\r\n'
