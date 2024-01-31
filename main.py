import os

from Constants import SETTINGS_DIR
from LocalDatabase import LocalDatabase

if __name__ == "__main__":

    #Setup settings directory if it doesn't exist
    if not os.path.exists(SETTINGS_DIR):
        os.mkdir(SETTINGS_DIR)

    #Load and validate database
    ldb = LocalDatabase()
    ldb.validate()
    ldb.setup()



    app_icon = QIcon()
    app_icon.addFile(f'{RESOURCE_PATH}/vetrak_icon.png', QSize(16,16))
    app_icon.addFile(f'{RESOURCE_PATH}/vetrak_icon.png', QSize(24,24))
    app_icon.addFile(f'{RESOURCE_PATH}/vetrak_icon.png', QSize(32,32))
    app_icon.addFile(f'{RESOURCE_PATH}/vetrak_icon.png', QSize(48,48))
    app_icon.addFile(f'{RESOURCE_PATH}/vetrak_icon.png', QSize(256,256))