"""Armado del trabajo de impresion en disposicion 3-up."""

from config import config
from modules import epl_label, zpl_label

# Generador de etiquetas por lenguaje de impresora.
_RENDERERS = {
    "epl": epl_label,
    "zpl": zpl_label,
}


def build_print_job(labels, language, print_price=True):
    """Construye el flujo de impresion completo para el lenguaje dado.

    Las etiquetas se agrupan en filas de COLUMNS columnas. Cada fila es una
    etiqueta logica con una cabecera, una etiqueta por columna y un cierre.

    Args:
        labels: lista de dicts con 'barcode', 'name' y 'price'.
        language: 'epl' o 'zpl'.

    Returns:
        bytes con el flujo listo para enviar a la impresora.

    Raises:
        ValueError: si no hay etiquetas o el lenguaje es desconocido.
    """
    if not labels:
        raise ValueError("No hay etiquetas para imprimir.")

    renderer = _RENDERERS.get(language)
    if renderer is None:
        raise ValueError(f"Lenguaje de impresora desconocido: {language}")

    rows = [
        labels[i:i + config.COLUMNS]
        for i in range(0, len(labels), config.COLUMNS)
    ]

    parts = []
    for row in rows:
        parts.append(renderer.row_header())
        for col_index, label in enumerate(row):
            x = col_index * config.COLUMN_PITCH_DOTS
            parts.append(renderer.build_label(label, x, print_price=print_price))
        parts.append(renderer.row_footer())

    print(
        f"Trabajo {language.upper()} armado: "
        f"{len(labels)} etiqueta(s) en {len(rows)} fila(s)"
    )
    return "".join(parts).encode("ascii", errors="replace")
