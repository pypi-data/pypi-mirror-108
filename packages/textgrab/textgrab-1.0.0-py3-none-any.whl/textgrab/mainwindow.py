# Copyright (C) 2021 PowerSnail
#
# This file is part of textgrab.
#
# textgrab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# textgrab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with textgrab.  If not, see <http://www.gnu.org/licenses/>.

import os
import pathlib
import tempfile
import typing as T

import pytesseract
from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt

from . import crop_mask_item, ui_mainwindow


def _default_picture_dir():
    default_paths = QtCore.QStandardPaths.standardLocations(QtCore.QStandardPaths.PicturesLocation)
    if default_paths:
        return default_paths[0]
    return "./"


class MainWindow(QtWidgets.QMainWindow, ui_mainwindow.Ui_MainWindow):

    image_changed = QtCore.Signal(QtGui.QPixmap)
    text_ready = QtCore.Signal(str)

    open_dir: str = _default_picture_dir()

    def __init__(
        self, parent: T.Optional[QtWidgets.QWidget] = None, flags: Qt.WindowFlags = Qt.WindowFlags(),
    ):
        super().__init__(parent=parent, flags=flags)
        self.setupUi(self)

        self.clipboard = QtGui.QClipboard()

        self.scene = QtWidgets.QGraphicsScene()
        self.crop_item = crop_mask_item.CropTool()

        self.overlay_label = QtWidgets.QLabel("Processing", self.text_edit)
        self.overlay_label.setVisible(False)

        self.ocr_thread = QtCore.QThread(self)
        self.ocr_worker = OCRWorker()
        self.setup_signals()
        self.setup_graphics_view()

        self.ocr_worker.moveToThread(self.ocr_thread)
        self.ocr_thread.start()

    def __del__(self):
        self.ocr_thread.exit(0)
        self.ocr_thread.wait()

    def setup_signals(self):
        self.action_grab_from_clipboard.triggered.connect(self.grab_image_from_clipboard)
        self.action_open.triggered.connect(self.open_image)
        self.action_screenshot.triggered.connect(self.screenshot)
        self.image_changed.connect(self.ocr_worker.ocr_to_string)
        self.ocr_worker.text_ready.connect(self.on_text_ready)
        self.ocr_worker.ocr_started.connect(self.on_task_started)
        self.crop_item.cropped_pixmap_changed.connect(self.on_cropped_pixmap_changed)

    def setup_graphics_view(self):
        self.graphics_view.setBackgroundBrush(Qt.black)
        self.graphics_view.setScene(self.scene)
        self.graphics_view.setRenderHint(QtGui.QPainter.SmoothPixmapTransform, True)
        self.graphics_view.setRenderHint(QtGui.QPainter.Antialiasing, True)
        self.scene.setBackgroundBrush(Qt.black)
        self.scene.addItem(self.crop_item.pixmap_item)

    def set_pixmap(self, pixmap: QtGui.QPixmap):
        self.crop_item.set_pixmap(pixmap)
        self.scene.setSceneRect(self.crop_item.pixmap_item.boundingRect())
        self.graphics_view.fitInView(self.crop_item.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        self.graphics_view.centerOn(self.crop_item.pixmap_item)
        self.crop_item.set_rendered_scale(self.graphics_view.transform().m11())

    def resizeEvent(self, _):
        self.graphics_view.fitInView(self.crop_item.pixmap_item, Qt.AspectRatioMode.KeepAspectRatio)
        self.crop_item.set_rendered_scale(self.graphics_view.transform().m11())

    @QtCore.Slot()
    def grab_image_from_clipboard(self):
        pixmap = self.clipboard.pixmap()
        if pixmap.isNull():
            QtWidgets.QMessageBox.warning(self, "Failed to paste image", "No supported image on clipboard")
            return
        self.set_pixmap(pixmap)

    @QtCore.Slot()
    def open_image(self):
        file, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, self.tr("Open Image..."), dir=self.open_dir, filter=self.tr("Image Files (*.png *.jpg *.jpeg *.bmp)"),
        )
        if not file:
            return

        pixmap = QtGui.QPixmap(file)
        if pixmap.isNull():
            QtWidgets.QMessageBox.warning(self, "Failed to open image", "Error reading the image file " + file)
        self.set_pixmap(pixmap)
        self.open_dir = str(pathlib.Path(file).parent.absolute())

    @QtCore.Slot()
    def screenshot(self):
        window = self.windowHandle()
        screen = window.screen()
        pixmap = screen.grabWindow(0)
        pixmap.setDevicePixelRatio(1.0)  # Workaround for QGraphicsPixmapItem's bug of not taking DPI into account

        if pixmap.isNull():
            QtWidgets.QMessageBox.warning(self, "Failed to grab screenshot")
        self.set_pixmap(pixmap)

    @QtCore.Slot(str)
    def on_text_ready(self, message: str):
        self.overlay_label.close()
        self.text_edit.setEnabled(True)
        self.text_edit.setPlainText(message)

    @QtCore.Slot()
    def on_task_started(self):
        self.text_edit.setEnabled(False)
        self.text_edit.clear()

        overlay_rect = self.overlay_label.rect()
        overlay_rect.moveCenter(self.text_edit.rect().center())
        self.overlay_label.move(overlay_rect.topLeft())
        self.overlay_label.show()

    @QtCore.Slot()
    def on_cropped_pixmap_changed(self):
        self.image_changed.emit(self.crop_item.cropped_pixmap())


class OCRWorker(QtCore.QObject):

    text_ready = QtCore.Signal(str)
    ocr_started = QtCore.Signal()

    @QtCore.Slot(QtGui.QPixmap)
    def ocr_to_string(self, pixmap):
        self.ocr_started.emit()
        handle, path = tempfile.mkstemp(suffix=".png")
        os.close(handle)
        pixmap.save(path)
        cwd = os.getcwd()
        os.chdir(pathlib.Path(path).parent)
        string = pytesseract.image_to_string(path)
        if isinstance(string, bytes):
            string = string.decode("utf-8", errors="ignore")
        self.text_ready.emit(string)
        os.remove(path)
        os.chdir(cwd)
