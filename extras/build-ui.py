import os

file_list = [
    ['ui/mainwindowview.ui', 'ui/ui_mainwindow.py']
]

#Build PyQt UI files for PySide6 and PySide2
for f in file_list:
    print(f"Building {f[1]}...", end="")
    # os.system(f'pyside2-uic ./{f[0]} > ./PySide2_UI/{f[1]}')
    os.system(f'pyside6-uic ./{f[0]} > ./{f[1]}')
    print("Done")