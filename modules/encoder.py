import os


def string_xor(first, second):
    return str(int(first) ^ int(second))


def bin_hash(string: str):
    """ Returns hash of string in bin format. """
    hsh = bin(hash(string))
    return str(hsh[2:])


def encrypt(path, password, attempt=0):
    # TODO
    if attempt < 5:
        try:
            pwd = bin_hash(password)
            with open(f'{path}.!~cpt', 'wb') as new:
                with open(f'{path}', 'rb') as file:
                    i = 0
                    for symbol in file.read():
                        print(symbol)
                        symbol = str(symbol)[2:]
                        new.write(bytes(string_xor(pwd[i%len(pwd)], symbol)))
                        i += 1
            os.remove(path)
            os.rename(path+".!~cpt", path)
        except KeyError:
            print(f'ERROR in file {path}. Try #{attempt}')
            encrypt(path, password, attempt+1)


def decrypt(path, password, attempt=0):
    # TODO
    if attempt < 5:
        try:
            pwd = bin_hash(password)
            with open(f'{path}.!~dpt', 'wb') as new:
                with open(f'{path}', 'rb') as file:
                    i = 0
                    for symbol in file.read():
                        symbol = str(symbol)[2:]
                        new.write(bytes(string_xor(pwd[i%len(pwd)], symbol)))
                        i += 1
            os.remove(path)
            os.rename(path+".!~dpt", path)
        except KeyError:
            print(f'ERROR in file {path}. Try #{attempt}')
            decrypt(path, password, attempt+1)