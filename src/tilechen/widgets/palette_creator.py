from PySide6 import QtCore, QtGui, QtWidgets

from tilechen.palettes import DEFAULT_PALETTE
from tilechen.widgets.color_button import ColorButton


class PaletteCreator(QtWidgets.QColorDialog):

    def __init__(self) -> None:
        super().__init__()
        self.setOption(QtWidgets.QColorDialog.ColorDialogOption.NoEyeDropperButton, True)
        self.setOption(QtWidgets.QColorDialog.ColorDialogOption.ShowAlphaChannel, False)
        self.setOption(QtWidgets.QColorDialog.ColorDialogOption.DontUseNativeDialog, True)
 
        self.colors = [QtGui.QColor(*color) for color in DEFAULT_PALETTE]
        self.color_buttons = [ColorButton(color) for color in self.colors]

        for color_button in self.color_buttons:
            self.layout().addWidget(color_button)

        # TODO make dialog nicer. Remove unnecessary parts!

