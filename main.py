"""Punto de entrada del impresor de etiquetas Zebra."""

from zebra_label_printer_odoo.modules.gui import LabelPrinterApp


def main():
    app = LabelPrinterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
