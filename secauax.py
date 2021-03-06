import glob
import os
from pathlib import Path
from typing import Union

from cryptography.fernet import Fernet, InvalidToken

from exceptions import Exit


class Secauax:
    """
    Secauax encryption class
    """

    def __init__(self):
        """
        Init method
        """
        self.key_ = Fernet.generate_key()

    def __str__(self):
        return self.key.decode()

    def __repr__(self):
        return self.key.decode()

    @property
    def key(self):
        return self.key_

    @staticmethod
    def load_key(path: Union[Path, str]) -> bytes:
        """
        Return a key from a file. This key must be valid, otherwise, an error will be thrown.
        :param path: path to key
        :return: bytes
        """
        with open(path, "rb") as filekey:
            key = filekey.read()
            filekey.close()

        return key

    def load_key_into_class(self, path: Union[Path, str]):
        """
        Replace the key class variable with the loaded key and return it.
        :param path: path to key
        :return: bytes
        """
        self.key_ = Secauax.load_key(path)
        return self.key

    def save_key(self, filename: Union[Path, str]) -> Union[bool, Exit]:
        """
        Save set key to a file. You can choose the file extension, although the ".key" extension is recommended.
        This method returns a true boolean if the file is saved successfully. An OSError will call the Exit class
        :param filename: path to save the key
        :return: bool
        """
        try:
            with open(filename, 'wb') as filekey:
                filekey.write(self.key)
                filekey.close()
        except OSError:
            return Exit(Exit.KeyFailedToSave)
        return True

    def encrypt_file(self, path: Union[Path, str], filename: Union[Path, str] = None) -> bytes:
        """
        Encrypt a file with the set key.
        Attention: If the filename parameter is not specified, the new file will overwrite the original.
        It returns the encrypted file data in bytes.
        :param path: path to the original file
        :param filename: path to save the encrypted file
        :return: bytes
        """
        fernet = Fernet(self.key)

        # Open original file
        with open(path, "rb") as file:
            original_file = file.read()  # Read data in bytes
            file.close()

        # Encrypt the file
        encrypted_data = fernet.encrypt(original_file)

        destination = filename if filename else path
        with open(destination, "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)
            encrypted_file.close()

        return encrypted_data

    def bulk_encrypt(self,
                     pathname: Union[Path, str],
                     output_directory: Union[Path, str] = None,
                     file_extension: str = "*") -> bool:
        """
        Encrypt all the files inside a directory and save them into another directory.
        Attention: If the output_directory parameter is not specified, the new file(s) will overwrite the original(s).
        This method returns a true boolean if the files are saved successfully. Any error will result in a false boolean.
        :param pathname: path to the decrypted folder
        :param output_directory: path to save the encrypted files
        :param file_extension: filter files by extension: ".png" / ".txt" / ...
        :return: bool
        """

        if not os.path.isdir(pathname) or not os.path.isdir(output_directory):
            raise Exit(Exit.DirectoryNotFound)

        files_encrypted = 0

        for file in glob.glob(os.path.join(pathname, file_extension)):
            try:
                filename = os.path.join(output_directory, os.path.basename(file))
                if os.path.isdir(file):  # Skip folders
                    continue
                self.encrypt_file(file, filename)
                files_encrypted += 1

            except InvalidToken:
                pass

        return True if files_encrypted >= 1 else False

    def decrypt_file(self, path: Union[Path, str], filename: Union[Path, str] = None) -> bytes:
        """
        Decrypt a file with the set key.
        Attention: If the filename parameter is not specified, the new file will overwrite the original.
        It returns the decrypted file data in bytes.
        :param path: path to the encrypted file
        :param filename: path to save the decrypted file
        :return: bytes
        """
        fernet = Fernet(self.key)

        # Open original file
        with open(path, "rb") as encrypted_file:
            encrypted_data = encrypted_file.read()
            encrypted_file.close()

        # Encrypt the file
        decrypted_data = fernet.decrypt(encrypted_data)

        destination = filename if filename else path
        with open(destination, "wb") as decrypted_file:
            decrypted_file.write(decrypted_data)
            decrypted_file.close()

        return decrypted_data

    def bulk_decrypt(self,
                     pathname: Union[Path, str],
                     output_directory: Union[Path, str] = None,
                     file_extension: str = "*") -> bool:
        """
        Decrypt all the files inside a directory and save them into another directory.
        Attention: If the output_directory parameter is not specified, the new file(s) will overwrite the original(s).
        This method returns a true boolean if at least one file was decrypted.
        :param pathname: path to encrypted folder
        :param output_directory: path to save the decrypted files
        :param file_extension: filter files by extension: ".png" / ".txt" / ...
        :return: bool
        """
        if not os.path.isdir(pathname) or not os.path.isdir(output_directory):
            raise Exit(Exit.DirectoryNotFound)

        files_decrypted = 0

        for file in glob.glob(os.path.join(pathname, file_extension)):
            try:
                filename = os.path.join(output_directory, os.path.basename(file))
                if os.path.isdir(file):  # Skip folders
                    continue
                self.decrypt_file(file, filename)
                files_decrypted += 1

            except InvalidToken:
                pass

        return True if files_decrypted >= 1 else False
