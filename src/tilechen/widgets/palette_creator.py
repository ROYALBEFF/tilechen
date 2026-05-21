from PySide6 import QtCore, QtGui, QtWidgets

from tilechen.model.palettes import (
    PRE_DEFINED_PALETTES,
    ColorPalette,
    create_color_palette,
    save_color_palette,
)
from tilechen.widgets.color_button import ColorButton


class PaletteCreator(QtWidgets.QColorDialog):

    palette_added = QtCore.Signal(str, object)

    def __init__(self, available_palettes: dict[str, ColorPalette], selected_palette: str) -> None:
        super().__init__()
        self.available_palettes = available_palettes

        self.setOption(QtWidgets.QColorDialog.ColorDialogOption.NoEyeDropperButton, True)
        self.setOption(QtWidgets.QColorDialog.ColorDialogOption.ShowAlphaChannel, False)
        self.setOption(QtWidgets.QColorDialog.ColorDialogOption.DontUseNativeDialog, True)
        self.setOption(QtWidgets.QColorDialog.ColorDialogOption.NoButtons, True)

        self.button_group = QtWidgets.QWidget()
        self.button_layout = QtWidgets.QHBoxLayout(self.button_group)

        self.color_labels = ["Black", "Light grey", "Dark grey", "White"]
        self.default_colors = [QtGui.QColor(*color) for color in self.available_palettes[selected_palette]]
        self.color_buttons = [
            ColorButton(label, color) for label, color in zip(self.color_labels, self.default_colors, strict=False)
        ]

        for color_button in self.color_buttons:
            self.button_layout.addWidget(color_button)
            color_button.clicked.connect(self.set_selected_color_button)

        self.store_color_palette = QtWidgets.QWidget()
        self.store_color_palette_layout = QtWidgets.QHBoxLayout(self.store_color_palette)

        self.palette_name_text_field = QtWidgets.QLineEdit()
        self.palette_name_text_field.setText(selected_palette)

        self.cancel_button = QtWidgets.QPushButton()
        self.cancel_button.setText("Cancel")
        self.cancel_button.clicked.connect(self.close_dialog)

        self.save_button = QtWidgets.QPushButton()
        self.save_button.setText("Save")
        self.save_button.clicked.connect(self.save)

        self.store_color_palette_layout.addWidget(self.palette_name_text_field)
        self.store_color_palette_layout.addWidget(self.save_button)
        self.store_color_palette_layout.addWidget(self.cancel_button)

        self.layout().addWidget(self.button_group)
        self.layout().addWidget(self.store_color_palette)

        self.selected_color_button = self.color_buttons[0]
        self.setCurrentColor(self.selected_color_button.color)

        self.currentColorChanged.connect(self.update_selected_color_button)

    def set_selected_color_button(self) -> None:
        self.selected_color_button = self.sender()
        self.setCurrentColor(self.selected_color_button.color)

    def update_selected_color_button(self) -> None:
        self.selected_color_button.set_color(self.currentColor())

    def save(self) -> None:
        palette_name = self.palette_name_text_field.text()
        if len(palette_name) == 0:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setText("Unable to save color palette!")
            msg_box.setInformativeText("You must specify a palette name before saving.")
            msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg_box.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msg_box.exec()
            return

        if palette_name in PRE_DEFINED_PALETTES:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setText("Unable to save color palette!")
            msg_box.setInformativeText("You cannot overwrite predefined color palettes.")
            msg_box.setStandardButtons(QtWidgets.QMessageBox.StandardButton.Ok)
            msg_box.setDefaultButton(QtWidgets.QMessageBox.Ok)
            msg_box.exec()
            return

        color_palette = create_color_palette(*(btn.color.rgb() for btn in self.color_buttons))
        overwrite = False
        if palette_name in self.available_palettes:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setText("Palette name is already taken!")
            msg_box.setInformativeText("Do you want to replace the existing color palette?")
            msg_box.setStandardButtons(
                QtWidgets.QMessageBox.StandardButton.Yes | QtWidgets.QMessageBox.StandardButton.No
            )
            msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
            decision = msg_box.exec()

            if decision == QtWidgets.QMessageBox.StandardButton.Yes:
                overwrite = True

        save_color_palette(palette_name, color_palette, overwrite)
        self.palette_added.emit(palette_name, color_palette)
        self.close()

    def close_dialog(self) -> None:
        self.close()
