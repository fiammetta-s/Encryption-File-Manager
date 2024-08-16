# Encryption File Manager

## Project Overview

This project is a command-line tool for securely encrypting and decrypting files. The tool leverages the `click` library for command-line interaction, the `cryptography` library for encryption, and the `werkzeug.security` module for password hashing. It allows users to create encrypted ZIP archives and decrypt them using a password.

## Features

- **Create Encrypted ZIP Files:** Securely compress and encrypt files into a ZIP archive.
- **Decrypt ZIP Files:** Decrypt previously encrypted ZIP files using a password.
- **Password Protection:** Passwords are hashed and stored securely to prevent unauthorized access.
- **Automatic Key Management:** Encryption keys are automatically generated and securely stored.

## Requirements

- Python 3.x
- Required Python libraries:
  - `click`
  - `cryptography`
  - `werkzeug`

Install the necessary libraries using pip:

```bash
pip install click cryptography werkzeug
```

## Usage

### Basic Commands

1. **Create an Encrypted ZIP File:**

    To create an encrypted ZIP file, use the following command:

    ```bash
    python zip.py create -pw
    ```

    You will be prompted to enter a password. After providing the password, specify the file path you want to encrypt. The tool will create an encrypted ZIP archive in the `ENC` folder.

2. **Decrypt an Encrypted ZIP File:**

    To decrypt an encrypted ZIP file, use the following command:

    ```bash
    python zip.py decrypt -pw
    ```

    After entering the correct password, the tool will list all available encrypted ZIP files. Select the one you want to decrypt by entering the corresponding number. The decrypted files will be extracted and stored in a newly created folder.

### Detailed Workflow

- **Encryption:**
  - The selected file is compressed into a ZIP archive.
  - The ZIP file is then encrypted using a randomly generated key.
  - The encryption key is stored securely in the `ENC` folder.

- **Decryption:**
  - The correct password must be provided to decrypt the ZIP file.
  - The corresponding encryption key is retrieved, and the ZIP file is decrypted.
  - The decrypted files are extracted and placed in a new folder.

## Code Overview

- **`cli(command, pw)`:** Main entry point for the command-line tool. Handles the `create` and `decrypt` commands.
- **`encrypt_zip(zip_filename, files)`:** Compresses and encrypts the specified files into a ZIP archive.
- **`list_all()`:** Lists all encrypted folders in the `ENC` directory.
- **`decrypt_zip(zip_filename)`:** Decrypts a selected ZIP archive and extracts the files.

## Contribution

Contributions are welcome! Feel free to fork the repository and submit a pull request with your enhancements.

