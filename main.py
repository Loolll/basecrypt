import sys
import os
import configparser
import argparse
import time
from modules.__files_including__ import main as include
import modules.language as language
import modules.encoder as encoder
from modules.logging import print


def __init__():
    # Parsing args form cli
    parser = argparse.ArgumentParser()
    parser.add_argument('-e', '--encrypt', help='Use it when you want to encrypt your files', action='store_true')
    parser.add_argument('-d', '--decrypt', help='Use it when you want to decrypt your files', action='store_true')
    parser.add_argument('-p', '--password', help='Use it to set password')
    parser.add_argument('-c', '--config', help='Loads config from this file. Default is settings.ini',
                        default='settings.ini')
    parser.add_argument('-s', '--silent', help='Silent mod', action='store_true')
    parser.add_argument('-l', '--logging', help='Logged all moves in log file', action='store_true')
    namespace = parser.parse_args(sys.argv[1:])

    # Config load part
    config = configparser.ConfigParser()
    config.read(namespace.config)

    # Files including
    files_paths = include(config)

    # Check preferences (check README)
    logging = config['Settings']['logging'] == '1' or namespace.logging
    silent = config['Settings']['silent'] == '1' or namespace.silent
    path_log = config['Settings']['log_file'] if len(config['Settings']['log_file']) else 'log.log'

    # Check assertions
    assert 'encrypt' in dir(encoder), "Encoder module doesn't contains 'encrypt' function."
    assert 'decrypt' in dir(encoder), "Encoder module doesn't contains 'decrypt' function."
    assert 'pass_correct' in dir(language), "Language module doesn't contains 'pass_correct' function."
    assert sum([namespace.decrypt, namespace.encrypt]) == 1, 'Please check main arg and try again.'
    assert namespace.password, 'Please set password and try again.'
    assert language.pass_correct(namespace.password), 'Password contains incorrect symbols.'
    assert len(files_paths), 'File list is empty.'

    # Transforming password if need (Check README)
    password = language.wrapper_over(namespace.password)

    return namespace, files_paths, password, silent, logging, path_log


if __name__ == '__main__':
    namespace, paths, password, silent, logging, path_log = __init__()
    global_start = time.time()

    function = None
    if namespace.encrypt:
        function = encoder.encrypt
        print(f'MODE: ENCRYPT {"-" * 65}',
              silent=True, logging=True, path_log=path_log)
    elif namespace.decrypt:
        function = encoder.decrypt
        print(f'MODE: DECRYPT {"-" * 65}',
              silent=True, logging=True, path_log=path_log)

    for path in paths:
        if os.path.exists(path):
            start = time.time()
            function(path=path, password=password)
            print(f"{path} OK IN ~{str(time.time() - start)[:5]}s",
                  silent=silent, logging=logging, path_log=path_log)
        else:
            print(f"{path} FILE DOESN'T EXISTS. SKIPPED",
                  silent=silent, logging=logging, path_log=path_log)

    print(f"OK. Total time ~"
          f"{str(time.time() - global_start)[:5]}s {'-' * 56}",
          silent=silent, logging=logging, path_log=path_log)
