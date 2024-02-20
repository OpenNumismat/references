import os
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QGuiApplication

QGuiApplication()

svg_path = "../data/icons/flags/Wikipedia"
maxWidth = 16
maxHeight = 16

for filename in os.listdir(svg_path):
    file_title, file_extension = os.path.splitext(filename)
    if file_extension == '.svg':
        img = QImage(os.path.join(svg_path, filename))
        if img.width() > maxWidth or img.height() > maxHeight:
            img = img.scaled(maxWidth, maxHeight,
                    Qt.KeepAspectRatio, Qt.SmoothTransformation)
        print(file_title + file_extension)
        img.save(os.path.join(svg_path, file_title + '.png'))
