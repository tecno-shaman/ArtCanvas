from random import gauss

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen, QPainter, QBrush


def draw_line(layer, draw_config, event):
    painter = QPainter(layer.image)
    pen = QPen(draw_config['pen_color'], draw_config['width'])
    painter.setPen(pen)
    painter.drawLine(layer.lastPoint, event.pos())

    layer.lastPoint = event.pos()
    layer.update()


def erase_line(layer, draw_config, event):
    painter = QPainter(layer.image)
    pen = QPen(Qt.GlobalColor.white, draw_config['width'])
    painter.setPen(pen)
    painter.drawLine(layer.lastPoint, event.pos())

    layer.lastPoint = event.pos()
    layer.update()


def spray(layer, draw_config, event):
    painter = QPainter(layer.image)
    pen = QPen(draw_config['pen_color'], 1)
    painter.setPen(pen)
    points = draw_config['width'] * 3
    for point in range(points):
        x = gauss(0, draw_config['width'])
        y = gauss(0, draw_config['width'])
        painter.drawPoint(
            int(event.position().x() + x),
            int(event.position().y() + y))

    layer.lastPoint = event.pos()
    layer.update()


def draw_rect(layer, draw_config, event):
    painter = QPainter(layer.image)
    pen = QPen(draw_config['pen_color'], draw_config['width'])
    brush = QBrush(draw_config['brush_color'])

    painter.setPen(pen)
    painter.setBrush(brush)

    painter.drawRect(layer.lastPoint.x(), layer.lastPoint.y(), event.pos().x() - layer.lastPoint.x(),
                     event.pos().y() - layer.lastPoint.y())

    layer.lastPoint = event.pos()
    layer.update()


#
def draw_ellipse(layer, draw_config, event):
    painter = QPainter(layer.image)
    pen = QPen(draw_config['pen_color'], draw_config['width'])
    brush = QBrush(draw_config['brush_color'])

    painter.setPen(pen)
    painter.setBrush(brush)

    painter.drawEllipse(layer.lastPoint.x(), layer.lastPoint.y(), event.pos().x() - layer.lastPoint.x(),
                        event.pos().y() - layer.lastPoint.y())

    layer.lastPoint = event.pos()
    layer.update()
