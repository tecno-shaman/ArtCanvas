import sys

from PyQt6.QtGui import (
    QAction,
    QColor,
    QActionGroup
)
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import (
    QMainWindow, QMenu,
    QTabWidget, QToolBar,
    QStatusBar, QSpinBox,
    QColorDialog, QPushButton,
    QToolButton, QFileDialog, QScrollArea
)

from Canvas import Canvas
from modal_windows import WindowNewLayer
from src.modal_windows import WindowHelp
from ui_libs.ui_main import Ui_MainWindow


class ArtCanvas(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # uic.loadUi('styles/main.ui', self)
        self.setWindowTitle('ArtCanvas')

        self.all_canvas = {}  # доступ к слоям
        self.c_canvas = 1
        self.cnt_canvas = 1
        self.canvas_names = []

        self.INSTRUMENTS = ('pen', 'erazer', 'spray')
        self.cInstrument = 1  # индекс инструмента

        self.draw_config = {
            'pen_color': QColor(0, 0, 0),
            'brush_color': QColor(255, 255, 255),
            'width': 2
        }

        self.load_ui()

    def load_ui(self):
        self.setStyleSheet('background-color: rgb(195, 195, 195)')

        self.tool_bar()
        self.layers()

        self.action.triggered.connect(self.open_file)
        self.action_2.triggered.connect(self.save_file)
        self.action_3.triggered.connect(self.close_canvases)
        self.action_close.triggered.connect(self.close_app)

        self.action_pen.triggered.connect(self.choose_pen)
        self.action_erazor.triggered.connect(self.choose_erazer)
        self.action_spray.triggered.connect(self.choose_spray)
        self.action_ellipse.triggered.connect(self.choose_ellipse)
        self.action_rect.triggered.connect(self.choose_rect)

        self.action_cpen.triggered.connect(self.change_pen_color)
        self.action_cbrush.triggered.connect(self.change_brush_color)

        self.action_about.triggered.connect(self.help_menu)

        # self.action_undo.triggered.connect(self.call_undo)
        # self.action_redo.triggered.connect(self.call_redo)

    def contextMenuEvent(self, e):  # код для пкм меню
        pass

    def call_undo(self):
        self.all_canvas[self.canvas_names[self.c_canvas]].undo()

    def call_redo(self):
        self.all_canvas[self.canvas_names[self.c_canvas]].undo(reverse=1)

    def help_menu(self):
        h_m = WindowHelp()
        h_m.exec()

    def tool_bar(self):
        toolbar = QToolBar("Основная панель инструментов")
        self.addToolBar(toolbar)

        instruments_group = QActionGroup(self)
        instruments_group.setExclusive(True)

        # создание кнопок
        brush_menu = QToolButton()
        brush_menu.setText('Инструменты')
        brush_menu.setStatusTip('Выбрать инструмент')

        menu = QMenu(self)

        self.button_pen = QAction("Кисть", self)
        self.button_pen.setStatusTip("Выбрать кисть")
        self.button_pen.setCheckable(True)
        self.button_pen.setChecked(True)

        self.button_spray = QAction("Спрей", self)
        self.button_spray.setStatusTip("Выбрать спрей")
        self.button_spray.setCheckable(True)
        self.button_spray.setChecked(False)

        self.button_erazer = QAction('Ластик', self)
        self.button_erazer.setStatusTip('Выбрать ластик')
        self.button_erazer.setCheckable(True)

        self.button_rect = QAction("Прямоугольник", self)
        self.button_rect.setStatusTip("Выбрать прямоугольник")
        self.button_rect.setCheckable(True)
        self.button_rect.setChecked(False)

        self.button_ellipse = QAction("Элипс", self)
        self.button_ellipse.setStatusTip("Выбрать элипс")
        self.button_ellipse.setCheckable(True)
        self.button_ellipse.setChecked(False)

        button_width = QSpinBox()
        button_width.setStatusTip('Толщина кисти')
        button_width.setValue(self.draw_config['width'])
        button_width.setMinimum(1)

        btn_pen_color = QAction('Цвет 1', self)
        btn_pen_color.setStatusTip('Окно выбора цвета кисти')
        btn_pen_color.setCheckable(False)

        self.pen_pallete = QPushButton()
        self.pen_pallete.setStatusTip('Окно выбора цвета кисти')
        self.pen_pallete.setStyleSheet('background-color: black')

        btn_brush_color = QAction('Цвет 2', self)
        btn_brush_color.setStatusTip('Окно выбора цвета заливки')
        btn_brush_color.setCheckable(False)

        self.brush_pallete = QPushButton()
        self.brush_pallete.setStatusTip('Окно выбора цвета заливки')
        self.brush_pallete.setStyleSheet('background-color: white')

        button_add_canvas = QPushButton('+')
        button_add_canvas.setStatusTip('Добавить новый слой')
        button_add_canvas.setStyleSheet('')

        # размещение по группам
        instruments_group.addAction(self.button_pen)
        instruments_group.addAction(self.button_spray)
        instruments_group.addAction(self.button_erazer)
        instruments_group.addAction(self.button_rect)
        instruments_group.addAction(self.button_ellipse)

        menu.addAction(self.button_pen)
        menu.addAction(self.button_spray)
        menu.addAction(self.button_rect)
        menu.addAction(self.button_ellipse)
        brush_menu.setMenu(menu)
        brush_menu.setPopupMode(QToolButton.ToolButtonPopupMode.MenuButtonPopup)  # ????

        # toolbar.addAction(button_pen)
        toolbar.addWidget(brush_menu)
        toolbar.addAction(self.button_erazer)
        toolbar.addWidget(button_width)

        toolbar.addAction(btn_pen_color)

        toolbar.addWidget(self.pen_pallete)
        toolbar.addAction(btn_brush_color)
        toolbar.addWidget(self.brush_pallete)
        toolbar.addWidget(button_add_canvas)

        self.button_pen.triggered.connect(self.choose_pen)
        self.button_erazer.triggered.connect(self.choose_erazer)
        self.button_spray.triggered.connect(self.choose_spray)
        self.button_rect.triggered.connect(self.choose_rect)
        self.button_ellipse.triggered.connect(self.choose_ellipse)

        button_width.valueChanged.connect(self.change_width)
        btn_pen_color.triggered.connect(self.change_pen_color)
        self.pen_pallete.clicked.connect(self.change_pen_color)
        btn_brush_color.triggered.connect(self.change_brush_color)
        self.brush_pallete.clicked.connect(self.change_brush_color)
        button_add_canvas.clicked.connect(self.add_canvas)

        self.setStatusBar(QStatusBar(self))

    # connect for toolbar
    def choose_pen(self):
        self.cInstrument = 1
        self.button_pen.setChecked(True)

    def choose_erazer(self):
        self.cInstrument = 2
        self.button_erazer.setChecked(True)

    def choose_spray(self):
        self.cInstrument = 3
        self.button_spray.setChecked(True)

    def choose_rect(self):
        self.cInstrument = 4
        self.button_rect.setChecked(True)

    def choose_ellipse(self):
        self.cInstrument = 5
        self.button_ellipse.setChecked(True)

    def change_width(self, s):
        self.draw_config['width'] = s

    def change_pen_color(self):
        color = QColorDialog.getColor(initial=QColor("red"),
                                      title="Выбор цвета кисти")
        if color.isValid():
            self.pen_pallete.setStyleSheet(f"background-color: {color.name()}; font-size: 16px; border: {color.name()}")
            self.draw_config['pen_color'] = QColor(color.name())

    def change_brush_color(self):
        color = QColorDialog.getColor(initial=QColor("red"),
                                      title="Выбор цвета заливки")
        if color.isValid():
            self.brush_pallete.setStyleSheet(
                f"background-color: {color.name()}; font-size: 16px; border: {color.name()}")
            self.draw_config['brush_color'] = QColor(color.name())

    # вкладки
    def layers(self):
        self.tabs = QTabWidget()
        self.tabs.setMovable(True)
        self.tabs.setTabPosition(QTabWidget.TabPosition.South)

        # self.AddCanvas()

        btn_add_cnas = QPushButton('+')
        btn_add_cnas.setStatusTip('Добавить новый слой')
        self.tabs.setCornerWidget(btn_add_cnas)

        self.setCentralWidget(self.tabs)

        (btn_add_cnas.clicked.connect(self.add_canvas))
        self.tabs.currentChanged.connect(self.change_canvas)

    def add_canvas(self):
        dialog = WindowNewLayer()
        dialog.name_line.setText(str(self.cnt_canvas))
        dialog.exec()

        if dialog.name != 'EOP_CancelExit':
            self.all_canvas[dialog.name] = Canvas(self, dialog.x, dialog.y, dialog.name)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(self.all_canvas[dialog.name])
            self.tabs.addTab(scroll_area, dialog.name)

            self.cnt_canvas += 1
            self.canvas_names.append(dialog.name)

    def open_file(self):
        path, name = QFileDialog.getOpenFileName(
            self,
            "Открыть файл",
            "", filter="PNG, JPEG (*.png, *.jpg);; PNG (*.png);; JPEG (*jpg);; Все файлы (*)[0]",
        )

        if path:
            self.all_canvas[name] = Canvas(self, 0, 0, self.cnt_canvas, img=path)

            scroll_area = QScrollArea()
            scroll_area.setWidgetResizable(True)
            scroll_area.setWidget(self.all_canvas[name])
            self.tabs.addTab(scroll_area, str(self.cnt_canvas))

            self.cnt_canvas += 1
            self.cnt_canvas += 1
            self.canvas_names.append(name)

    def save_file(self):
        """
        Save active canvas to image file.
        :return:
        """
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить файл", "", "PNG Image file (*.png)"
        )

        if path:
            pixmap = self.all_canvas[self.canvas_names[self.c_canvas]]
            pixmap.save(path, "PNG")

    def close_canvases(self):
        self.all_canvas = {}
        self.c_canvas = 1
        self.cnt_canvas = 1
        self.canvas_names = []

        self.layers()

    def close_app(self):
        self.close()

    def change_canvas(self, idx):
        self.c_canvas = idx


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


def create_window():
    app = QApplication(sys.argv)
    ex = ArtCanvas()
    ex.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())


if __name__ == "__main__":
    create_window()
