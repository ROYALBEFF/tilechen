import json
import sys

from PySide6 import QtWidgets

from tilechen.paths import DATA_PATH, PALETTE_DATA_FILEPATH
from tilechen.view.main_window import MainWindow


def initialize_config() -> None:
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    if not PALETTE_DATA_FILEPATH.exists():
        with PALETTE_DATA_FILEPATH.open("w") as f:
            json.dump({}, f)

def run() -> None:
    initialize_config()

    app = QtWidgets.QApplication([])

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    run()
