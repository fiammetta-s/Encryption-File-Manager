import zipfile
import os
import click
from datetime import datetime as dt
from cryptography.fernet import Fernet
from werkzeug.security import generate_password_hash, check_password_hash

# Define constants for folder and zip filename
folder = "ENC"
zip_filename = "encrypted.zip"

@click.command()
@click.argument("command", type=click.Choice(["create", "decrypt"]))
@click.option("-pw", help="Enter a password for accessing zip files", hide_input=True, prompt="Enter a password for accessing zip files")
def cli(command, pw):
    if not os.path.exists(folder):
        os.mkdir(folder)
        
    pw_path = folder + os.sep + "password.txt"
    
    if command == "create":
        pw_lower = pw.lower()
        pw_gen = generate_password_hash(pw_lower)
        
        if not os.path.exists(pw_path):
            with open(pw_path, "w") as w:
                w.write(pw_gen)
        else:
            with open(pw_path, "w") as w:
                w.write(pw_gen)
    
        file_path = input("Enter the file path to encrypt: ")
        files = [file_path]
        encrypt_zip(zip_filename, files)
        click.secho("Encrypted zip folder created successfully: {}".format(zip_filename), fg="red")
        
    elif command == "decrypt":
        with open(pw_path, "r") as r:
            pw_gen = r.readlines()[0]
            
        if check_password_hash(pw_gen, pw.lower()):
            decrypt_files = decrypt_zip(zip_filename)
            if decrypt_files is not None:
                click.secho("Zip folder decrypted successfully.", fg="blue")
                click.secho("Decrypted files: ", fg="yellow")
                for file in decrypt_files:
                    click.secho(file, fg="green")
        else:
            click.secho("Invalid password", fg="red")
    else:
        click.secho("Invalid input: Must be either 'create' or 'decrypt'", fg="red")

def encrypt_zip(zip_filename, files):
    fernet_key = Fernet.generate_key()
    cipher_suite = Fernet(fernet_key)
    sub_folder = "enc_" + dt.now().strftime("%Y_%m_%d_%H_%M_%S")
    full_path = folder + os.sep + sub_folder
    os.mkdir(full_path)
    with zipfile.ZipFile(full_path + os.sep + zip_filename, "w", zipfile.ZIP_DEFLATED) as z:
        for file in files:
            z.write(file, os.path.basename(file))
    with open(full_path + os.sep + "key.key", "wb") as key_file:
        key_file.write(fernet_key)
    with open(full_path + os.sep + zip_filename, "rb+") as z:
        encrypted_data = cipher_suite.encrypt(z.read())
        z.seek(0)
        z.write(encrypted_data)
        
def list_all():
    folders = os.listdir(folder)
    for f in range(len(folders)):
        if folders[f].startswith("enc_"):
            print(f, folders[f])
    return folders 
        
def decrypt_zip(zip_filename):
    folders = list_all()
    zf = input("Pick a zipfile to decrypt:")
    folder_index_list = [str(folders.index(i)) for i in folders if i.startswith("enc_")]
    if zf in folder_index_list:
        zf_int = int(zf)
    else:
        print("Invalid input: Must be an integer")
        return None
    sub_folder = folders[zf_int]
    full_path = folder + os.sep + sub_folder
    key_file_path = full_path + os.sep + "key.key"
    if not os.path.exists(key_file_path):
        print("Encryption key file not found.")
        return None
    with open(key_file_path, "rb") as key_file:
        fernet_key = key_file.read()
    cipher_suite = Fernet(fernet_key)
    with open(full_path + os.sep + zip_filename, "rb") as z:
        decrypted_data = cipher_suite.decrypt(z.read())
    with open(full_path + os.sep + zip_filename, "wb") as z:
        z.write(decrypted_data)
    decrypted_files = []
    with zipfile.ZipFile(full_path + os.sep + zip_filename, "r") as z:
        namelist = z.namelist()
        for file in namelist:
            z.extract(file)
            decrypted_files.append(file)  
    enc_name = folder + os.sep + sub_folder
    dec_name = folder + os.sep + sub_folder.replace("enc", "dec")
    os.rename(enc_name, dec_name)
    return decrypted_files


if __name__ == "__main__":
    cli()
