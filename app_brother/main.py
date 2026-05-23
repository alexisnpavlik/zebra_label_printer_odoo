"""Punto de entrada del impresor de etiquetas Brother QL-800."""

from modules.gui import BrotherLabelPrinterApp


def main():
    app = BrotherLabelPrinterApp()
    app.mainloop()


if __name__ == "__main__":
    main()
