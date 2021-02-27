import os
ROOT = os.getcwd().replace('\\', '/')


def main(config):
    """ Function which returns paths of all involved files """
    black_list = [path[1] for path in config['BlackList'].items()]
    white_list = [path[1] for path in config['WhiteList'].items()]
    black_files = transform_in_absolute_paths(black_list, ROOT)
    white_files = transform_in_absolute_paths(white_list, ROOT)
    return white_files.difference(black_files)


def transform_in_absolute_paths(all_path_list: list, root: str):
    """ Returns absolute paths of files from files list which contents files with mixed paths"""
    absolute_paths = set()
    for item in all_path_list:
        if not check_abs(item):
            if check_dir(item):
                absolute_paths.update(set(recursion_reading(item, root)))
            else:
                absolute_paths.add(root + '/' + item)
        else:
            if check_dir(item):
                absolute_paths.update(set(recursion_reading(item)))
            else:
                absolute_paths.add(item)
    return absolute_paths


def recursion_reading(directory: str, root: str = ''):
    """ Wrapper over os.walk """
    files_paths = []
    for item in os.walk(directory):
        files_paths += [root + '/' + (item[0] + '\\' + path).replace('\\', '/') for path in item[2]]
    return files_paths


def check_dir(path: str):
    """ Returns true if path is directory"""
    return os.path.isdir(path)


def check_abs(path: str):
    """ Returns true if path is absolute"""
    return os.path.isabs(path)
