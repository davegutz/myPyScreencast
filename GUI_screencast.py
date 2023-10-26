#  Graphical interface to screencast recorder
#  Run in PyCharm
#     or
#  'python3 GUI_screencast.py
#
#  2023-Oct-26  Dave Gutz   Create
# Copyright (C) 2023 Dave Gutz
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# See http://www.fsf.org/licensing/licenses/lgpl.txt for full license text.

"""Define a class to manage configuration using files for memory (poor man's database)"""
import time
from configparser import ConfigParser
import re
from tkinter import ttk, filedialog
import tkinter.simpledialog
import tkinter.messagebox
import shutil
import pyperclip
import subprocess
import datetime
global putty_shell

# Defaults for initialization of ini
defaults = {'Darwin': ('', '', ("For general purpose running", "'save data' will present a choice of file name", "")),
          'Windows': ('Ff0;D^0;Ca.5;Xp0;W4;Xm247;DP1;Dr100;W2;HR;Pf;v2;Xv.002;Xu1;W200;Xu0;Xv1;W100;v0;Pf;', 'Hd;Xp0;Xu0;Xv1;Ca.5;v0;Rf;Pf;DP4;', ("Run for 60 sec.   Plots DOM 1 Fig 2 or 3 should show Tb was detected as fault but not failed.",)),
          'Linux': ('Ff0;D^0;Ca.5;Xp0;W4;Xm246;DP1;Dr100;W2;HR;Pf;v2;Xv.002;W50;Xu1;W200;Xu0;Xv1;W100;v0;Pf;', 'Hd;Xp0;Xu0;Xv1;Ca.5;v0;Rf;Pf;DP4;', ("Run for 60 sec.   Plots DOM 1 Fig 2 or 3 should show Tb was detected as fault but not failed.", "'Xp0' in reset puts Xm back to 247.")),
          }


# Begini - configuration class using .ini files
class Begini(ConfigParser):

    def __init__(self, name, def_dict_):
        ConfigParser.__init__(self)

        (config_path, config_basename) = os.path.split(name)
        config_txt = os.path.splitext(config_basename)[0] + '.ini'
        self.config_file_path = os.path.join(config_path, config_txt)
        print('config file', self.config_file_path)
        if os.path.isfile(self.config_file_path):
            self.read(self.config_file_path)
        else:
            with open(self.config_file_path, 'w') as cfg_file:
                self.read_dict(def_dict_)
                self.write(cfg_file)
            print('wrote', self.config_file_path)

    # Get an item
    def get_item(self, ind, item):
        return self[ind][item]

    # Put an item
    def put_item(self, ind, item, value):
        self[ind][item] = value
        self.save_to_file()

    # Save again
    def save_to_file(self):
        with open(self.config_file_path, 'w') as cfg_file:
            self.write(cfg_file)
        print('wrote', self.config_file_path)


# Global methods
def add_to_clip_board(text):
    pyperclip.copy(text)


# Split all information contained in file path
def contain_all(testpath):
    folder_path, basename = os.path.split(testpath)
    parent, txt = os.path.split(folder_path)
    # get key
    key = ''
    with open(testpath, 'r') as file:
        for line in file:
            if line.__contains__(txt):
                us_loc = line.find('_' + txt)
                key = (basename, line[:us_loc])
                break
    return folder_path, parent, basename, txt, key


def create_file_txt(option_, unit_, battery_):
    return option_ + '_' + unit_ + '_' + battery_ + '.csv'


def lookup_default():
    start_val, reset_val, ev_val = defaults.get(option.get())
    start.set(start_val)
    start_button.config(text=start.get())
    reset.set(reset_val)
    reset_button.config(text=reset.get())
    while len(ev_val) < 4:
        ev_val = ev_val + ('',)
    if ev_val[0]:
        ev1_label.config(text='-' + ev_val[0])
    else:
        ev1_label.config(text='')
    if ev_val[1]:
        ev2_label.config(text='-' + ev_val[1])
    else:
        ev2_label.config(text='')
    if ev_val[2]:
        ev3_label.config(text='-' + ev_val[2])
    else:
        ev3_label.config(text='')
    if ev_val[3]:
        ev4_label.config(text='-' + ev_val[3])
    else:
        ev4_label.config(text='')


def option_handler(*args):
    lookup_start()
    option_ = option.get()
    option_show.set(option_)
    cf['others']['option'] = option_
    cf.save_to_file()
    Test.create_file_path_and_key()
    Ref.create_file_path_and_key()
    save_data_button.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='black', text='save data')
    save_data_as_button.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='black', text='save data as')
    start_button.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='purple')
    reset_button.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='purple')



def ref_remove():
    ref_label.grid_remove()
    Ref.version_button.grid_remove()
    Ref.unit_button.grid_remove()
    Ref.battery_button.grid_remove()
    Ref.key_label.grid_remove()
    Ref.label.grid_remove()
    run_button.config(text='Compare Run Sim')


def ref_restore():
    ref_label.grid()
    Ref.version_button.grid()
    Ref.unit_button.grid()
    Ref.battery_button.grid()
    Ref.key_label.grid()
    Ref.label.grid()
    run_button.config(text='Compare Run Run')


def save_data():
    if os.path.getsize(putty_test_csv_path.get()) > 512:  # bytes
        # create empty file
        try:
            open(empty_csv_path.get(), 'x')
        except FileExistsError:
            pass
        # For custom option, redefine Test.file_path if requested
        new_file_txt = None
        if option.get() == 'custom':
            new_file_txt = tk.simpledialog.askstring(title=__file__, prompt="custom file name string:")
            if new_file_txt is not None:
                Test.create_file_path_and_key(name_override=new_file_txt)
                Test.label.config(text=Test.file_txt)
                print('Test.file_path', Test.file_path)
        if os.path.isfile(Test.file_path) and os.path.getsize(Test.file_path) > 0:  # bytes
            confirmation = tk.messagebox.askyesno('query overwrite', 'File exists:  overwrite?')
            if confirmation is False:
                print('reset and use clear')
                tkinter.messagebox.showwarning(message='reset and use clear')
                return
        copy_clean(putty_test_csv_path.get(), Test.file_path)
        print('copied ', putty_test_csv_path.get(), '\nto\n', Test.file_path)
        save_data_button.config(bg='green', activebackground='green', fg='red', activeforeground='red', text='data saved')
        save_data_as_button.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='black', text='data saved')
        shutil.copyfile(empty_csv_path.get(), putty_test_csv_path.get())
        print('emptied', putty_test_csv_path.get())
        try:
            os.remove(empty_csv_path.get())
        except OSError:
            pass
        print('updating Test file label')
        Test.create_file_path_and_key(name_override=new_file_txt)
    else:
        print('putty test file is too small (<512 bytes) probably already done')
        tkinter.messagebox.showwarning(message="Nothing to save")
    start_button.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='purple')
    reset_button.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='purple')


def save_data_as():
    if os.path.getsize(putty_test_csv_path.get()) > 512:  # bytes
        # create empty file
        try:
            open(empty_csv_path.get(), 'x')
        except FileExistsError:
            pass
        # For custom option, redefine Test.file_path if requested
        if option.get() == 'custom':
            new_file_txt = tk.simpledialog.askstring(title=__file__, prompt="custom file name string:")
            if new_file_txt is not None:
                Test.create_file_path_and_key(name_override=new_file_txt)
                Test.label.config(text=Test.file_txt)
                print('Test.file_path', Test.file_path)
        else:
            new_file_txt = tk.simpledialog.askstring(title=__file__, prompt="custom file name string:",
                                                     initialvalue=Test.file_txt)
            if new_file_txt is not None:
                Test.create_file_path_and_key(name_override=new_file_txt)
                Test.label.config(text=Test.file_txt)
                print('Test.file_path', Test.file_path)
        if os.path.isfile(Test.file_path) and os.path.getsize(Test.file_path) > 0:  # bytes
            confirmation = tk.messagebox.askyesno('query overwrite', 'File exists:  overwrite?')
            if confirmation is False:
                print('reset and use clear')
                tkinter.messagebox.showwarning(message='reset and use clear')
                return
        copy_clean(putty_test_csv_path.get(), Test.file_path)
        print('copied ', putty_test_csv_path.get(), '\nto\n', Test.file_path)
        save_data_button.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='black', text='data saved')
        save_data_as_button.config(bg='green', activebackground='green', fg='red', activeforeground='red', text='data saved as')
        shutil.copyfile(empty_csv_path.get(), putty_test_csv_path.get())
        print('emptied', putty_test_csv_path.get())
        try:
            os.remove(empty_csv_path.get())
        except OSError:
            pass
        print('updating Test file label')
        Test.create_file_path_and_key(name_override=new_file_txt)
    else:
        print('putty test file is too small (<512 bytes) probably already done')
        tkinter.messagebox.showwarning(message="Nothing to save")
    start_button.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='purple')
    reset_button.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='purple')


if __name__ == '__main__':
    import os
    import tkinter as tk
    from tkinter import ttk
    result_ready = 0
    thread_active = 0

    # Configuration for entire folder selection read with filepaths
    def_dict = {'test': {"version": "g20230530",
                         "unit": "pro1a",
                         "battery": "bb"},
                'ref':  {"version": "v20230403",
                         "unit": "pro1a",
                         "battery": "bb"},
                'others': {"option": "custom",
                           'modeling': True}
                }

    cf = Begini(__file__, def_dict)

    # Define frames
    min_width = 800
    main_height = 500
    wrap_length = 800
    bg_color = "lightgray"

    # Master and header
    master = tk.Tk()
    master.title('State of Charge')
    master.wm_minsize(width=min_width, height=main_height)
    # master.geometry('%dx%d' % (master.winfo_screenwidth(), master.winfo_screenheight()))
    pwd_path = tk.StringVar(master)
    pwd_path.set(os.getcwd())
    path_to_data = os.path.join(pwd_path.get(), '../dataReduction')
    print(path_to_data)
    icon_path = os.path.join(ex_root.script_loc, 'TestSOC_Icon.png')
    master.iconphoto(False, tk.PhotoImage(file=icon_path))
    tk.Label(master, text="Item", fg="blue").grid(row=0, column=0, sticky=tk.N, pady=2)
    tk.Label(master, text="Test", fg="blue").grid(row=0, column=1, sticky=tk.N, pady=2)
    modeling = tk.BooleanVar(master)
    modeling.set(bool(cf['others']['modeling']))
    modeling_button = tk.Checkbutton(master, text='modeling', bg=bg_color, variable=modeling,
                                     onvalue=True, offvalue=False)
    modeling_button.grid(row=0, column=3, pady=2, sticky=tk.N)
    modeling.trace_add('write', modeling_handler)
    ref_label = tk.Label(master, text="Ref", fg="blue")
    ref_label.grid(row=0, column=4, sticky=tk.N, pady=2)

    # Version row
    tk.Label(master, text="Version").grid(row=1, column=0, pady=2)
    Test.version_button = tk.Button(master, text=Test.version, command=Test.enter_version, fg="blue", bg=bg_color)
    Test.version_button.grid(row=1, column=1, pady=2)
    Ref.version_button = tk.Button(master, text=Ref.version, command=Ref.enter_version, fg="blue", bg=bg_color)
    Ref.version_button.grid(row=1, column=4, pady=2)

    # Unit row
    tk.Label(master, text="Unit").grid(row=2, column=0, pady=2)
    Test.unit_button = tk.Button(master, text=Test.unit, command=Test.enter_unit, fg="purple", bg=bg_color)
    Test.unit_button.grid(row=2, column=1, pady=2)
    Ref.unit_button = tk.Button(master, text=Ref.unit, command=Ref.enter_unit, fg="purple", bg=bg_color)
    Ref.unit_button.grid(row=2, column=4, pady=2)

    # Battery row
    tk.Label(master, text="Battery").grid(row=3, column=0, pady=2)
    Test.battery_button = tk.Button(master, text=Test.battery, command=Test.enter_battery, fg="green", bg=bg_color)
    Test.battery_button.grid(row=3, column=1, pady=2)
    Ref.battery_button = tk.Button(master, text=Ref.battery, command=Ref.enter_battery, fg="green", bg=bg_color)
    Ref.battery_button.grid(row=3, column=4, pady=2)

    # Key row
    tk.Label(master, text="Key").grid(row=4, column=0, pady=2)
    Test.key_label = tk.Label(master, text=Test.key)
    Test.key_label.grid(row=4, column=1,  padx=5, pady=5)
    Ref.key_label = tk.Label(master, text=Ref.key)
    Ref.key_label.grid(row=4, column=4, padx=5, pady=5)

    # Image
    pic_path = os.path.join(ex_root.script_loc, 'TestSOC.png')
    picture = tk.PhotoImage(file=pic_path).subsample(5, 5)
    label = tk.Label(master, image=picture)
    label.grid(row=1, column=2, columnspan=2, rowspan=3, padx=5, pady=5)

    # Option
    tk.ttk.Separator(master, orient='horizontal').grid(row=5, columnspan=5, pady=5, sticky='ew')
    option = tk.StringVar(master)
    option.set(str(cf['others']['option']))
    option_show = tk.StringVar(master)
    option_show.set(str(cf['others']['option']))
    sel = tk.OptionMenu(master, option, *sel_list)
    sel.config(width=20)
    sel.grid(row=6, padx=5, pady=5, sticky=tk.W)
    option.trace_add('write', option_handler)
    Test.label = tk.Label(master, text=Test.file_txt)
    Test.label.grid(row=6, column=1, padx=5, pady=5)
    Ref.label = tk.Label(master, text=Ref.file_txt)
    Ref.label.grid(row=6, column=4, padx=5, pady=5)
    Test.create_file_path_and_key(cf['others']['option'])
    Ref.create_file_path_and_key(cf['others']['option'])

    start = tk.StringVar(master)
    start.set('')
    start_label = tk.Label(master, text='copy start:')
    start_label.grid(row=8, column=0, padx=5, pady=5)
    start_button = tk.Button(master, text='', command=grab_start, fg="purple", bg=bg_color, wraplength=wrap_length,
                             justify=tk.LEFT, font=("Arial", 8))
    start_button.grid(sticky="W", row=8, column=1, columnspan=4, rowspan=2, padx=5, pady=5)

    reset = tk.StringVar(master)
    reset.set('')
    reset_label = tk.Label(master, text='copy reset:')
    reset_label.grid(row=10, column=0, padx=5, pady=5)
    reset_button = tk.Button(master, text='', command=grab_reset, fg="purple", bg=bg_color, wraplength=wrap_length,
                             justify=tk.LEFT, font=("Arial", 8))
    reset_button.grid(sticky="W", row=10, column=1, columnspan=4, rowspan=2, padx=5, pady=5)

    ev1_label = tk.Label(master, text='', wraplength=wrap_length, justify=tk.LEFT)
    ev1_label.grid(sticky="W", row=12, column=1, columnspan=4, padx=5, pady=5)

    ev2_label = tk.Label(master, text='', wraplength=wrap_length, justify=tk.LEFT)
    ev2_label.grid(sticky="W", row=13, column=1, columnspan=4, padx=5, pady=5)

    ev3_label = tk.Label(master, text='', wraplength=wrap_length, justify=tk.LEFT)
    ev3_label.grid(sticky="W", row=14, column=1, columnspan=4, padx=5, pady=5)

    ev4_label = tk.Label(master, text='', wraplength=wrap_length, justify=tk.LEFT)
    ev4_label.grid(sticky="W", row=15, column=1, columnspan=4, padx=5, pady=5)

    save_data_label = tk.Label(master, text='save data:')
    save_data_label.grid(row=16, column=0, padx=5, pady=5)
    save_data_button = tk.Button(master, text='save data', command=save_data, fg="red", bg=bg_color, wraplength=wrap_length, justify=tk.LEFT)
    save_data_button.grid(sticky="W", row=16, column=1, padx=5, pady=5)
    save_data_as_button = tk.Button(master, text='save as', command=save_data_as, fg="red", bg=bg_color, wraplength=wrap_length, justify=tk.LEFT)
    save_data_as_button.grid(sticky="W", row=16, column=2, padx=5, pady=5)
    clear_data_button = tk.Button(master, text='clear', command=clear_data, fg="red", bg=bg_color, wraplength=wrap_length, justify=tk.RIGHT)
    clear_data_button.grid(sticky="W", row=16, column=3, padx=5, pady=5)

    tk.ttk.Separator(master, orient='horizontal').grid(row=17, columnspan=5, pady=5, sticky='ew')
    run_button = tk.Button(master, text='Compare', command=compare_run, fg="green", bg=bg_color, wraplength=wrap_length, justify=tk.LEFT)
    run_button.grid(row=18, column=0, padx=5, pady=5)

    tk.ttk.Separator(master, orient='horizontal').grid(row=19, columnspan=5, pady=5, sticky='ew')
    choose_label = tk.Label(master, text='choose existing files:')
    choose_label.grid(row=20, column=0, padx=5, pady=5)
    run_sim_choose_button = tk.Button(master, text='Compare Run Sim Choose', command=compare_run_sim_choose, fg="blue", bg=bg_color, wraplength=wrap_length, justify=tk.LEFT)
    run_sim_choose_button.grid(sticky="W", row=20, column=1, padx=5, pady=5)
    run_run_choose_button = tk.Button(master, text='Compare Run Run Choose', command=compare_run_run_choose, fg="blue", bg=bg_color, wraplength=wrap_length, justify=tk.LEFT)
    run_run_choose_button.grid(sticky="W", row=20, column=2, padx=5, pady=5)

    # Begin
    option_handler()
    master.mainloop()
