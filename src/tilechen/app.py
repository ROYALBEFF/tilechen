import sys

from PySide6 import QtWidgets

from tilechen.view.main_window import MainWindow


def run() -> None:
    app = QtWidgets.QApplication([])

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()
