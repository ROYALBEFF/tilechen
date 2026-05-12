from PySide6 import QtCore, QtGui, QtWidgets


class ColorButton(QtWidgets.QPushButton):
    def __init__(self, color: QtGui.QColor | None = None) -> None:
        super().__init__()

        self.color = color
        if self.color is None:
            self.color = QtGui.QColor(0x000000)

        icon_size = QtCore.QSize(16, 16)
        color_preview = QtGui.QPixmap(icon_size)
        color_preview.fill(self.color)
        self.color_icon = QtGui.QIcon(color_preview)

        self.setIcon(self.color_icon)
        self.setFixedSize(icon_size)
