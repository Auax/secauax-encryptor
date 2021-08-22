import os
import sys
from pathlib import Path
from typing import Union, Any

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox


def resource_path(relative_path: Union[str, Path]) -> str:
    """
    Executable resource getter
    :param relative_path: path to resource
    :return: str
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


def generate_pixmap(image_path: Union[str, Path], geometry: Any) -> QPixmap:
    """Responsive pixmap generator"""
    pixmap = QPixmap(resource_path(image_path))  # Load image
    pwidth, pheight = pixmap.width(), pixmap.height()  # Get image dimensions
    w, h = geometry.width(), geometry.height()  # Get misc dimensions
    pixmap = pixmap.scaled(int(w / 1.5), int(w / 1.5 / pheight * pwidth),
                           Qt.KeepAspectRatio,
                           Qt.FastTransformation)

    return pixmap


def create_dialog(message: str, informative_text: str, title: str = "Info", icon=QMessageBox.Critical) -> None:
    """
    Create a dialog misc
    :param message: the message to show
    :param informative_text: the message below
    :param title: the dialog misc title
    :param icon: the icon to display.
    :return: None
    """
    msg = QMessageBox()
    msg.setIcon(icon)
    msg.setText(message)
    msg.setInformativeText(informative_text)
    msg.setWindowTitle(title)
    msg.exec_()


def file_browser_label(fname, qlabel):
    """Function for the browse_file() method
    :param fname: filename (automatically passed by wrapper)
    :param qlabel: qlabel reference
    """
    qlabel.setText(fname[0])


def file_browser_image_key(fname, qlabel, toggle_btn):
    """Function for the browse_file() method
    :param fname: filename (automatically passed by wrapper)
    :param qlabel: qlabel reference
    :param toggle_btn: toggle this button
    """
    qlabel.setText(fname[0])
    if fname[0]:
        toggle_btn.setEnabled(True)
    else:
        toggle_btn.setEnabled(False)
