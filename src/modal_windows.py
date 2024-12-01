from PyQt6.QtWidgets import QDialog

from ui_libs.create_layer_ui import New_layer_ui
from ui_libs.help import Ui_Form


class WindowNewLayer(QDialog, New_layer_ui):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class WindowHelp(QDialog, Ui_Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        with open('../Documentation/help.html', 'rt', encoding='utf-8') as help_doc:
            text = help_doc.read()

        self.textBrowser.setText(text)
