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

import threading
import typing as T

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import Qt, QRectF


class HandleCircleItem(QtWidgets.QGraphicsEllipseItem):
    def __init__(self, radius: float, position_change_callback, parent):
        super().__init__(-radius, -radius, radius * 2, radius * 2, parent)
        self.position_change_callback = position_change_callback
        self.setFlag(self.ItemIsMovable, True)
        self.setFlag(self.ItemSendsGeometryChanges, True)
        self.setBrush(QtGui.QColor("#99d8c9"))
        self.setPen(QtGui.QPen(QtGui.QColor("#2ca25f"), 1))

    def itemChange(self, change: QtWidgets.QGraphicsItem.GraphicsItemChange, value: T.Any) -> T.Any:
        if change == self.ItemPositionChange and self.scene():
            new_point = self.position_change_callback(T.cast(QtCore.QPointF, value), self)
            return new_point

        return super().itemChange(change, value)


class DelayedWorker(QtCore.QObject):
    def __init__(self, delay_time_ms: int, work):
        super().__init__()
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(delay_time_ms)
        self.timer.timeout.connect(self.time_out)
        self.work = work
        self.args = ()

    def renew_timer(self, *args):
        self.timer.start(self.timer.interval())
        self.args = args

    def time_out(self):
        self.timer.stop()
        self.work(*self.args)


class CropMask(QtWidgets.QGraphicsPathItem):
    def __init__(self, parent, rect_change_callback):
        super().__init__(parent)
        self.top_left_handle = HandleCircleItem(8, self.position_callback, self)
        self.top_right_handle = HandleCircleItem(8, self.position_callback, self)
        self.bottom_left_handle = HandleCircleItem(8, self.position_callback, self)
        self.bottom_right_handle = HandleCircleItem(8, self.position_callback, self)
        self.setBrush(QtGui.QColor("#8899d8c9"))
        self.setPen(QtGui.QPen(QtGui.QColor("#2ca25f"), 1))
        self.handle_move_lock = threading.Lock()

        self.opposing_vertices = {
            self.top_left_handle: self.bottom_right_handle,
            self.top_right_handle: self.bottom_left_handle,
            self.bottom_left_handle: self.top_right_handle,
            self.bottom_right_handle: self.top_left_handle,
        }
        self.restriction_signs = {
            self.top_left_handle: (1.0, 1.0),
            self.top_right_handle: (-1.0, 1.0),
            self.bottom_left_handle: (1.0, -1.0),
            self.bottom_right_handle: (-1.0, -1.0),
        }
        self.crop_rect = QtCore.QRectF(0, 0, 0, 0)
        self.bound_rect = QtCore.QRectF(0, 0, 0, 0)

        self.rect_change_callback = rect_change_callback

    def position_callback(self, point: QtCore.QPointF, vertex: HandleCircleItem):
        if self.handle_move_lock.locked():
            return point

        point = put_inside(point, self.bound_rect)
        opposite_point = self.opposing_vertices[vertex].pos()
        x_sign, y_sign = self.restriction_signs[vertex]

        if not has_same_sign(opposite_point.x() - point.x(), x_sign):
            point.setX(opposite_point.x())

        if not has_same_sign(opposite_point.y() - point.y(), y_sign):
            point.setY(opposite_point.y())

        self.crop_rect = QRectF(point, opposite_point).normalized()
        self.rect_change_callback()
        self.redraw()
        return point

    def redraw(self):
        with self.handle_move_lock:
            self.top_left_handle.setPos(self.crop_rect.topLeft())
            self.top_right_handle.setPos(self.crop_rect.topRight())
            self.bottom_left_handle.setPos(self.crop_rect.bottomLeft())
            self.bottom_right_handle.setPos(self.crop_rect.bottomRight())
            path = QtGui.QPainterPath()
            path.addRect(self.bound_rect)
            path.addRect(self.crop_rect.normalized())
            path.setFillRule(Qt.OddEvenFill)
            self.setPath(path)


class CropTool(QtCore.QObject):

    cropped_pixmap_changed = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.pixmap_item = QtWidgets.QGraphicsPixmapItem()
        self.pixmap_item.setTransformationMode(Qt.SmoothTransformation)
        self.signal_emitter = DelayedWorker(500, lambda: self.cropped_pixmap_changed.emit())
        self.crop_item = CropMask(self.pixmap_item, lambda: self.signal_emitter.renew_timer())

    def set_pixmap(self, pixmap: QtGui.QPixmap):
        self.pixmap_item.setPixmap(pixmap)
        self.crop_item.bound_rect = self.crop_item.mapRectFromParent(self.pixmap_item.boundingRect())
        self.crop_item.crop_rect = self.crop_item.bound_rect
        self.crop_item.redraw()
        self.signal_emitter.renew_timer()

    def cropped_pixmap(self) -> QtGui.QPixmap:
        rect = self.crop_item.mapRectToParent(self.crop_item.crop_rect)
        pixmap = self.pixmap_item.pixmap().copy(rect.toRect())
        return pixmap

    def set_rendered_scale(self, scale: float):
        bound = self.pixmap_item.boundingRect()
        crop = self.crop_item.mapRectToParent(self.crop_item.crop_rect)
        self.crop_item.setScale(1 / scale)
        self.crop_item.bound_rect = self.crop_item.mapRectFromParent(bound)
        self.crop_item.crop_rect = self.crop_item.mapRectFromParent(crop)
        self.crop_item.redraw()


def has_same_sign(x, y):  # if one is zeros, always return True
    return x * y >= 0


def put_inside(point: QtCore.QPointF, bound: QtCore.QRectF):
    bound = bound.normalized()
    return QtCore.QPointF(
        max(min(point.x(), bound.right()), bound.left()), max(min(point.y(), bound.bottom()), bound.top()),
    )
