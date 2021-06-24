import getpass
import os
import sys
import webbrowser
from typing import Any

from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.uic import loadUi
from cryptography.fernet import InvalidToken

from exceptions import Exit
from secauax import Secauax


def resource_path(relative_path: str) -> str:
    """
    Executable resource getter
    :param relative_path: path to resource
    :return: str
    """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.log_data = []

        # Set Window settings
        loadUi(resource_path("resources/main.ui"), self)
        self.setWindowTitle("Secauax by Auax")
        self.setWindowIcon(QtGui.QIcon(resource_path("resources/icon.ico")))

        self.enable = False  # Enable the encrypt and decrypt buttons

        # Connect Menu
        self.clear_log.triggered.connect(self.reset_logger)
        self.open_github.triggered.connect(lambda: webbrowser.open("https://github.com/auax"))
        self.report_issue.triggered.connect(lambda: webbrowser.open("https://github.com/auax/secauax/issues/new"))
        self.donate.triggered.connect(lambda: webbrowser.open("https://paypal.me/zellius"))

        # Connect First Section (input path)
        self.browse_file_inp_btn.clicked.connect(lambda: self.browse_file(self.input_path))
        self.browse_directory_inp_btn.clicked.connect(lambda: self.browse_folder(self.input_path))

        # Connect Second Section (output path)
        self.browse_file_out_btn.clicked.connect(lambda: self.browse_file(self.output_path, True))
        self.browse_directory_out_btn.clicked.connect(lambda: self.browse_folder(self.output_path))

        # On change mode (file or directory)
        self.mode_cb.stateChanged.connect(self.change_mode)

        # On enable "save_key" checkbox
        self.save_key_cb.stateChanged.connect(lambda: MainWindow.key_mode(self.save_key_cb,
                                                                          self.save_key_path,
                                                                          self.browse_save_key_btn))
        self.browse_save_key_btn.clicked.connect(lambda: self.browse_file(self.save_key_path, True))

        # On enable "load_key" checkbox
        self.load_key_cb.stateChanged.connect(lambda: MainWindow.key_mode(self.load_key_cb,
                                                                          self.load_key_path,
                                                                          self.browse_load_key_btn))
        self.browse_load_key_btn.clicked.connect(lambda: self.browse_file(self.load_key_path))

        # Last section (encrypt and decrypt buttons)
        self.encrypt_btn.clicked.connect(self.encrypt)
        self.decrypt_btn.clicked.connect(self.decrypt)

        self.logger(f"Welcome to Secauax, {getpass.getuser().capitalize()}")

    def browse_file(self, change_label: Any = None, save: bool = False) -> None:
        """
        Open file browser.
        :param change_label: change a QLabel text to the path
        :param save: open browser in save mode
        :return: None
        """

        if save:
            fname = QFileDialog.getSaveFileName(self, "Save File")
        else:
            fname = QFileDialog.getOpenFileName(self, "Select File")

        if change_label:
            change_label.setText(fname[0])  # Change label text

        self.valid()
        return fname

    def browse_folder(self, change_label: Any = None) -> None:
        """
         Open folder browser.
        :param change_label: change a QLabel text to the path
        :return: None
        """
        fname = QFileDialog.getExistingDirectory(self, "Select Folder")

        # Change label
        if change_label:
            change_label.setText(fname)

        self.valid()
        return fname

    def change_mode(self) -> None:
        """
        Enable or disable the buttons and clear the paths based on the mode_cb checkbox
        :return: None
        """

        # Clear paths
        self.input_path.setText("")
        self.output_path.setText("")

        checked = self.mode_cb.isChecked()

        # Enable and disable buttons
        self.browse_file_inp_btn.setEnabled(not checked)
        self.browse_directory_inp_btn.setEnabled(checked)
        self.browse_file_out_btn.setEnabled(not checked)
        self.browse_directory_out_btn.setEnabled(checked)

        self.valid()

    def valid(self) -> None:
        """
        Check if the configuration is valid
        :return: None
        """

        # If the QLabels are defined with a path then enable the buttons
        if self.input_path.text() and self.output_path.text():
            self.encrypt_btn.setEnabled(True)
            self.decrypt_btn.setEnabled(True)
        else:
            self.encrypt_btn.setEnabled(False)
            self.decrypt_btn.setEnabled(False)

    @staticmethod
    def key_mode(this_checkbox, to_clear, to_enable) -> None:
        """
        Enable or disable the key-mode
        :param this_checkbox: referred to the checked checkbox
        :param to_clear: the QLabel to clear
        :param to_enable: the button to enable
        :return: None
        """
        checked = this_checkbox.isChecked()
        if not checked:
            to_clear.setText("")  # Clear text
        to_enable.setEnabled(checked)

    def encrypt(self) -> None:
        """
        Encrypt using the Secauax.encrypt_file or Secauax.bulk_encrypt methods.
        :return: None
        """

        try:
            secauax = Secauax()  # Class instance

            if self.save_key_path.text():
                # Save key to the desired path
                secauax.save_key(self.save_key_path.text())
                self.logger(f"Key saved in {self.save_key_path.text()}!")

            if self.load_key_path.text():
                # Load key from the desired path
                secauax.load_key_into_class(self.load_key_path.text())
                self.logger(f"Key path set to: {self.load_key_path.text()}!")

            if self.mode_cb.isChecked():
                # Directory mode
                if not secauax.bulk_encrypt(self.input_path.text(), self.output_path.text()):
                    raise InvalidToken
            else:
                # File mode
                secauax.encrypt_file(self.input_path.text(), self.output_path.text())

            self.logger(f"Used key: {secauax.key.decode()}")
            self.logger(f"File(s) successfuly encrypted in {self.output_path.text()}!")

            # Show a message
            MainWindow.create_dialog("File(s) encrypted successfuly!", "", "Success!", QMessageBox.Information)

        except InvalidToken:
            self.logger("InvalidToken! Make sure to select the correct key.", "red")

        except ValueError:
            self.logger("Invalid Fernet key: Fernet key must be 32 url-safe base64-encoded bytes", "red")

        except Exception as E:

            if E.__class__ == Exit:
                exitcode = E.exitcode

                if exitcode == 1:
                    self.logger("Couldn't save the key!", "red")

                elif exitcode == 2:
                    self.logger("Path to directory not found!", "red")

            else:
                self.logger(f"Unhandled error: {type(E).__name__}", "red")

    def decrypt(self) -> None:
        """
        Decrypt using the Secauax.decrypt_file or Secauax.bulk_decrypt methods.
        :return: None
        """

        try:
            secauax = Secauax()  # Class instance

            if self.save_key_path.text():
                # Save key to the desired path
                secauax.save_key(self.save_key_path.text())
                self.logger(f"Key saved in {self.save_key_path.text()}!")

            if self.load_key_path.text():
                # Load key from the desired path
                secauax.load_key_into_class(self.load_key_path.text())
                self.logger(f"Key path set to: {self.load_key_path.text()}!")

            if self.mode_cb.isChecked():
                # Directory mode
                if not secauax.bulk_decrypt(self.input_path.text(), self.output_path.text()):
                    raise InvalidToken
            else:
                # File mode
                secauax.decrypt_file(self.input_path.text(), self.output_path.text())

            self.logger(f"Used key: {secauax.key.decode()}")
            self.logger(f"File(s) successfuly decrypted in {self.output_path.text()}!")

            # Show message
            MainWindow.create_dialog("File(s) decrypted successfuly!", "", "Success!", QMessageBox.Information)

        except InvalidToken:
            self.logger("InvalidToken! Make sure to select the correct key.", "red")

        except ValueError:
            self.logger("Invalid Fernet key: Fernet key must be 32 url-safe base64-encoded bytes", "red")

        except Exception as E:

            if E.__class__ == Exit:
                exitcode = E.exitcode

                if exitcode == 1:
                    self.logger("Couldn't save the key!", "red")

                elif exitcode == 2:
                    self.logger("Path to directory not found!", "red")

            else:
                self.logger(f"Unhandled error: {type(E).__name__}", "red")
                raise E

    def logger(self, message: str, color: str = "black") -> None:
        """
         Add text to the logger object
        :param message: the message to display
        :param color: color of the message
        :return: None
        """
        to_html = ""
        self.log_data.append(message)

        for string in self.log_data:
            to_html += f"<p style='margin: 2px 4px 2px 4px !important;'>" \
                       f"<code style='color:red'>> </code>" \
                       f"<code style='color:{color}'>{string}</code></p> "

        self.log.setHtml(to_html)  # Set the generated HTML content

    def reset_logger(self) -> None:
        """
        Clear all log data
        :return: None
        """
        self.log_data = []
        self.log.setHtml("")

    @staticmethod
    def create_dialog(message: str, informative_text: str, title: str = "Info", icon=QMessageBox.Critical) -> None:
        """
        Create a dialog window
        :param message: the message to show
        :param informative_text: the message below
        :param title: the dialog window title
        :param icon: the icon to display.
        :return: None
        """
        msg = QMessageBox()
        msg.setIcon(icon)
        msg.setText(message)
        msg.setInformativeText(informative_text)
        msg.setWindowTitle(title)
        msg.exec_()


# Run app
app = QApplication(sys.argv)
main_window = MainWindow()
print(main_window.geometry())
main_window.setMinimumSize(650, 680)
main_window.show()
sys.exit(app.exec())
