import os, sys

#Import PySide classes
from PySide6.QtCore import QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication

#Import local classes
from Constants import SETTINGS_DIR, RESOURCE_PATH
from LocalDatabase import LocalDatabase
from MainWindow import MainWindow

from RelayPath import RelayPath

#If main program run this.
if __name__ == "__main__":

    rp = RelayPath()
    rp.generateRelayPaths()

    #Output SS threshold
    output = f"PATH SS THRESHOLD: {rp.PATH_SS_THRESHOLD}\n\n"

    #Output Relay Signal Score table
    output += "RELAY SIGNAL SCORE\n"
    output += rp.score_table

    #Output Primary Relay Path table
    output += "\n\nRELAY PATH\n"
    output += rp.primary_relay_table

    #Output Alternate Relay Path table
    # output += "\n\nALTERNATE RELAY PATH\n"
    # output += rp.alternate_replay_table
    output += '\n\n'

    #Output Isolated Callsigns table. These are callsigns that have entries for TX but no log for RX signals
    output += rp.non_contact_table

    print(output)

    # #Setup settings directory if it doesn't exist
    # if not os.path.exists(SETTINGS_DIR):
    #     os.mkdir(SETTINGS_DIR)

    # #Load and validate database
    # ldb = LocalDatabase()
    # ldb.validate()
    # ldb.setup()

    # #Start Qt Application
    # app = QApplication(sys.argv)

    # #Load icon as windows icon
    # app_icon = QIcon()
    # app_icon.addFile(f'{RESOURCE_PATH}/iegmrs.png', QSize(16,16))
    # app_icon.addFile(f'{RESOURCE_PATH}/iegmrs.png', QSize(24,24))
    # app_icon.addFile(f'{RESOURCE_PATH}/iegmrs.png', QSize(32,32))
    # app_icon.addFile(f'{RESOURCE_PATH}/iegmrs.png', QSize(48,48))
    # app_icon.addFile(f'{RESOURCE_PATH}/iegmrs.png', QSize(256,256))
    # app.setWindowIcon(app_icon)

    # #Show main window
    # window = MainWindow()
    # window.show()

    # #Exit when window is closed
    # app.exec()