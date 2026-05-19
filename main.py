"""Punto de entrada del impresor de etiquetas Zebra."""

from modules.gui import LabelPrinterApp


def main():
    app = LabelPrinterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
