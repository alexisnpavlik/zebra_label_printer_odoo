# Diseño: Toggle para imprimir número de código de barras

**Fecha:** 2026-05-27  
**Alcance:** app_zebra + app_brother

---

## Resumen

Agregar un checkbox en la interfaz gráfica de ambas apps para controlar si se imprime el número (dígitos legibles) debajo del código de barras. Desactivado por defecto. Sigue el mismo patrón que el checkbox "Imprimir precio" ya existente.

---

## GUI (ambas apps)

Agregar un nuevo `CTkCheckBox` debajo del checkbox de precio:

```python
self.print_barcode_number_var = ctk.BooleanVar(value=False)
ctk.CTkCheckBox(
    self,
    text="Imprimir número de código de barras",
    variable=self.print_barcode_number_var,
).pack(pady=(4, 0))
```

**app_zebra:** sin persistencia (igual que `print_price` en esa app).  
**app_brother:** persistir en `brother_settings.json` junto a `print_price`, con `command=self._save_settings`.

---

## app_zebra — cadena de parámetros

### `gui.py`
- Declarar `self.print_barcode_number_var = ctk.BooleanVar(value=False)`.
- En `_print`: pasar `print_barcode_number=self.print_barcode_number_var.get()` a `build_print_job`.

### `label_layout.py`
- `build_print_job(labels, language, print_price=True, print_barcode_number=True)`
- Pasar `print_barcode_number` a `renderer.build_label`.

### `zpl_label.py`
- `build_label(label, x, print_price=True, print_barcode_number=True)`
- `_barcode(barcode, x, print_barcode_number=True)`
- EAN-13: `^BEN,40,Y,N` → la `Y` se reemplaza por `"Y" if print_barcode_number else "N"`.
- Code 128: `^BCN,40,Y,N,N` → igual para el tercer parámetro.

### `epl_label.py`
- `build_label(label, x, print_price=True, print_barcode_number=True)`
- `_barcode(barcode, x, print_barcode_number=True)`
- EAN-13 y Code 128: el carácter `B` (human readable below) al final del comando `B...` se reemplaza por `"B" if print_barcode_number else "N"`.

---

## app_brother — manipulación de PDF

### `gui.py` — `_load_settings` / `_save_settings`
- Cargar: `self.saved_print_barcode_number = data.get("print_barcode_number", False)`
- Guardar: incluir `"print_barcode_number": self.print_barcode_number_var.get()` en el dict.

### `gui.py` — `_build_widgets`
- Inicializar `self.print_barcode_number_var = ctk.BooleanVar(value=self.saved_print_barcode_number)`.
- Agregar checkbox con `command=self._save_settings`.

### `gui.py` — `_print`
- Pasar `print_barcode_number=self.print_barcode_number_var.get()` y `labels=self.labels` a `_prepare_pdf_for_printing`.

### `gui.py` — `_prepare_pdf_for_printing`
- Firma: `_prepare_pdf_for_printing(self, original_pdf_path, print_price, labels=None, print_barcode_number=True)`
- Para cada página `i`: si `not print_barcode_number` y `labels` tiene `labels[i]['barcode']`, usar `page.search_for(labels[i]['barcode'])` y cubrir cada rect encontrado con rectángulo blanco (mismo patrón que el precio).

---

## Invariantes

- Valor por defecto `False` en ambas apps (no imprime el número de barras por defecto).
- No rompe comportamiento existente: todos los parámetros nuevos tienen defaults `True` en los renderers ZPL/EPL para no afectar código que los llame sin el parámetro.
- app_brother: si `labels` es `None` o el barcode está vacío, se omite la supresión silenciosamente.
