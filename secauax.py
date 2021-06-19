import os
import glob
from typing import Any, Union
from pathlib import Path
from cryptography.fernet import Fernet


class Secauax:
    def __init__(self):
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
        Return a key from a ".key" file.
        :param path: path to key
        :return: bytes
        """
        with open(path, "rb") as filekey:
            key = filekey.read()
            filekey.close()

        return key

    def load_key_into_class(self, path: Union[Path, str]):
        """
        Replace the key class variable with loaded key.
        File extension is ".key"
        :param path: path to key
        :return: bytes
        """
        self.key_ = Secauax.load_key(path)
        return self.key

    def save_key(self, filename: Union[Path, str]) -> None:
        """
        Save generated key to a file.
        File extension is ".key"
        :param filename: path to save the key
        :return: None
        """
        with open(filename, 'wb') as filekey:
            filekey.write(self.key)
            filekey.close()

    def encrypt_file(self, path: Union[Path, str], filename: Union[Path, str] = None) -> bytes:
        """
        Encrypt a file with a generated key.
        DISCLAIMER: if no "filename" parameter is specified, the file will be overwritten.
        Returns the encrypted file data in bytes.
        :param path: path to original file
        :param filename: path to save the encrypted file
        :return: bytes
        """
        fernet = Fernet(self.key)

        # Open original file
        with open(path, "rb") as file:
            original_file = file.read()
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
                     file_extension: str = "*") -> None:
        """
        Encrypt all files inside a directory and save them into another directory.
        If the "output_directory" is the same as the "pathname", the files will be overwritten.
        :param pathname: path to the decrypted folder
        :param output_directory: path to save the encrypted files
        :param file_extension: select which files will be encrypted. Format: ".png" or, for all type of files: "*"
        :return: None
        """

        assert os.path.isdir(pathname), "pathname path doesn't exist"
        assert os.path.isdir(output_directory), "output_directory path doesn't exist"

        for file in glob.glob(os.path.join(pathname, file_extension)):
            self.encrypt_file(file, os.path.join(output_directory, os.path.basename(file)))

    def decrypt_file(self, path: Union[Path, str], filename: Union[Path, str] = None) -> bytes:
        """
        Decrypt a file with a generated key.
        DISCLAIMER: if no "filename" parameter is specified, the file will be overwritten.
        Returns the decrypted file data in bytes.
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

    def bulk_decrypt(self,
                     pathname: Union[Path, str],
                     output_directory: Union[Path, str] = None,
                     file_extension: str = "*") -> None:
        """
        Decrypt all files inside a directory and save them into another directory.
        If the "output_directory" is the same as the "pathname", the files will be overwritten.
        :param pathname: path to encrypted folder
        :param output_directory: path to save the decrypted files
        :param file_extension: select which files will be decrypted. Format: ".png" or, for all type of files: "*"
        :return: None
        """

        assert os.path.isdir(pathname), "pathname path doesn't exist"
        assert os.path.isdir(output_directory), "output_directory path doesn't exist"

        for file in glob.glob(os.path.join(pathname, file_extension)):
            self.decrypt_file(file, os.path.join(output_directory, os.path.basename(file)))
