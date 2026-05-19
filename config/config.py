"""Configuracion del impresor de etiquetas Zebra.

Todos los valores son ajustables por variable de entorno o editando los
defaults. Las medidas en dots asumen una impresora de 203 dpi.
"""

import os

# Resolucion del cabezal (203 dpi en GC420t y ZD421-203dpi).
DPI = int(os.getenv("ZEBRA_DPI", "203"))

# --- Geometria del rollo 3-up (etiqueta 30x20 mm, 3 columnas) ---
# Ancho total imprimible de una fila completa (comando EPL "q" / ZPL "^PW").
ROW_WIDTH_DOTS = int(os.getenv("ZEBRA_ROW_WIDTH", "720"))

# Paso horizontal de columna a columna (30 mm a 203 dpi).
COLUMN_PITCH_DOTS = int(os.getenv("ZEBRA_COLUMN_PITCH", "240"))

# Cantidad de columnas por fila.
COLUMNS = int(os.getenv("ZEBRA_COLUMNS", "3"))

# Largo de la etiqueta y espacio entre filas (comando EPL "Q" / ZPL "^LL").
LABEL_HEIGHT_DOTS = int(os.getenv("ZEBRA_LABEL_HEIGHT", "160"))
GAP_V_DOTS = int(os.getenv("ZEBRA_GAP_V", "16"))

# Ancho imprimible de una etiqueta individual (para centrar el contenido).
LABEL_WIDTH_DOTS = int(os.getenv("ZEBRA_LABEL_WIDTH", "216"))
