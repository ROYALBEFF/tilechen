import json
import sys

from PySide6 import QtWidgets

from tilechen.paths import DATA_PATH, PALETTE_DATA_FILEPATH
from tilechen.view.main_window import MainWindow


def initialize_palette_json() -> None:
    DATA_PATH.mkdir(parents=True, exist_ok=True)
    if not PALETTE_DATA_FILEPATH.exists():
        with PALETTE_DATA_FILEPATH.open("w") as f:
            json.dump({}, f)

def validate_palette_json() -> bool:
    try:
        with PALETTE_DATA_FILEPATH.open("r") as f:
            json.load(f)
        return True
    except json.JSONDecodeError:
        return False

def run() -> None:
    initialize_palette_json()

    app = QtWidgets.QApplication([])

    if not validate_palette_json():
        msg_box = QtWidgets.QMessageBox()
        msg_box.setText("Unable to load color palettes!")
        msg_box.setInformativeText(
            f"The color palettes file {PALETTE_DATA_FILEPATH} is not a valid JSON file. Should it be removed? "
            "All custom color palettes will be lost!"
        )
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
        decision = msg_box.exec()

        match decision:
            case QtWidgets.QMessageBox.Yes:
                PALETTE_DATA_FILEPATH.unlink()
                initialize_palette_json()
            case QtWidgets.QMessageBox.No:
                sys.exit(1)

    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    run()
