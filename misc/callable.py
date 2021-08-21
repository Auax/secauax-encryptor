import os
import sys
from pathlib import Path
from typing import Union, Any

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap


def resource_path(relative_path: str) -> str:
    """
    Executable resource getter
    :param relative_path: path to resource
    :return: str
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def generate_pixmap(image_path: Union[str, Path], geometry: Any):
    """Responsive pixmap generator"""
    pixmap = QPixmap(resource_path(image_path))  # Load image
    pwidth, pheight = pixmap.width(), pixmap.height()  # Get image dimensions
    w, h = geometry.width(), geometry.height()  # Get misc dimensions
    pixmap = pixmap.scaled(int(w / 1.5), int(w / 1.5 / pheight * pwidth),
                           Qt.KeepAspectRatio,
                           Qt.FastTransformation)

    return pixmap


"""
Wrappers for browse_file()
"""


def file_browser_label_wrapper(fname, qlabel):
    """browse_file() wrapper"""
    qlabel.setText(fname[0])


def file_browser_image_key_wrapper(fname, qlabel, toggle_btn):
    """browse_file() wrapper"""
    qlabel.setText(fname[0])
    if fname[0]:
        toggle_btn.setEnabled(True)
    else:
        toggle_btn.setEnabled(False)
