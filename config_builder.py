import tkinter as tk
from tkinter import font
from tkinter import filedialog
import os
import configparser
from functools import partial

ROOT = os.getcwd().replace('\\', '/')


class App:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.whitelist_last_index = 0
        self.blacklist_last_index = 0
        self.last_row = 6

        self.dom = tk.Tk()
        self.dom.title("Config builder tool")
        self.dom.geometry('620x400')
        self.dom.resizable(False, True)

        self.dom.file_choose_label = tk.Label(self.dom, text="Choose file config or create new")
        self.dom.file_choose_label.grid(column=0, row=0, pady=5, sticky=tk.W)
        self.dom.file_choose_button = tk.Button(self.dom, text="Browse", command=self.__load_config_file)
        self.dom.file_choose_button.grid(column=1, row=0, padx=10, pady=5, sticky=tk.W)

        self.dom.build_button = tk.Button(self.dom, text="Build", font=tk.font.Font(size=16, weight='bold'), bg='azure2', command=self.__build)
        self.dom.build_button.grid(column=10, row=10, sticky=tk.E + tk.S, pady=10)
        self.dom.build_button.grid_remove()

        self.dom.checkbox_silent_value = tk.BooleanVar()
        self.dom.checkbox_silent = tk.Checkbutton(self.dom, text="Silent", command=self.__checkbox_silent_change,
                                                  variable=self.dom.checkbox_silent_value)
        self.dom.checkbox_silent.grid(column=0, row=2, sticky=tk.W)
        self.dom.checkbox_silent.grid_remove()

        self.dom.checkbox_logging_value = tk.BooleanVar()
        self.dom.checkbox_logging = tk.Checkbutton(self.dom, text="Logging", command=self.__checkbox_logging_change,
                                                   variable=self.dom.checkbox_logging_value)
        self.dom.checkbox_logging.grid(column=0, row=3, sticky=tk.W)
        self.dom.checkbox_logging.grid_remove()

        self.dom.logfile_choose_label = tk.Label(self.dom, text="Select log file")
        self.dom.logfile_choose_label.grid(column=0, row=4, sticky=tk.W)
        self.dom.logfile_choose_label.grid_remove()
        self.dom.logfile_choose_button = tk.Button(self.dom, text="Browse", command=self.__load_log_file)
        self.dom.logfile_choose_button.grid(column=1, row=4, padx=10, sticky=tk.W)
        self.dom.logfile_choose_button.grid_remove()

        self.dom.whitelist_label = tk.Label(self.dom, text="WhiteList", font=tk.font.Font(size=16, weight='bold'))
        self.dom.whitelist_label.grid(column=0, row=5)
        self.dom.whitelist_label.grid_remove()
        self.dom.whitelist_files_select_button = tk.Button(self.dom, text="Add files",
                                                           command=self.__whitelist_add_files)
        self.dom.whitelist_files_select_button.grid(column=0, row=6, sticky=tk.E)
        self.dom.whitelist_files_select_button.grid_remove()
        self.dom.whitelist_dir_select_button = tk.Button(self.dom, text="Add dir",
                                                         command=self.__whitelist_add_dir)
        self.dom.whitelist_dir_select_button.grid(column=0, row=6, sticky=tk.W, padx=2)
        self.dom.whitelist_dir_select_button.grid_remove()
        self.dom.whitelist_files = dict()
        self.dom.whitelist_dirs = dict()

        self.dom.blacklist_label = tk.Label(self.dom, text="BlackList", font=tk.font.Font(size=16, weight='bold'))
        self.dom.blacklist_label.grid(column=0, row=7)
        self.dom.blacklist_label.grid_remove()
        self.dom.blacklist_files_select_button = tk.Button(self.dom, text="Add files",
                                                           command=self.__blacklist_add_files)
        self.dom.blacklist_files_select_button.grid(column=0, row=8, sticky=tk.E)
        self.dom.blacklist_files_select_button.grid_remove()
        self.dom.blacklist_dir_select_button = tk.Button(self.dom, text="Add dir",
                                                         command=self.__blacklist_add_dir)
        self.dom.blacklist_dir_select_button.grid(column=0, row=8, sticky=tk.W, padx=2)
        self.dom.blacklist_dir_select_button.grid_remove()
        self.dom.blacklist_files = dict()
        self.dom.blacklist_dirs = dict()

        self.dom.mainloop()

    def __blacklist_add_files(self):
        files_names = tk.filedialog.askopenfilenames(title="Select files", initialdir=ROOT)
        for file_path in files_names:
            if file_path not in self.config["BlackList"].values():
                self.blacklist_last_index += 1
                self.config["BlackList"][f"file{self.blacklist_last_index}"] = file_path
        self.__reload_dom_from_config()

    def __blacklist_add_dir(self):
        dir_ = tk.filedialog.askdirectory(title="Select dir", initialdir=ROOT)
        if len(dir_) and dir_ not in self.config["BlackList"].values():
            self.blacklist_last_index += 1
            self.config["BlackList"][f"dir{self.blacklist_last_index}"] = dir_
            self.__reload_dom_from_config()

    def __whitelist_add_files(self):
        files_names = tk.filedialog.askopenfilenames(title="Select files", initialdir=ROOT)
        for file_path in files_names:
            if file_path not in self.config["WhiteList"].values():
                self.whitelist_last_index += 1
                self.config["WhiteList"][f"file{self.whitelist_last_index}"] = file_path
        self.__reload_dom_from_config()

    def __whitelist_add_dir(self):
        dir_ = tk.filedialog.askdirectory(title="Select dir", initialdir=ROOT)
        if len(dir_) and dir_ not in self.config["WhiteList"].values():
            self.whitelist_last_index += 1
            self.config["WhiteList"][f"dir{self.whitelist_last_index}"] = dir_
            self.__reload_dom_from_config()

    def __checkbox_logging_change(self):
        self.config["Settings"]["logging"] = "1" if self.dom.checkbox_logging_value.get() else "0"
        if self.dom.checkbox_logging_value.get():
            self.dom.logfile_choose_button.grid()
            self.dom.logfile_choose_label.grid()
        else:
            self.dom.logfile_choose_button.grid_remove()
            self.dom.logfile_choose_label.grid_remove()

    def __checkbox_silent_change(self):
        self.config["Settings"]["silent"] = "1" if self.dom.checkbox_silent_value.get() else "0"

    def __load_log_file(self):
        log_file_name = tk.filedialog.askopenfilename(initialdir=ROOT + "/logs", title="Select log file",
                                                      filetypes=(("Log file", "*.log"), ('All files', "*.*")))
        if len(log_file_name):
            self.config["Settings"]["log_file"] = log_file_name
            self.dom.logfile_choose_button.configure(text=log_file_name)
        else:
            self.dom.logfile_choose_button.configure(text="Incorrect file")

    def __load_config_file(self):
        config_file_name = tk.filedialog.askopenfilename(
            initialdir=ROOT + "/configs", title="Choose config file",
            filetypes=(('Configuration file', "*.ini"), ('All files', "*.*")))

        if len(config_file_name):
            self.config_path = config_file_name
            self.config.read(self.config_path)
            self.__config_struct_builder()
            self.__reload_dom_from_config()
            self.__checkbox_logging_change()
            self.__get_last_whitelist_index()
            self.__get_last_blacklist_index()

            self.dom.file_choose_button.configure(text=self.config_path)
            self.dom.build_button.grid()
            self.dom.checkbox_silent.grid()
            self.dom.checkbox_logging.grid()
            self.dom.whitelist_label.grid()
            self.dom.whitelist_files_select_button.grid()
            self.dom.whitelist_dir_select_button.grid()
        else:
            self.config.clear()
            self.dom.file_choose_button.configure(text="Incorrect file")
            self.dom.build_button.grid_remove()
            self.dom.checkbox_silent.grid_remove()
            self.dom.checkbox_logging.grid_remove()
            self.dom.logfile_choose_button.grid_remove()
            self.dom.logfile_choose_label.grid_remove()
            self.dom.whitelist_label.grid_remove()
            self.dom.whitelist_files_select_button.grid_remove()
            self.dom.whitelist_dir_select_button.grid_remove()
            self.dom.blacklist_label.grid_remove()
            self.dom.blacklist_files_select_button.grid_remove()
            self.dom.blacklist_dir_select_button.grid_remove()

    def __reload_dom_from_config(self):
        self.dom.checkbox_silent_value.set(self.config["Settings"]["silent"] == "1")
        self.dom.checkbox_logging_value.set(self.config["Settings"]["logging"] == "1")
        self.last_row = 6
        self.__dom_clean()

        for key in sorted(self.config["WhiteList"].keys()):
            path = self.config["WhiteList"][key]
            label = tk.Label(self.dom, text=path)
            label.grid(row=self.last_row + 1, column=0, sticky=tk.W, columnspan=2)
            button = tk.Button(self.dom, text="Delete", command=partial(self.__delete_from_list, "WL", key))
            button.grid(row=self.last_row + 1, column=2, sticky=tk.E)
            self.last_row += 1
            if "dir" in key:
                label.configure(background="spring green")
                self.dom.whitelist_dirs[key] = (label, button)
            else:
                label.configure(background="lawn green")
                self.dom.whitelist_files[key] = (label, button)

        self.dom.blacklist_label.grid(column=0, row=self.last_row + 1)
        self.dom.blacklist_files_select_button.grid(column=0, row=self.last_row + 2, sticky=tk.E)
        self.dom.blacklist_dir_select_button.grid(column=0, row=self.last_row + 2, sticky=tk.W, padx=2)
        self.last_row += 2

        for key in sorted(self.config["BlackList"].keys()):
            path = self.config["BlackList"][key]
            label = tk.Label(self.dom, text=path)
            label.grid(row=self.last_row + 1, column=0, sticky=tk.W, columnspan=2)
            button = tk.Button(self.dom, text="Delete", command=partial(self.__delete_from_list, "BL", key))
            button.grid(row=self.last_row + 1, column=2, sticky=tk.E)
            self.last_row += 1
            if "dir" in key:
                label.configure(background="firebrick1")
                self.dom.blacklist_dirs[key] = (label, button)
            else:
                label.configure(background="firebrick3")
                self.dom.blacklist_files[key] = (label, button)

        self.dom.build_button.grid(column=2, row=self.last_row + 10, sticky=tk.E + tk.S, pady=10)

    def __dom_clean(self):
        for key in self.dom.whitelist_dirs:
            pair = self.dom.whitelist_dirs[key]
            pair[0].grid_forget()
            pair[1].grid_forget()
        self.dom.whitelist_dirs.clear()

        for key in self.dom.whitelist_files:
            pair = self.dom.whitelist_files[key]
            pair[0].grid_forget()
            pair[1].grid_forget()
        self.dom.whitelist_files.clear()

        for key in self.dom.blacklist_dirs:
            pair = self.dom.blacklist_dirs[key]
            pair[0].grid_forget()
            pair[1].grid_forget()

        for key in self.dom.blacklist_files:
            pair = self.dom.blacklist_files[key]
            pair[0].grid_forget()
            pair[1].grid_forget()

    def __config_struct_builder(self):
        if "Settings" not in self.config:
            self.config.add_section("Settings")
        if "silent" not in self.config["Settings"]:
            self.config["Settings"]["silent"] = "0"
        if "logging" not in self.config["Settings"]:
            self.config["Settings"]["logging"] = "0"
        if "log_file" not in self.config["Settings"]:
            self.config["Settings"]["log_file"] = "logs/log.log"
        if "WhiteList" not in self.config:
            self.config.add_section("WhiteList")
        if "BlackList" not in self.config:
            self.config.add_section("BlackList")

    def __delete_from_list(self, list_, key):
        if list_ == "WL":
            self.config.remove_option("WhiteList", key)
        elif list_ == "BL":
            self.config.remove_option("BlackList", key)
        self.__reload_dom_from_config()

    def __get_last_whitelist_index(self):
        for key in self.config["WhiteList"]:
            self.whitelist_last_index = max(int(''.join([s for s in key if s in '1234567890'])),
                                            self.whitelist_last_index)

    def __get_last_blacklist_index(self):
        for key in self.config["BlackList"]:
            self.blacklist_last_index = max(int(''.join([s for s in key if s in '1234567890'])),
                                            self.blacklist_last_index)

    def __build(self):
        with open(self.config_path, 'w') as cfg_file:
            self.config.write(cfg_file)


if __name__ == "__main__":
    app = App()
