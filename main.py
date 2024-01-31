import os, sys

from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication
from Constants import SETTINGS_DIR, RESOURCE_PATH
from LocalDatabase import LocalDatabase
from MainWindow import MainWindow

if __name__ == "__main__":

    #Setup settings directory if it doesn't exist
    if not os.path.exists(SETTINGS_DIR):
        os.mkdir(SETTINGS_DIR)

    #Load and validate database
    ldb = LocalDatabase()
    ldb.validate()
    ldb.setup()

    app = QApplication(sys.argv)

    app_icon = QIcon()
    app_icon.addFile(f'{RESOURCE_PATH}/iegmrs.png', QSize(16,16))
    app_icon.addFile(f'{RESOURCE_PATH}/iegmrs.png', QSize(24,24))
    app_icon.addFile(f'{RESOURCE_PATH}/iegmrs.png', QSize(32,32))
    app_icon.addFile(f'{RESOURCE_PATH}/iegmrs.png', QSize(48,48))
    app_icon.addFile(f'{RESOURCE_PATH}/iegmrs.png', QSize(256,256))
    app.setWindowIcon(app_icon)

    window = MainWindow()
    window.show()

    app.exec()