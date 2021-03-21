import os


def encrypt(path, password, attempt=0):
    # TODO
    if attempt < 5:
        try:
            pwd = password
            with open(f'{path}.!~cpt', 'wb') as new:
                with open(f'{path}', 'rb') as file:
                    for i, symbol in enumerate(file.read()):
                        ns = symbol ^ ord(pwd[i%len(pwd)])
                        new.write(bytes([ns]))
            os.remove(path)
            os.rename(path+".!~cpt", path)
        except KeyError:
            print(f'ERROR in file {path}. Try #{attempt}')
            encrypt(path, password, attempt+1)


def decrypt(path, password, attempt=0):
    # TODO
    if attempt < 5:
        try:
            pwd = password
            with open(f'{path}.!~dpt', 'wb') as new:
                with open(f'{path}', 'rb') as file:
                    for i, symbol in enumerate(file.read()):
                        ns = symbol ^ ord(pwd[i%len(pwd)])
                        new.write(bytes([ns]))
            os.remove(path)
            os.rename(path+".!~dpt", path)
        except KeyError:
            print(f'ERROR in file {path}. Try #{attempt}')
            decrypt(path, password, attempt+1)