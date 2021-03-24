import modules.encoder as crypt
import os


def crypt_test():
    text = '3fadshfgiDIUGBYU9E38GT2389HJAKDFB723Y40-8U2-0E9FBAUGFB\nSDOAISPDFAJGFPIAasdasojdashf\nasdhashfdgaqancbvq832'
    path = os.getcwd().replace("\\", '/') + "/text.txt"
    password = 'hgiaojfgvbagi'
    with open(path, 'w') as file:
        file.write(text)
    crypt.encrypt(path, password)
    crypt.decrypt(path, password)
    new_text = ''
    with open(path, 'r') as file:
        new_text = file.read()
    if new_text != text:
        print("INCORRECT ENCODER MODULE")
    os.remove(path)


if __name__ == "__main__":
    crypt_test()