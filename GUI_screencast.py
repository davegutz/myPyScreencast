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
import platform
global putty_shell


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


if __name__ == '__main__':
    import os
    import tkinter as tk
    from tkinter import ttk
    result_ready = 0
    thread_active = 0

    # Configuration for entire folder selection read with filepaths
    def_dict = {
                'Linux':   {"title": '',
                            "rec_time": '6.',
                            "crf": '25',
                            "video_grabber": 'x11grab',
                            "video_in": ':0.0+0.0',
                            "audio_grabber": 'pulse',
                            "audio_in": 'default',
                            "silent": '1',
                            "video_delay": '0.0'},
                'Windows': {"title": '',
                            "rec_time": '6.',
                            "crf": '28',
                            "video_grabber": "gdigrab",
                            "video_in": 'desktop',
                            "audio_grabber": 'dshow',
                            "audio_in": 'audio="CABLE Output (VB-Audio Virtual Cable)"',
                            "silent": '1',
                            "video_delay": '0.0'},
                'Darwin':  {"title": '',
                            "rec_time": '6.',
                            "crf": '25',
                            "video_grabber": 'avfoundation',
                            "video_in": '1',
                            "audio_grabber": '',
                            "audio_in": '2',
                            "silent": '1',
                            "video_delay": '0.0'},
                }
    cf = Begini(__file__, def_dict)

    # Frame properties
    min_width = 800
    main_height = 500
    wrap_length = 800
    bg_color = "lightgray"
    plate = platform.system()

    # Globals
    master = tk.Tk()
    master.title('Screencast')
    master.wm_minsize(width=min_width, height=main_height)
    script_loc = os.path.dirname(os.path.abspath(__file__))
    cwd_path = tk.StringVar(master, os.getcwd())
    path_to_data = tk.StringVar(master, os.path.join(cwd_path.get(), '../dataReduction'))
    master.iconphoto(False, tk.PhotoImage(file=os.path.join(script_loc, 'GUI_screencast_Icon.png')))
    title = tk.StringVar(master, cf[plate]['title'])
    rec_time = tk.DoubleVar(master, float(cf[plate]['rec_time']))
    crf = tk.IntVar(master, int(cf[plate]['crf']))
    video_grabber = tk.StringVar(master, cf[plate]['video_grabber'])
    video_in = tk.StringVar(master, cf[plate]['video_in'])
    audio_grabber = tk.StringVar(master, cf[plate]['audio_grabber'])
    audio_in = tk.StringVar(master, cf[plate]['audio_in'])
    silent = tk.BooleanVar(master, bool(cf[plate]['silent']))
    video_delay = tk.DoubleVar(master, float(cf[plate]['video_delay']))

    # Name row
    folder_button = tk.Button(master, text=path_to_data.get(), command='enter destination folder', fg="blue", bg=bg_color)
    title_button = tk.Button(master, text=title.get(), command='enter title', fg="blue", bg=bg_color)
    tk.Label(master, text="Location", fg="blue").grid(row=0, column=0, sticky=tk.N, pady=2)
    tk.Label(master, text="Title", fg="blue").grid(row=0, column=1, sticky=tk.N, pady=2)
    silent_button = tk.Checkbutton(master, text='silent', bg=bg_color, variable=silent,
                                   onvalue=True, offvalue=False)
    silent_button.grid(row=0, column=3, pady=2, sticky=tk.N)

    # Size row
    tk.Label(master, text="Sizes").grid(row=1, column=0, pady=2)
    title_button.grid(row=1, column=1, pady=2)

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
