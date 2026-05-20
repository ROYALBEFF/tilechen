from PySide6 import QtCore, QtGui, QtWidgets


class ColorButton(QtWidgets.QPushButton):
    def __init__(self, label: str | None, color: QtGui.QColor | None = None) -> None:
        super().__init__()

        if color is None:
            color = QtGui.QColor(0x000000)

        self.icon_size = QtCore.QSize(32, 32)
        self.set_color(color)

        if label is not None:
            self.setText(label)

    def set_color(self, color: QtGui.QColor):
        self.color = color
        color_preview = QtGui.QPixmap(self.icon_size)
        color_preview.fill(self.color)
        self.color_icon = QtGui.QIcon(color_preview)
        self.setIcon(self.color_icon)
