# Secauax
From `Secure Auax`

### Only tested in Windows 10 at the moment!
---
## How does it work?
This program should be used to encrypt and decrypt files.
It has been built with the `cryptography` package. The encryptation technique is based on a Base64 key. This key is crucial to decrypt the files later on. 
Without the key, you cannot read the file.

## Download
You can download the `Secauax by Auax.exe` file from the *executable* 
branch, this requires no installation of any packages.
You can also download the source from the *main* branch.
The program will run the same.

## Source Installation
To run the non-executable version of this program, you need Python 3 
or superior. It's also required to install the following packages:
* pyqt5
* cryptography

This can be found in the `requirements.txt` file.

# Run the program
## Executable version:
To run Secauax, double-click the executable file. The program should run as expected.

## The source version:
Open the Windows 10 console (CMD) and type: `python3 window.py`.

---
# How to use it
<img src="https://i.imgur.com/jhVSR5e.jpg" height="400" />
This is the program's interface. To encrypt a file, you must select a file and set the output filename.

### Keys
* When encrypting a file, you must store the key somewhere otherwise you WON'T be able to decrypt it later.
* When decrypting a file, you must select the same key used to encrypt it, or you will encounter an error. 
<img src="https://i.imgur.com/ofFYzMv.jpg" height="120"/>

---
**By Auax**

Contact: `auax.dev@gmail.com`
