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
from configparser import ConfigParser
import platform
if platform.system() == 'Darwin':
    import ttwidgets as tktt
else:
    import tkinter as tk
from tkinter import ttk, filedialog
import tkinter.simpledialog
from screencast import screencast, delay_audio_sync, delay_video_sync
# import tkinter.messagebox
import pyperclip
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


def enter_audio_grabber():
    audio_grabber.set(tk.simpledialog.askstring(title=__file__, prompt="ffmpeg audio_grabber parameter"))


def enter_audio_in():
    audio_in.set(tk.simpledialog.askstring(title=__file__, prompt="ffmpeg audio_in parameter"))


def enter_crf():
    crf.set(tk.simpledialog.askinteger(title=__file__, prompt="enter ffmpeg crf, lower is larger file"))
    cf[plate]['crf'] = str(crf.get())
    cf.save_to_file()
    crf_button.config(text=crf.get())


def enter_destination_folder():
    destination_folder.set(tk.filedialog.askdirectory(title="Select a Recordings Folder", initialdir=destination_folder.get()))
    cf[plate]['folder'] = str(destination_folder.get())
    cf.save_to_file()
    destination_folder_button.config(text=destination_folder.get())


def enter_rec_time():
    rec_time.set(tk.simpledialog.askfloat(title=__file__, prompt="enter record time, seconds"))
    cf[plate]['rec_time'] = str(rec_time.get())
    cf.save_to_file()
    time_button.config(text=rec_time.get())


def enter_title():
    title.set(tk.simpledialog.askstring(title=__file__, prompt="enter title"))
    if title.get() == '':
        title.set('enter title')
    cf[plate]['title'] = title.get()
    cf.save_to_file()
    title_button.config(text=title.get())


def enter_video_grabber():
    video_grabber.set(tk.simpledialog.askstring(title=__file__, prompt="ffmpeg video_grabber parameter"))


def enter_video_in():
    video_in.set(tk.simpledialog.askstring(title=__file__, prompt="ffmpeg video_in parameter"))


def record():
    raw_file, result_ready = screencast(silent=silent.get(),
                                        video_grabber=video_grabber.get(), video_in=video_in.get(),
                                        audio_grabber=audio_grabber.get(), audio_in=audio_in.get(),
                                        crf=crf.get(),
                                        rec_time=rec_time.get(),
                                        output_file=os.path.join(os.getcwd(), 'screencast.mkv'))
    if result_ready:
        if video_delay.get() >= 0.0:
            delay_video_sync(silent=silent.get(), delay=video_delay.get(), input_file=raw_file,
                             output_file=os.path.join(os.getcwd(), destination_path.get()))
        else:
            delay_audio_sync(silent=silent.get(), delay=-video_delay.get(), input_file=raw_file,
                             output_file=os.path.join(os.getcwd(), destination_path.get()))

    record_button.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='purple')


if __name__ == '__main__':
    import os
    import tkinter as tk
    from tkinter import ttk

    # Configuration for entire folder selection read with filepaths
    def_dict = {
                'Linux':   {"title":  'enter title of recording',
                            "rec_time": '6.',
                            "crf": '25',
                            "video_grabber": 'x11grab',
                            "video_in": ':0.0+0.0',
                            "audio_grabber": 'pulse',
                            "audio_in": 'default',
                            "silent": '1',
                            "video_delay": '0.0'},
                'Windows': {"title": "enter title of recording",
                            "rec_time": '6.',
                            "crf": '28',
                            "video_grabber": "gdigrab",
                            "video_in": 'desktop',
                            "audio_grabber": 'dshow',
                            "audio_in": 'audio="CABLE Output (VB-Audio Virtual Cable)"',
                            "silent": '1',
                            "video_delay": '0.0'},
                'Darwin':  {"title":  'enter title of recording',
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
    destination_folder = tk.StringVar(master, os.path.join(cwd_path.get(), './'))
    master.iconphoto(False, tk.PhotoImage(file=os.path.join(script_loc, 'GUI_screencast_Icon.png')))
    title = tk.StringVar(master, cf[plate]['title'])
    destination_path = tk.StringVar(master, os.path.join(destination_folder.get(), title.get()+'.mkv'))
    rec_time = tk.DoubleVar(master, float(cf[plate]['rec_time']))
    crf = tk.IntVar(master, int(cf[plate]['crf']))
    video_grabber = tk.StringVar(master, cf[plate]['video_grabber'])
    video_in = tk.StringVar(master, cf[plate]['video_in'])
    audio_grabber = tk.StringVar(master, cf[plate]['audio_grabber'])
    audio_in = tk.StringVar(master, cf[plate]['audio_in'])
    silent = tk.BooleanVar(master, bool(cf[plate]['silent']))
    video_delay = tk.DoubleVar(master, float(cf[plate]['video_delay']))

    # Name row 0
    if platform.system() == 'Darwin':
        folder_button = tktt.TTButton(master, text=destination_folder.get(), command=enter_destination_folder,
                                      fg="blue", bg=bg_color)
        title_button = tktt.TTButton(master, text=title.get(), command=enter_title,
                                     fg="blue", bg=bg_color)
    else:
        destination_folder_button = tk.Button(master, text=destination_folder.get(), command=enter_destination_folder,
                                  fg="blue", bg=bg_color)
        title_button = tk.Button(master, text=title.get(), command=enter_title,
                                  fg="blue", bg=bg_color)
    destination_folder_button.grid(row=0, column=0, pady=2, sticky=tk.N)
    title_button.grid(row=0, column=1, pady=2, sticky=tk.N)
    tk.Label(master, text=".mkv", fg="blue").grid(row=0, column=2, sticky=tk.N, pady=2)
    silent_button = tk.Checkbutton(master, text='silent', bg=bg_color, variable=silent,
                                   onvalue=True, offvalue=False)
    silent_button.grid(row=0, column=3, pady=2, sticky=tk.N)

    # Recording length row 1
    tk.Label(master, text="Recording length, seconds:").grid(row=1, column=0, pady=2)
    time_button = tk.Button(master, text=rec_time.get(), command=enter_rec_time, fg="green", bg=bg_color)
    time_button.grid(row=1, column=1, pady=2)

    # Quality row 2
    tk.Label(master, text="crf quality for ffmpeg:").grid(row=2, column=0, pady=2)
    crf_button = tk.Button(master, text=crf.get(), command=enter_crf, fg="green", bg=bg_color)
    crf_button.grid(row=2, column=1, pady=2)

    # Video row 3
    tk.Label(master, text="Video").grid(row=3, column=0, pady=2)
    video_grabber_button = tk.Button(master, text=video_grabber.get(), command=enter_video_grabber, fg="purple", bg=bg_color)
    video_grabber_button.grid(row=3, column=1, pady=2)
    video_in_button = tk.Button(master, text=video_in.get(), command=enter_video_in, fg="purple", bg=bg_color)
    video_in_button.grid(row=3, column=3, pady=2)

    # Audio row 4
    tk.Label(master, text="Audio").grid(row=4, column=0, pady=2)
    audio_grabber_button = tk.Button(master, text=audio_grabber.get(), command=enter_audio_grabber, fg="purple", bg=bg_color)
    audio_grabber_button.grid(row=4, column=1, pady=2)
    audio_in_button = tk.Button(master, text=audio_in.get(), command=enter_audio_in, fg="purple", bg=bg_color)
    audio_in_button.grid(row=4, column=3, pady=2)

    # Image row 5
    pic_path = os.path.join(script_loc, 'screencast.png')
    picture = tk.PhotoImage(file=pic_path).subsample(5, 5)
    label = tk.Label(master, image=picture)
    label.grid(row=5, column=3, columnspan=2, rowspan=3, padx=5, pady=5)

    ev1_label = tk.Label(master, text='', wraplength=wrap_length, justify=tk.LEFT)
    ev1_label.grid(sticky="W", row=6, column=1, columnspan=4, padx=5, pady=5)

    ev2_label = tk.Label(master, text='', wraplength=wrap_length, justify=tk.LEFT)
    ev2_label.grid(sticky="W", row=7, column=1, columnspan=4, padx=5, pady=5)

    ev3_label = tk.Label(master, text='', wraplength=wrap_length, justify=tk.LEFT)
    ev3_label.grid(sticky="W", row=8, column=1, columnspan=4, padx=5, pady=5)

    ev4_label = tk.Label(master, text='', wraplength=wrap_length, justify=tk.LEFT)
    ev4_label.grid(sticky="W", row=9, column=1, columnspan=4, padx=5, pady=5)

    tk.ttk.Separator(master, orient='horizontal').grid(row=10, columnspan=5, pady=5, sticky='ew')

    # Action row 11
    tk.Label(master, text="Action").grid(row=11, column=0, pady=2)
    record_label = tk.Label(master, text='Action:')
    record_label.grid(row=11, column=0, padx=5, pady=5)
    record_button = tk.Button(master, text='RECORD', command=record, fg="red", bg=bg_color, wraplength=wrap_length, justify=tk.LEFT)
    record_button.grid(sticky="W", row=11, column=1, padx=5, pady=5)

    # Begin
    # option_handler()
    master.mainloop()
