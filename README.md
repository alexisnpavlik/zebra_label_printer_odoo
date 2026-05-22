# Impresor de Etiquetas Zebra

Aplicación de escritorio para imprimir etiquetas de productos en impresoras Zebra desde archivos PDF o TXT (ZPL) exportados de Odoo.

Soporta etiquetas de 3 columnas (formato 29×20 mm) en lenguaje **EPL** (GC420t y similares) y **ZPL** (ZD421 y similares).

---

## Características

- Carga archivos PDF (exportados de Odoo) o TXT con comandos ZPL directos
- Detecta automáticamente las impresoras disponibles en CUPS
- Vista previa de la primera etiqueta antes de imprimir
- Opción para incluir o excluir el precio en la etiqueta
- Empaquetable como ejecutable standalone con PyInstaller

---

## Requisitos

- Python 3.10+
- CUPS instalado y con la impresora Zebra configurada
- Dependencias Python (ver `requirements.txt`)

---

## Instalación

```bash
pip install -r requirements.txt
```

---

## Uso

```bash
python main.py
```

1. Seleccioná la impresora en el desplegable (o hacé clic en **Actualizar**)
2. Cargá un archivo PDF o TXT con **Cargar PDF / TXT**
3. Verificá la vista previa
4. Marcá **Imprimir precio** si querés incluirlo en la etiqueta (desmarcado por defecto)
5. Hacé clic en **Imprimir**

---

## Configuración

Todos los parámetros de geometría se pueden ajustar por variable de entorno sin tocar el código:

| Variable              | Descripción                              | Default |
|-----------------------|------------------------------------------|---------|
| `ZEBRA_DPI`           | Resolución del cabezal (dpi)             | `203`   |
| `ZEBRA_ROW_WIDTH`     | Ancho total imprimible de una fila (dots)| `728`   |
| `ZEBRA_COLUMN_PITCH`  | Paso horizontal entre columnas (dots)    | `248`   |
| `ZEBRA_COLUMNS`       | Cantidad de columnas por fila            | `3`     |
| `ZEBRA_LABEL_HEIGHT`  | Alto de etiqueta (dots)                  | `160`   |
| `ZEBRA_GAP_V`         | Espacio vertical entre filas (dots)      | `16`    |
| `ZEBRA_LABEL_WIDTH`   | Ancho de una etiqueta individual (dots)  | `232`   |

Los defaults corresponden a etiquetas de 29×20 mm en impresora de 203 dpi.

---

## Generar ejecutable

```bash
python build.py
```

El ejecutable queda en `dist/ZebraLabelPrinter` (Linux/Mac) o `dist/ZebraLabelPrinter.exe` (Windows).

---

## Estructura del proyecto

```
├── main.py              # Punto de entrada
├── build.py             # Script de empaquetado con PyInstaller
├── requirements.txt
├── config/
│   └── config.py        # Parámetros de geometría (env vars)
└── modules/
    ├── gui.py           # Interfaz gráfica (customtkinter)
    ├── pdf_extract.py   # Extracción de datos desde PDF
    ├── txt_extract.py   # Lectura de archivos TXT/ZPL
    ├── label_layout.py  # Armado del trabajo de impresión (3-up)
    ├── label_text.py    # Normalización de texto y precios
    ├── zpl_label.py     # Generación de comandos ZPL
    ├── epl_label.py     # Generación de comandos EPL
    └── printer.py       # Comunicación con CUPS
```
