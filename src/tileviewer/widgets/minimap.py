from PySide6 import QtCore, QtGui, QtWidgets


class Minimap(QtWidgets.QWidget):
    def __init__(self, scroll_area: QtWidgets.QScrollArea) -> None:
        super().__init__()
        self.scroll_area = scroll_area

        self.image_preview = QtWidgets.QLabel()
        self.tilemap_pixmap = None
        self.scaled_tilemap_pixmap = None

        self.rubberband = QtWidgets.QRubberBand(QtWidgets.QRubberBand.Shape.Rectangle, self)

        self.rubberband_height = 0
        self.rubberband.setFixedHeight(self.rubberband_height)
        self.rubberband.setFixedWidth(140)

        self.setFixedWidth(140)
        self.setMinimumHeight(200)

        # TODO connect to function that oves rubberband
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.update)
        self.scroll_area.horizontalScrollBar().valueChanged.connect(self.update)

        self._is_clicked = False

    def set_preview(self, pixmap: QtGui.QPixmap) -> None:
        self.tilemap_pixmap = pixmap
        self.scaled_tilemap_pixmap = self.tilemap_pixmap.scaled(
            self.width(),
            self.height(),
            QtCore.Qt.AspectRatioMode.IgnoreAspectRatio,
            QtCore.Qt.TransformationMode.SmoothTransformation
        )
        self.image_preview.setPixmap(self.scaled_tilemap_pixmap)

        relative_rubberband_height = self.scroll_area.viewport().height() / self.tilemap_pixmap.height()
        self.rubberband_height = int(self.height() * relative_rubberband_height)
        self.rubberband.setFixedHeight(self.rubberband_height)
        self.rubberband.show()

    def paintEvent(self, event: QtGui.QPaintEvent) -> None:  # noqa: ARG002, N802
        if self.scaled_tilemap_pixmap is not None:
            painter = QtGui.QPainter(self)
            painter.drawPixmap(0, 0, self.scaled_tilemap_pixmap)

    def scroll_to_selction(self) -> None:
        if self.tilemap_pixmap is not None:
            rubberband_position = self.rubberband.pos()
            relative_rubberband_position = rubberband_position.y() / self.height()
            scroll_position = self.tilemap_pixmap.height() * relative_rubberband_position
            self.scroll_area.verticalScrollBar().setValue(int(scroll_position))

    def update_selection_rectanlge_position(self, position: QtCore.QPoint) -> None:
        y = max(position.y() - 0.5 * self.rubberband_height, 0)
        y = min(y, self.height() - self.rubberband_height)
        position.setY(int(y))

        position.setX(0)
        self.rubberband.move(position)
        self.scroll_to_selction()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: N802
        self._is_clicked = True
        self.update_selection_rectanlge_position(event.pos())

    def mouseReleaseEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: ARG002, N802
        self._is_clicked = False

    def mouseMoveEvent(self, event: QtGui.QMouseEvent) -> None:  # noqa: N802
        if self._is_clicked:
            self.update_selection_rectanlge_position(event.pos())

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:  # noqa: ARG002, N802
        if self.tilemap_pixmap is not None:
            self.set_preview(self.tilemap_pixmap)
