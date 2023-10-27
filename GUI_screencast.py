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
import tkinter.messagebox
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


def destination_path_handler(*args):
    print(f"destination_path_handler")
    if os.path.isfile(destination_path.get()) and os.path.getsize(destination_path.get()) > 0:  # bytes
        confirmation = tk.messagebox.askyesno('query overwrite', 'File exists:  overwrite later?')
        if confirmation is False:
            print('enter different folder or title first row')
            tkinter.messagebox.showwarning(message='enter different folder or title first row')
            overwriting.set(False)
            destination_folder_button.config(bg=bg_color)
            title_button.config(bg=bg_color)
        else:
            overwriting.set(True)
            destination_folder_button.config(bg='yellow')
            title_button.config(bg='yellow')
    cf.save_to_file()


def enter_audio_grabber():
    audio_grabber.set(tk.simpledialog.askstring(title=__file__, prompt="ffmpeg audio_grabber parameter"))
    cf[plate]['audio_grabber'] = audio_grabber.get()
    cf.save_to_file()
    audio_grabber_button.config(text=audio_grabber.get())


def enter_audio_in():
    audio_in.set(tk.simpledialog.askstring(title=__file__, prompt="ffmpeg audio_in parameter"))
    cf[plate]['audio_in'] = audio_in.get()
    cf.save_to_file()
    audio_in_button.config(text=audio_in.get())


def enter_crf():
    crf.set(tk.simpledialog.askinteger(title=__file__, prompt="enter ffmpeg crf, lower is larger file"))
    cf[plate]['crf'] = str(crf.get())
    cf.save_to_file()
    crf_button.config(text=crf.get())


def enter_destination_folder(folder_='', init=False):
    destination_folder.set(folder_)
    if folder_ == '' and not init:
        destination_folder.set(tk.filedialog.askdirectory(title="Select a Recordings Folder", initialdir=destination_folder.get()))
    if destination_folder.get() == '' or destination_folder.get() == '<enter destination folder>':
        destination_folder.set('<enter destination folder>')
        destination_folder_button.config(bg='pink')
    else:
        destination_folder_button.config(bg=bg_color)
    cf[plate]['destination_folder'] = destination_folder.get()
    cf.save_to_file()
    destination_folder_button.config(text=destination_folder.get())
    destination_path.set(os.path.join(destination_folder.get(), title.get()+'.mkv'))


def enter_rec_time():
    rec_time.set(tk.simpledialog.askfloat(title=__file__, prompt="enter record time, seconds"))
    cf[plate]['rec_time'] = str(rec_time.get())
    cf.save_to_file()
    time_button.config(text=rec_time.get())


def enter_title(title_='', init=False):
    title.set(title_)
    if title_ == '' and not init:
        title.set(tk.simpledialog.askstring(title=__file__, prompt="enter title"))
    if title.get() == '' or title.get() == '<enter title>':
        title.set('<enter title>')
        title_button.config(bg='pink')
    else:
        title_button.config(bg=bg_color)
    cf[plate]['title'] = title.get()
    cf.save_to_file()
    title_button.config(text=title.get())
    destination_path.set(os.path.join(destination_folder.get(), title.get()+'.mkv'))


def enter_video_delay():
    video_delay.set(float(tk.simpledialog.askstring(title=__file__, prompt="enter seconds video delay audio +/-")))
    cf[plate]['video_delay'] = str(video_delay.get())
    cf.save_to_file()
    video_delay_button.config(text=str(video_delay.get()))


def enter_video_grabber():
    video_grabber.set(tk.simpledialog.askstring(title=__file__, prompt="ffmpeg video_grabber parameter"))
    cf[plate]['video_grabber'] = video_grabber.get()
    cf.save_to_file()
    video_grabber_button.config(text=video_grabber.get())


def enter_video_in():
    video_in.set(tk.simpledialog.askstring(title=__file__, prompt="ffmpeg video_in parameter"))
    cf[plate]['video_in'] = video_in.get()
    cf.save_to_file()
    video_in_button.config(text=video_in.get())


def record():
    if title.get() == '<enter title>' or title.get() == '' or title.get() == 'None':
        enter_title()
    if title.get() != '<enter title>' and title.get() != '' and title.get() != 'None':
        rf, rr = screencast(silent=silent.get(),
                            video_grabber=video_grabber.get(), video_in=video_in.get(),
                            audio_grabber=audio_grabber.get(), audio_in=audio_in.get(),
                            crf=crf.get(),
                            rec_time=rec_time.get(),
                            output_file=raw_file.get())
        raw_file.set(rf)  # screencast may null filename if fails
        result_ready.set(rr)
        if result_ready.get():
            record_button.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='purple')
        sync()
        # if result_ready.get():
        #     if video_delay.get() >= 0.0:
        #         delay_video_sync(silent=silent.get(), delay=video_delay.get(), input_file=raw_file.get(),
        #                          output_file=os.path.join(os.getcwd(), destination_path.get()))
        #     else:
        #         delay_audio_sync(silent=silent.get(), delay=-video_delay.get(), input_file=raw_file.get(),
        #                          output_file=os.path.join(os.getcwd(), destination_path.get()))
    else:
        print('aborting print....need to enter title.  Presently = ', title.get())


def result_ready_handler(*args):
    print(f"destination_path_handler")
    if os.path.isfile(destination_path.get()) and os.path.getsize(destination_path.get()) > 0:  # bytes
        if result_ready.get():
            overwriting.set(False)
            destination_folder_button.config(bg='green')
            title_button.config(bg='green')
            record_button.config(bg=bg_color, activebackground='green', fg='black', activeforeground='purple')
            sync_button.config(bg=bg_color, activebackground=bg_color, fg='red', activeforeground='purple')
        else:
            overwriting.set(True)
            destination_folder_button.config(bg=bg_color)
            title_button.config(bg=bg_color)
            record_button.config(bg=bg_color, activebackground=bg_color, fg='red', activeforeground='purple')
            sync_button.config(bg=bg_color, activebackground=bg_color, fg='red', activeforeground='purple')


def silent_handler(*args):
    cf[plate]['silent'] = str(silent.get())
    cf.save_to_file()


def sync():
    if result_ready.get():
        if video_delay.get() >= 0.0:
            delay_video_sync(silent=silent.get(), delay=video_delay.get(), input_file=raw_file.get(),
                             output_file=os.path.join(os.getcwd(), destination_path.get()))
        else:
            delay_audio_sync(silent=silent.get(), delay=-video_delay.get(), input_file=raw_file.get(),
                             output_file=os.path.join(os.getcwd(), destination_path.get()))
            sync_button.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='purple')
    else:
        print("record first *******")


if __name__ == '__main__':
    import os
    import tkinter as tk
    from tkinter import ttk

    # Configuration for entire folder selection read with filepaths
    def_dict = {
                'Linux':   {"destination_folder": '<enter destination folder>',
                            "title":  '<enter title>',
                            "rec_time": '6.',
                            "crf": '25',
                            "video_grabber": 'x11grab',
                            "video_in": ':0.0+0.0',
                            "audio_grabber": 'pulse',
                            "audio_in": 'default',
                            "silent": '1',
                            "video_delay": '0.0',
                            "overwriting": '0'},
                'Windows': {"destination_folder": '<enter destination folder>',
                            "title": '<enter title>',
                            "rec_time": '6.',
                            "crf": '28',
                            "video_grabber": "gdigrab",
                            "video_in": 'desktop',
                            "audio_grabber": 'dshow',
                            "audio_in": 'audio="CABLE Output (VB-Audio Virtual Cable)"',
                            "silent": '1',
                            "video_delay": '0.0',
                            "overwriting": '0'},
                'Darwin':  {"destination_folder": '<enter destination folder>',
                            "title":  '<enter title>',
                            "rec_time": '6.',
                            "crf": '25',
                            "video_grabber": 'avfoundation',
                            "video_in": '1',
                            "audio_grabber": '',
                            "audio_in": '2',
                            "silent": '1',
                            "video_delay": '0.0',
                            "overwriting": '0'},
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
    destination_folder = tk.StringVar(master, cf[plate]['destination_folder'])
    master.iconphoto(False, tk.PhotoImage(file=os.path.join(script_loc, 'GUI_screencast_Icon.png')))
    title = tk.StringVar(master, cf[plate]['title'])
    destination_path = tk.StringVar(master, os.path.join(destination_folder.get(), title.get()+'.mkv'))
    rec_time = tk.DoubleVar(master, float(cf[plate]['rec_time']))
    crf = tk.IntVar(master, int(cf[plate]['crf']))
    video_grabber = tk.StringVar(master, cf[plate]['video_grabber'])
    video_in = tk.StringVar(master, cf[plate]['video_in'])
    audio_grabber = tk.StringVar(master, cf[plate]['audio_grabber'])
    audio_in = tk.StringVar(master, cf[plate]['audio_in'])
    if cf[plate]['silent'] == 'False':
        silent = tk.BooleanVar(master, False)
    else:
        silent = tk.BooleanVar(master, True)
    video_delay = tk.DoubleVar(master, float(cf[plate]['video_delay']))
    if cf[plate]['overwriting'] == 'False':
        overwriting = tk.BooleanVar(master, False)
    else:
        overwriting = tk.BooleanVar(master, True)
    print(f"after load {overwriting.get()}")
    raw_file = tk.StringVar(master, os.path.join(os.getcwd(), 'screencast.mkv'))
    result_ready = tk.BooleanVar(master, os.path.isfile(destination_path.get()) and os.path.getsize(destination_path.get()))
    row = 0

    for i in range(1):
        row += i
        blank = tk.Label(master, text='', wraplength=wrap_length, justify=tk.LEFT)
        blank.grid(sticky="W", row=row, column=1, columnspan=4, padx=5, pady=5)

    # Name row
    row += 1
    destination_folder_button = None
    title_button = None
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

    enter_destination_folder(cf[plate]['destination_folder'], True)
    enter_title(cf[plate]['title'], True)
    destination_folder_button.grid(row=row, column=0, pady=2, sticky=tk.N)
    tk.Label(master, text="/", fg="blue").grid(row=row, column=1, sticky=tk.W, pady=2)
    title_button.grid(row=row, column=2, pady=2, sticky=tk.W)
    tk.Label(master, text=".mkv", fg="blue").grid(row=row, column=3, sticky=tk.W, pady=2)
    silent_button = tk.Checkbutton(master, text='silent', bg=bg_color, variable=silent, onvalue=True, offvalue=False)
    silent_button.grid(row=row, column=4, pady=2, sticky=tk.E)

    # Recording length row
    row += 1
    tk.Label(master, text="Recording length, seconds:").grid(row=row, column=0, pady=2, sticky=tk.E)
    time_button = tk.Button(master, text=rec_time.get(), command=enter_rec_time, fg="green", bg=bg_color)
    time_button.grid(row=row, column=2, pady=2, sticky=tk.W)

    # Quality row
    row += 1
    tk.Label(master, text="crf quality for ffmpeg:").grid(row=row, column=0, pady=2, sticky=tk.E)
    crf_button = tk.Button(master, text=crf.get(), command=enter_crf, fg="green", bg=bg_color)
    crf_button.grid(row=row, column=2, pady=2, sticky=tk.W)

    # Video row
    row += 1
    tk.Label(master, text="Video:").grid(row=row, column=0, pady=2, sticky=tk.E)
    video_grabber_button = tk.Button(master, text=video_grabber.get(), command=enter_video_grabber, fg="purple", bg=bg_color)
    video_grabber_button.grid(row=row, column=2, pady=2, sticky=tk.W)
    video_in_button = tk.Button(master, text=video_in.get(), command=enter_video_in, fg="purple", bg=bg_color)
    video_in_button.grid(row=row, column=3, pady=2, sticky=tk.W)

    # Audio row
    row += 1
    tk.Label(master, text="Audio:").grid(row=row, column=0, pady=2, sticky=tk.E)
    audio_grabber_button = tk.Button(master, text=audio_grabber.get(), command=enter_audio_grabber, fg="purple", bg=bg_color)
    audio_grabber_button.grid(row=row, column=2, pady=2, sticky=tk.W)
    audio_in_button = tk.Button(master, text=audio_in.get(), command=enter_audio_in, fg="purple", bg=bg_color)
    audio_in_button.grid(row=row, column=3, pady=2, sticky=tk.W)

    # Video delay row
    row += 1
    tk.Label(master, text="Video delay +/-").grid(row=row, column=0, pady=2, sticky=tk.E)
    video_delay_button = tk.Button(master, text=video_delay.get(), command=enter_video_delay, fg="purple", bg=bg_color)
    video_delay_button.grid(row=row, column=2, pady=2, sticky=tk.W)

    # Image row
    row += 1
    pic_path = os.path.join(script_loc, 'screencast.png')
    picture = tk.PhotoImage(file=pic_path).subsample(5, 5)
    label = tk.Label(master, image=picture)
    label.grid(row=row, column=2, columnspan=2, rowspan=3, padx=5, pady=5)

    for i in range(4):
        row += i
        blank = tk.Label(master, text='', wraplength=wrap_length, justify=tk.LEFT)
        blank.grid(sticky="W", row=row, column=1, columnspan=4, padx=5, pady=5)
        
    row += 1
    tk.ttk.Separator(master, orient='horizontal').grid(row=row, columnspan=5, pady=5, sticky='ew')

    # Action row
    row += 1
    record_button = tk.Button(master, text='RECORD', command=record, fg="red", bg=bg_color, wraplength=wrap_length, justify=tk.LEFT)
    record_button.grid(sticky="W", row=row, column=0, padx=5, pady=5)
    sync_label = tk.Label(master, text='Sync Only:')
    sync_label.grid(row=row, column=2, padx=5, pady=5, sticky=tk.E)
    sync_button = tk.Button(master, text='REPEAT SYNC', command=sync, fg="red", bg=bg_color, wraplength=wrap_length, justify=tk.LEFT)
    sync_button.grid(row=row, column=3, padx=5, pady=5, sticky=tk.W)

    print(f"after init before handler")

    # Begin
    destination_path_handler()
    destination_path.trace_add('write', destination_path_handler)
    silent_handler()
    silent.trace_add('write', silent_handler)
    result_ready_handler()
    result_ready.trace_add('write', result_ready_handler)
    master.mainloop()
