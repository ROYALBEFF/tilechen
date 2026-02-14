from PySide6 import QtCore, QtGui, QtWidgets


class Minimap(QtWidgets.QWidget):
    def __init__(self, scroll_area: QtWidgets.QScrollArea) -> None:
        super().__init__()
        self.scroll_area = scroll_area
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.update_rubber_band_position)

        self.minimap_image = QtWidgets.QLabel()
        self.tilemap_pixmap = None
        self.scaled_tilemap_pixmap = None

        self.rubber_band = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Shape.Rectangle, self)
        self.rubber_band_height = 0
        self.rubber_band.setFixedHeight(self.rubber_band_height)
        self.rubber_band.setFixedWidth(140)

        self.setFixedWidth(140)
        self.setMinimumHeight(200)

        self._is_clicked = False

    def set_minimap_image(self, pixmap: QtGui.QPixmap) -> None:
        self.tilemap_pixmap = pixmap
        self.scaled_tilemap_pixmap = self.tilemap_pixmap.scaled(
            self.width(),
            self.height(),
            QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        self.minimap_image.setPixmap(self.scaled_tilemap_pixmap)

        relative_rubber_band_height = self.scroll_area.viewport().height() / self.tilemap_pixmap.height()
        self.rubber_band_height = int(self.height() * relative_rubber_band_height)
        self.rubber_band.setFixedHeight(self.rubber_band_height)
        self.rubber_band.show()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:  # noqa: ARG002, N802
        if self.scaled_tilemap_pixmap is not None:
            QtGui.QPainter(self).drawPixmap(0, 0, self.scaled_tilemap_pixmap)

    def update_rubber_band_position(self, scroll_bar_position: int) -> None:
        if self.tilemap_pixmap is not None and not self._is_clicked:
            relative_scroll_bar_position = scroll_bar_position / self.tilemap_pixmap.height()

            rubber_band_top_position_y = relative_scroll_bar_position * self.height()
            rubber_band_top_position_y = min(rubber_band_top_position_y, self.height() - 0.5 * self.rubber_band_height)
            rubber_band_center_position_y = int(rubber_band_top_position_y + 0.5 * self.rubber_band_height)
            self.move_rubber_band(rubber_band_center_position_y)

    def scroll_to_selction(self) -> None:
        if self.tilemap_pixmap is not None:
            rubber_band_position = self.rubber_band.pos()
            relative_rubber_band_position = rubber_band_position.y() / self.height()
            scroll_position = self.tilemap_pixmap.height() * relative_rubber_band_position
            self.scroll_area.verticalScrollBar().setValue(int(scroll_position))

    def move_rubber_band(self, y_rubber_band_center: int) -> None:
        y_rubber_band_top = max(y_rubber_band_center - 0.5 * self.rubber_band_height, 0)
        y_rubber_band_top = min(y_rubber_band_top, self.height() - self.rubber_band_height)
        self.rubber_band.move(0, int(y_rubber_band_top))

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: N802
        self._is_clicked = True
        self.move_rubber_band(event.pos().y())
        self.scroll_to_selction()

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: ARG002, N802
        self._is_clicked = False

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: N802
        if self._is_clicked:
            self.move_rubber_band(event.pos().y())
            self.scroll_to_selction()

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:  # noqa: ARG002, N802
        if self.tilemap_pixmap is not None:
            self.set_minimap_image(self.tilemap_pixmap)
