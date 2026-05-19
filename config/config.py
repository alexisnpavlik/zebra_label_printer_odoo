"""Configuracion del impresor de etiquetas Zebra.

Todos los valores son ajustables por variable de entorno o editando los
defaults. Las medidas en dots asumen una impresora de 203 dpi.
"""

import os

# Resolucion del cabezal (203 dpi en GC420t y ZD421-203dpi).
DPI = int(os.getenv("ZEBRA_DPI", "203"))

# --- Geometria del rollo 3-up (etiqueta 29x20 mm, 3 columnas, gap 2 mm) ---
# Ancho total imprimible de una fila completa (comando EPL "q" / ZPL "^PW").
# 91 mm utiles x 7.992 = 728 dots.
ROW_WIDTH_DOTS = int(os.getenv("ZEBRA_ROW_WIDTH", "728"))

# Paso horizontal de columna a columna (etiqueta 29 mm + gap 2 mm = 31 mm).
# 31 mm x 7.992 = 248 dots.
COLUMN_PITCH_DOTS = int(os.getenv("ZEBRA_COLUMN_PITCH", "248"))

# Cantidad de columnas por fila.
COLUMNS = int(os.getenv("ZEBRA_COLUMNS", "3"))

# Largo de la etiqueta y espacio entre filas (comando EPL "Q" / ZPL "^LL").
LABEL_HEIGHT_DOTS = int(os.getenv("ZEBRA_LABEL_HEIGHT", "160"))
GAP_V_DOTS = int(os.getenv("ZEBRA_GAP_V", "16"))

# Ancho imprimible de una etiqueta individual (para centrar el contenido).
# 29 mm x 7.992 = 232 dots.
LABEL_WIDTH_DOTS = int(os.getenv("ZEBRA_LABEL_WIDTH", "232"))
