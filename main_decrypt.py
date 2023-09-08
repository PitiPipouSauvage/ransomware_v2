#!/usr/bin/env python3

"""Decryption file !"""

from cryptography.fernet import Fernet 
import os 
import sys

decision = input("Do you want to decrypt a single directory (c) or do you want to decrypt all subdirectories from source (a) ? [c/a] ")

def decrypt(dir):
    content = os.listdir(dir)
    with open("key.key", "rb") as key:
        decryption_key = key.read()

    for file_id in range(len(content)):
        file_name = dir + "/" +content[file_id]

        if content[file_id] == "key.key" or content[file_id] == "main_decrypt.py":
            continue

        with open(content[file_id], 'wb') as encrypted_file:

            fernet = Fernet(key=decryption_key)
            decrypted_text = Fernet.decrypt(fernet, decryption_key)
            encrypted_file.write(decrypted_text) 

        advancment = (100 * (file_id + 1)) / len(content)
        print(f"[{file_id + 1}/{len(content)}]" + "[" + "#" * int(advancment / 10) + " " * (10 - int(advancment / 10)) + "]" , f"{advancment}%" , f"Decrypting {file_name}...", end="\r")

    print("\n")
    message()


def recursive_decrypt(root):
    print("Finding files...", end="")
    all_files = tuple(os.walk(root))
    print("Done", f"{len(all_files)} files found")
    
    print("Getting decryption key..." , end='')

    with open('key.key', 'rb') as key:
        decryption_key = key.read()
    
    print("Done") 

    for dir_id in range(len(all_files)):

        for file_id in range(len(all_files[dir_id][2])):
            file_name = all_files[dir_id][0] + "/" + all_files[dir_id][2][file_id]

            if all_files[dir_id][2][file_id] == 'key.key' or all_files[dir_id][2][file_id] == 'main_decrypt.py':
                continue

            with open(file_name, 'wb') as encrypted_file:

                fernet = Fernet(key=decryption_key)
                decrypted_text = fernet.decrypt(decryption_key)
                decrypted_file.write(decrypted_text)
                
        total_advancment = int((100 * (dir_id + 1)) / len(all_files))
        current_folder = all_files[dir_id][0].split("/")[-1]
        print(f"[{dir_id + 1}/{len(all_files)}]" + "[" + "#" * total_advancment + " " * (100 - total_advancment) + "]", f"{total_advancment}%", f"Encrypting {current_folder}...", end="\r")
    print("")

if decision == 'c':
    dir = input("What directory do you wish to decrypt ? (RECOMMENDED: use absolute path): ")
    decrypt(dir)

elif decision == 'a':
    root = input("From wich root file do you want to decrypt ? (RECOMMENDED: use absolute path): ")
    recursive_decrypt(root)
