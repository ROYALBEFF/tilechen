from pathlib import Path

from PySide6 import QtCore, QtGui, QtWidgets

from tilechen.constants import COLOR_CHANNELS, SCALED_IMG_WIDTH
from tilechen.model.tilemap import TileMap
from tilechen.palettes import (
    DEFAULT_PALETTE,
    PRE_DEFINED_PALETTES,
    ColorPalette,
    load_available_palettes,
    remove_color_palette,
)
from tilechen.widgets.minimap import Minimap
from tilechen.widgets.palette_creator import PaletteCreator


class MainWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.select_rom_button = QtWidgets.QPushButton("Select ROM")

        self.color_palettes = load_available_palettes()
        self.selected_color_palette_name = "default"
        self.selected_color_palette = DEFAULT_PALETTE

        self.palette_selection_dropdown = QtWidgets.QComboBox()
        self.palette_selection_dropdown.addItems(tuple(self.color_palettes.keys()))

        self.add_color_palette_button = QtWidgets.QPushButton("Add/Edit palette")
        self.delete_color_palette_button = QtWidgets.QPushButton("Delete palette")

        self.rom_file_dialog = QtWidgets.QFileDialog()
        self.rom_file_dialog.setNameFilter("*.gb")
        self.rom_file_dialog.setFileMode(QtWidgets.QFileDialog.FileMode.ExistingFile)

        self.tilemap_scroll_area = QtWidgets.QScrollArea()
        self.tilemap_scroll_area.setWidgetResizable(True)
        self.tilemap_image = QtWidgets.QLabel()
        self.tilemap = None

        self.vertical_layout = QtWidgets.QVBoxLayout(self)
        self.button_group = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self)

        self.vertical_layout.addLayout(self.button_group)
        self.vertical_layout.addLayout(self.horizontal_layout)

        self.horizontal_layout.addWidget(self.tilemap_scroll_area)
        self.minimap = Minimap(self.tilemap_scroll_area)
        self.horizontal_layout.addWidget(self.minimap)

        self.button_group.addWidget(self.select_rom_button)
        self.button_group.addWidget(self.palette_selection_dropdown)
        self.button_group.addWidget(self.add_color_palette_button)
        self.button_group.addWidget(self.delete_color_palette_button)

        self.select_rom_button.clicked.connect(self.rom_file_dialog.open)
        self.palette_selection_dropdown.currentTextChanged.connect(self.select_palette)
        self.add_color_palette_button.clicked.connect(self.create_palette)
        self.delete_color_palette_button.clicked.connect(self.remove_palette)
        self.rom_file_dialog.accepted.connect(self.read_rom_file)

    @QtCore.Slot()
    def read_rom_file(self) -> None:
        selected_files = self.rom_file_dialog.selectedFiles()
        assert len(selected_files) == 1

        selected_file = Path(selected_files[0])
        self.tilemap = TileMap.read_rom(selected_file)
        self.set_tilemap_image()

    def set_tilemap_image(self) -> None:
        assert self.tilemap is not None
        rgb_tilemap = self.tilemap.to_rgb(self.selected_color_palette)
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

        self.minimap.set_minimap_image(pixmap)

    @QtCore.Slot()
    def select_palette(self, palette_key: str) -> None:
        self.selected_color_palette_name = palette_key
        self.selected_color_palette = self.color_palettes[palette_key]
        if self.tilemap is not None:
            self.set_tilemap_image()

    @QtCore.Slot()
    def create_palette(self) -> None:
        self.palette_creator = PaletteCreator(self.color_palettes, self.selected_color_palette_name)
        self.palette_creator.palette_added.connect(self.update_available_palettes)
        self.palette_creator.show()

    def remove_palette(self) -> None:
        if self.selected_color_palette_name in PRE_DEFINED_PALETTES:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setText(f"Unable to delete color palette {self.selected_color_palette_name}!")
            msg_box.setInformativeText("Pre-defined color palettes cannot be deleted.")
            msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg_box.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msg_box.exec()
            return

        msg_box = QtWidgets.QMessageBox()
        msg_box.setText(f"Color palette {self.selected_color_palette_name} will be deleted. Are you sure?")
        msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
        decision = msg_box.exec()

        print(self.selected_color_palette_name)
        if decision == QtWidgets.QMessageBox.Yes:
            remove_color_palette(self.selected_color_palette_name)
            del self.color_palettes[self.selected_color_palette_name]
            self.palette_selection_dropdown.removeItem(self.palette_selection_dropdown.currentIndex())
            self.palette_selection_dropdown.setCurrentIndex(0)

            print(self.color_palettes.keys())
            print()
            for i in range(self.palette_selection_dropdown.count()):
                print(i, self.palette_selection_dropdown.itemText(i))


    @QtCore.Slot()
    def update_available_palettes(self, palette_name: str, color_palette: ColorPalette) -> None:
        overwritten_palette = palette_name in self.color_palettes
        if not overwritten_palette:
            self.palette_selection_dropdown.addItem(palette_name)

        self.color_palettes[palette_name] = color_palette

        # redraw image if currently selected color palette was overwritten
        if overwritten_palette and self.selected_color_palette_name == palette_name:
            self.select_palette(palette_name)
