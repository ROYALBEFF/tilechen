from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets

from tileviewer.constants import COLOR_CHANNELS, SCALED_IMG_WIDTH
from tileviewer.model.tilemap import TileMap


class MainWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.select_rom_button = QtWidgets.QPushButton("Select ROM")

        self.rom_file_dialog = QtWidgets.QFileDialog()
        self.rom_file_dialog.setNameFilter("*.gb")
        self.rom_file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)

        self.tilemap_scroll_area = QtWidgets.QScrollArea()
        self.tilemap_scroll_area.setWidgetResizable(False)
        self.tilemap_image = QtWidgets.QLabel()

        self.box_layout = QtWidgets.QVBoxLayout(self)
        self.box_layout.addWidget(self.tilemap_scroll_area)
        self.box_layout.addWidget(self.select_rom_button)

        self.select_rom_button.clicked.connect(self.rom_file_dialog.open)
        self.rom_file_dialog.accepted.connect(self.read_rom_file)

    @QtCore.Slot()
    def read_rom_file(self) -> None:
        selected_files = self.rom_file_dialog.selectedFiles()
        selected_file = Path(selected_files[0])
        tilemap = TileMap.read_rom(selected_file)

        rgb_tilemap = tilemap.to_rgb()
        img_width = rgb_tilemap.shape[1]
        img_height = rgb_tilemap.shape[0]
        bytes_per_image_row = img_width * COLOR_CHANNELS

        img = QtGui.QImage(
            rgb_tilemap.data,
            img_width,
            img_height,
            bytes_per_image_row,
            QtGui.QImage.Format.Format_RGB888
        )

        pixmap = QtGui.QPixmap.fromImage(img)
        pixmap = pixmap.scaledToWidth(SCALED_IMG_WIDTH)

        self.tilemap_image.setPixmap(pixmap)
        self.tilemap_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)
        self.tilemap_image.setAlignment(QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignHCenter)

        self.tilemap_scroll_area.setWidget(self.tilemap_image)
