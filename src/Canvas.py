from PyQt6.QtCore import (
    QPoint
)
from PyQt6.QtGui import (
    QPixmap,
    QColor
)
from PyQt6.QtWidgets import (
    QLabel
)

from changes import *
from instruments import *
from utils import *


class Canvas(QLabel, QPixmap):
    def __init__(self, window, x, y, name, img=None):
        super().__init__()
        if img:
            self.image = QImage(img)
            self.x = self.image.width()
            self.y = self.image.height()

        else:
            self.x = int(x)
            self.y = int(y)
            self.image = QImage(self.x, self.y, QImage.Format.Format_RGB32)
            self.image.fill(Qt.GlobalColor.white)

        self.setPixmap(QPixmap.fromImage(self.image))
        self.name = name

        self.c_inx = 0
        self.alpha = 1.0
        self.window = window
        self.move = []
        self.lastPoint = QPoint()
        self.drawing = False
        self.sign = 0
        self.cpose = None

        # database
        self.con, self.cur = create_connection(self.name)
        add_change_to_db(self.con, self.cur, 0, self.window.draw_config, image_to_bytearray(self.image))
        self.c_inx += 1

    def setPixmap(self, pixmap: QPixmap):
        super().setPixmap(pixmap)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawImage(0, 0, self.image)

        # отрисовка рамки
        painter.setPen(QPen(QColor(185, 185, 185), 2))
        painter.drawRect(0, 0, self.x - 1, self.y - 1)
        if self.sign and self.window.cInstrument == 4:
            painter.setPen(QPen(self.window.draw_config['pen_color'], self.window.draw_config['width']))
            painter.drawRect(self.lastPoint.x(), self.lastPoint.y(), self.cpose.x() - self.lastPoint.x(),
                             self.cpose.y() - self.lastPoint.y())
        elif self.sign and self.window.cInstrument == 5:
            painter.setPen(QPen(self.window.draw_config['pen_color'], self.window.draw_config['width']))
            painter.drawEllipse(self.lastPoint.x(), self.lastPoint.y(), self.cpose.x() - self.lastPoint.x(),
                                self.cpose.y() - self.lastPoint.y())

    def mousePressEvent(self, event):
        # self.move = [(event.pos().x(), event.pos().y())]

        if event.button() == Qt.MouseButton.LeftButton:
            self.lastPoint = event.pos()
            self.drawing = True

        if self.drawing and self.window.cInstrument == 1:
            draw_line(self, self.window.draw_config, event)

        elif self.drawing and self.window.cInstrument == 2:
            erase_line(self, self.window.draw_config, event)

        elif self.drawing and self.window.cInstrument == 3:
            spray(self, self.window.draw_config, event)

    def mouseMoveEvent(self, event):
        # self.move.append((event.pos().x(), event.pos().y()))
        if self.drawing and self.window.cInstrument == 1:
            draw_line(self, self.window.draw_config, event)

        elif self.drawing and self.window.cInstrument == 2:
            erase_line(self, self.window.draw_config, event)

        elif self.drawing and self.window.cInstrument == 3:
            spray(self, self.window.draw_config, event)

        if self.drawing and self.window.cInstrument in (4, 5):
            self.sign = 1
            self.cpose = event.pos()
            self.update()
        else:
            self.sign = 0

    def mouseReleaseEvent(self, event):
        add_change_to_db(self.con, self.cur, self.window.cInstrument, self.window.draw_config,
                         image_to_bytearray(self.image))
        self.c_inx += 1

        if self.drawing and self.window.cInstrument == 4:
            draw_rect(self, self.window.draw_config, event)
        elif self.drawing and self.window.cInstrument == 5:
            draw_ellipse(self, self.window.draw_config, event)

        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def undo(self, reverse=0):
        # self.cur.execute("SELECT * FROM Changes ORDER BY id")
        # rows = self.cur.fetchall()
        #
        # if len(rows) > 1 and not reverse:
        #     print(rows[self.c_inx][5])  # Печать предпоследней записи
        #     self.image = bytearray_to_image(rows[self.c_inx][5])
        #     self.update()
        bin_img = str(self.cur.execute(f"SELECT meta FROM Changes WHERE id = {self.c_inx}").fetchall()[0])
        print(bin_img)
        self.image = binary_to_qimage(bin_img)
        self.update()

    def save(self, path, out_format):
        self.image.save(path, out_format)
