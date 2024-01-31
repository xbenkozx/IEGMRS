import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        if os.path.basename(sys.argv[0]) == "vetrak_keys.py":
            base_path = os.path.dirname(os.path.realpath(sys.argv[0]))
        else:
            base_path = "."

    return os.path.join(base_path, relative_path)

RESOURCE_PATH           = resource_path("resources")
BASE_PATH               = os.path.dirname(os.path.realpath(sys.argv[0]))
SETTINGS_DIR            = os.path.join(os.path.expanduser('~'), "AppData", "Local", "IEGMRS")