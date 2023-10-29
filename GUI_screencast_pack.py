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
from tkinter import filedialog
import tkinter.simpledialog
from screencast import screencast, delay_audio_sync, delay_video_sync, cut_short, length
import tkinter.messagebox
import pyperclip
from datetime import timedelta
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


# Executive class to control the global variables
class Global:
    def __init__(self, owner):
        self.sync_tuner_butt = tk.Button(owner)
        self.sync_short_tuner_butt = tk.Button(owner)
        self.video_delay_tuner_butt = tk.Button(owner)
        self.intermediate_file = tk.Label(owner)
        self.short_file_path_label = tk.Label(owner)
        self.start_short_butt = tk.Button(owner)
        self.stop_short_butt = tk.Button(owner)
        self.short_cut_butt = tk.Button(owner)


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


def enter_audio_grab():
    audio_grab.set(tk.simpledialog.askstring(title=__file__, prompt="ffmpeg audio_grab parameter", initialvalue=audio_grab.get()))
    cf[SYS]['audio_grab'] = audio_grab.get()
    cf.save_to_file()
    audio_grab_butt.config(text=audio_grab.get())


def enter_audio_in():
    audio_in.set(tk.simpledialog.askstring(title=__file__, prompt="ffmpeg audio_in parameter", initialvalue=audio_in.get()))
    cf[SYS]['audio_in'] = audio_in.get()
    cf.save_to_file()
    audio_in_butt.config(text=audio_in.get())


def enter_crf():
    crf.set(tk.simpledialog.askinteger(title=__file__, prompt="enter ffmpeg crf, lower is larger file", initialvalue=crf.get()))
    cf[SYS]['crf'] = str(crf.get())
    cf.save_to_file()
    crf_butt.config(text=crf.get())


def enter_folder(folder_='', init=False):
    folder.set(folder_)
    if folder_ == '' and not init:
        folder.set(tk.filedialog.askdirectory(title="Select a Recordings Folder", initialdir=folder.get()))
    if folder.get() == '' or folder.get() == '<enter destination folder>':
        folder.set('<enter destination folder>')
        folder_butt.config(bg='pink')
    else:
        folder_butt.config(bg=bg_color)
    cf[SYS]['folder'] = folder.get()
    cf.save_to_file()
    folder_butt.config(text=folder.get())
    out_path.set(os.path.join(folder.get(), title.get() + '.mkv'))
    short_out_path.set(os.path.join(folder.get(), 'short_' + title.get() + '.mkv'))


def enter_rec_time():
    rec_time.set(tk.simpledialog.askfloat(title=__file__, prompt="enter record time, minutes", initialvalue=rec_time.get()))
    cf[SYS]['rec_time'] = str(rec_time.get())
    cf.save_to_file()
    time_butt.config(text=rec_time.get())


def enter_start_short_time():
    start_short.set(tk.simpledialog.askfloat(title=__file__, prompt="enter clip start, minutes", initialvalue=start_short.get()))
    tuners.start_short_butt.config(text=start_short.get())


def enter_stop_short_time():
    stop_short.set(tk.simpledialog.askfloat(title=__file__, prompt="enter clip stop, minutes", initialvalue=stop_short.get()))
    tuners.stop_short_butt.config(text=stop_short.get())


def enter_title(title_='', init=False):
    title.set(title_)
    if title_ == '' and not init:
        title.set(tk.simpledialog.askstring(title=__file__, prompt="enter title", initialvalue=title.get()))
    if title.get() == '' or title.get() == '<enter title>':
        title.set('<enter title>')
        title_butt.config(bg='pink')
    else:
        title_butt.config(bg=bg_color)
    cf[SYS]['title'] = title.get()
    cf.save_to_file()
    title_butt.config(text=title.get())
    out_path.set(os.path.join(folder.get(), title.get() + '.mkv'))
    short_out_path.set(os.path.join(folder.get(), 'short_' + title.get() + '.mkv'))


def enter_video_delay():
    video_delay.set(float(tk.simpledialog.askfloat(title=__file__, prompt="enter seconds video delay audio +/-", initialvalue=video_delay.get())))
    cf[SYS]['video_delay'] = str(video_delay.get())
    cf.save_to_file()
    video_delay_butt.config(text=str(video_delay.get()))
    video_delay_butt.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='purple')
    tuners.video_delay_tuner_butt.config(text=str(video_delay.get()))
    tuners.sync_tuner_butt.config(bg=bg_color, activebackground=bg_color, fg='black', activeforeground='purple')


def enter_video_grab():
    video_grab.set(tk.simpledialog.askstring(title=__file__, prompt="ffmpeg video_grab parameter", initialvalue=video_grab.get()))
    cf[SYS]['video_grab'] = video_grab.get()
    cf.save_to_file()
    video_grab_butt.config(text=video_grab.get())


def enter_video_in():
    video_in.set(tk.simpledialog.askstring(title=__file__, prompt="ffmpeg video_in parameter", initialvalue=video_in.get()))
    cf[SYS]['video_in'] = video_in.get()
    cf.save_to_file()
    video_in_butt.config(text=video_in.get())


def folder_path_handler(*args):
    print(f"folder_path_handler")
    if os.path.isfile(out_path.get()) and os.path.getsize(out_path.get()) > 0:  # bytes
        confirmation = tk.messagebox.askyesno('query overwrite', 'File exists:  overwrite later?')
        if confirmation is False:
            print('enter different folder or title first row')
            tkinter.messagebox.showwarning(message='enter different folder or title first row')
            overwriting.set(False)
            folder_butt.config(bg=bg_color)
            title_butt.config(bg=bg_color)
        else:
            overwriting.set(True)
            folder_butt.config(bg='yellow')
            title_butt.config(bg='yellow')
    cf.save_to_file()
    record_time = length(raw_file_path.get(), silent=silent.get())
    if record_time is not None:
        rec_time.set(record_time / 60.)
    else:
        rec_time.set(0.)
    hms = "hms=" + str(timedelta(minutes=rec_time.get()))
    hms_label.config(text=hms)


# Tuner window
def open_tuner_window():
    tuner_window = tk.Toplevel(root, bg=bg_color)
    tuner_window.title("Tuner")
    # tuner_window.geometry("700x200")

    # Video delay row
    video_delay_tuner_frame = tk.Frame(tuner_window, bg=box_color, bd=4, relief=relief)
    video_delay_tuner_frame.pack(side=tk.TOP)
    vd_label = tk.Label(video_delay_tuner_frame, text="Video delay +/-", bg=bg_color)
    tuners.video_delay_tuner_butt = tk.Button(video_delay_tuner_frame, text=video_delay.get(), command=enter_video_delay, fg="purple", bg=bg_color)
    vd_label.pack(side="left", fill='x')
    tuners.video_delay_tuner_butt.pack(side="left", fill='x')

    # Shortcut row
    shortcut_frame = tk.Frame(tuner_window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    shortcut_frame.pack(side=tk.TOP)
    shortcut_label = tk.Label(shortcut_frame, text="Cut range, minutes:", bg=bg_color)
    tuners.start_short_butt = tk.Button(shortcut_frame, text=start_short.get(), command=enter_start_short_time, fg="green", bg=bg_color)
    tuners.stop_short_butt = tk.Button(shortcut_frame, text=stop_short.get(), command=enter_stop_short_time, fg="green", bg=bg_color)
    shortcut_label.pack(side="left", fill='x')
    tuners.start_short_butt.pack(side="left", fill='x')
    tuners.stop_short_butt.pack(side="left", fill='x')

    # Cut short
    cut_short_frame = tk.Frame(tuner_window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    cut_short_frame.pack(side=tk.TOP)
    tuners.short_cut_butt = tk.Button(cut_short_frame, text="CUT IT OUT", command=short_cut, bg='lightyellow', fg='black')
    cut_short_label = tk.Label(cut_short_frame, text="Short file=", bg=bg_color)
    tuners.short_file_path_label = tk.Label(cut_short_frame, text=short_file_path.get(), wraplength=wrap_length, justify=tk.RIGHT)
    tuners.short_file_path_label.config(bg=bg_color)
    tuners.short_cut_butt.pack(side="left", fill='x')
    cut_short_label.pack(side="left", fill='x')
    tuners.short_file_path_label.pack(side="left", fill='x')

    # Sync short
    sync_short_frame = tk.Frame(tuner_window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    sync_short_frame.pack(side=tk.TOP)
    tuners.sync_short_tuner_butt = tk.Button(sync_short_frame, text="  SYNC SHORT  ", command=short_cut, bg='lightyellow', fg='black')
    sync_short_label = tk.Label(sync_short_frame, text="sync short=", bg=bg_color)
    tuners.short_out_file_path_label = tk.Label(sync_short_frame, text=short_out_path.get(), wraplength=wrap_length, justify=tk.RIGHT)
    tuners.short_out_file_path_label.config(bg=bg_color)
    tuners.sync_short_tuner_butt.pack(side="left", fill='x')
    sync_short_label.pack(side="left", fill='x')
    tuners.short_out_file_path_label.pack(side="left", fill='x')

    # Sync main
    sync_frame = tk.Frame(tuner_window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    sync_frame.pack(side=tk.TOP)
    tuners.sync_tuner_butt = tk.Button(sync_frame, text="***  SYNC    ***", command=short_cut, bg='red', fg='white')
    sync_label = tk.Label(sync_frame, text="sync =", bg=bg_color)
    tuners.out_file_path_label = tk.Label(sync_frame, text=out_path.get(), wraplength=wrap_length, justify=tk.RIGHT)
    tuners.out_file_path_label.config(bg=bg_color)
    tuners.sync_tuner_butt.pack(side="left", fill='x')
    sync_label.pack(side="left", fill='x')
    tuners.out_file_path_label.pack(side="left", fill='x')

    # Instructions
    tuner_doc_frame = tk.Frame(tuner_window, width=250, height=100, bg=bg_color, bd=4, relief=relief)
    tuner_doc_frame.pack(side=tk.TOP)
    tuner_doc = """Tune for video / audio sync.\n\
    - Set range to be within the length of original video.\n\
    - Press 'CUT IT OUT'.\n\
    - Go to file explorer and verify sync.   Adjust 'Video delay +/-' as necessary."""
    tuner_doc = tk.Label(tuner_doc_frame, text=tuner_doc, fg="black", justify='left', bg=bg_color)
    tuner_doc.pack(side="left", fill='x')

    short_file_path_handler()
    short_file_path.trace_add('write', short_file_path_handler)


def record():
    if title.get() == '<enter title>' or title.get() == '' or title.get() == 'None':
        enter_title()
    if title.get() != '<enter title>' and title.get() != '' and title.get() != 'None':
        rf, rr = screencast(silent=silent.get(),
                            video_grabber=video_grab.get(), video_in=video_in.get(),
                            audio_grabber=audio_grab.get(), audio_in=audio_in.get(),
                            crf=crf.get(),
                            rec_time=rec_time.get()*60.,
                            output_file=raw_file_path.get())
        raw_file_path.set(rf)  # screencast may cause null filename if fails
        result_ready.set(rr)
        sync()
    else:
        print('aborting recording....need to enter title.  Presently = ', title.get())


def result_ready_handler(*args):
    print(f"folder_path_handler")
    if os.path.isfile(out_path.get()) and os.path.getsize(out_path.get()) > 0:  # bytes
        if result_ready.get():
            overwriting.set(False)
            folder_butt.config(bg='lightgreen')
            title_butt.config(bg='lightgreen')
            record_butt.config(bg='yellow', activebackground='yellow', fg='black', activeforeground='purple')
            record_time = length(raw_file_path.get(), silent=silent.get())
            if record_time is not None:
                rec_time.set(record_time / 60.)
            else:
                rec_time.set(0.)
            hms = "hms=" + str(timedelta(minutes=rec_time.get()))
            hms_label.config(text=hms)
        else:
            overwriting.set(True)
            folder_butt.config(bg=bg_color)
            title_butt.config(bg=bg_color)
            record_butt.config(bg='red', activebackground='red', fg='white', activeforeground='purple')


def short_cut():
    sf, rr = cut_short(silent=silent.get(), raw_file=raw_file_path.get(),
                       start_short=start_short.get()*60., stop_short=stop_short.get()*60.,
                       short_file=short_file_path.get())
    if rr:
        tuners.short_file_path_label.config(bg='lightgreen', fg='black')
        tuners.short_cut_butt.config(bg='yellow', fg='black')
    else:
        tuners.short_file_path_label.config(bg=bg_color, fg='black')
        tuners.short_cut_butt.config(bg='red', fg='black')


def short_file_path_handler(*args):
    print(f"short_file_path_handler")
    if os.path.isfile(out_path.get()) and os.path.getsize(out_path.get()) > 0:  # bytes
        tuners.short_file_path_label.config(bg=bg_color)
    else:
        tuners.short_file_path_label.config(bg='yellow')


def silent_handler(*args):
    cf[SYS]['silent'] = str(silent.get())
    cf.save_to_file()


def sync():
    if result_ready.get():
        if video_delay.get() >= 0.0:
            delay_video_sync(silent=silent.get(), delay=video_delay.get(), input_file=raw_file_path.get(),
                             output_file=os.path.join(os.getcwd(), out_path.get()))
        else:
            delay_audio_sync(silent=silent.get(), delay=-video_delay.get(), input_file=raw_file_path.get(),
                             output_file=os.path.join(os.getcwd(), out_path.get()))
        tuners.sync_tuner_butt.config(bg='lightgreen', activebackground='lightgreen', fg='red', activeforeground='purple')
    else:
        print("record first *******")


def sync_short():
    if result_ready.get():
        if video_delay.get() >= 0.0:
            delay_video_sync(silent=silent.get(), delay=video_delay.get(), input_file=short_file_path.get(),
                             output_file=os.path.join(os.getcwd(), short_out_path.get()))
        else:
            delay_audio_sync(silent=silent.get(), delay=-video_delay.get(), input_file=short_file_path.get(),
                             output_file=os.path.join(os.getcwd(), short_out_path.get()))
        tuners.sync_short_tuner_butt.config(bg='lightgreen', activebackground='lightgreen', fg='red', activeforeground='purple')
    else:
        print("record first *******")


if __name__ == '__main__':
    import os
    import tkinter as tk
    SYS = platform.system()

    # Configuration for entire folder selection read with filepaths
    def_dict = {
                'Linux':   {"folder": '<enter destination folder>',
                            "title":  '<enter title>',
                            "rec_time": '0.1',
                            "crf": '25',
                            "video_grab": 'x11grab',
                            "video_in": ':0.0+0.0',
                            "audio_grab": 'pulse',
                            "audio_in": 'default',
                            "silent": '1',
                            "video_delay": '0.0',
                            "overwriting": '0'},
                'Windows': {"folder": '<enter destination folder>',
                            "title": '<enter title>',
                            "rec_time": '0.1',
                            "crf": '28',
                            "video_grab": "gdigrab",
                            "video_in": 'desktop',
                            "audio_grab": 'dshow',
                            "audio_in": 'audio="CABLE Output (VB-Audio Virtual Cable)"',
                            "silent": '1',
                            "video_delay": '0.0',
                            "overwriting": '0'},
                'Darwin':  {"folder": '<enter destination folder>',
                            "title":  '<enter title>',
                            "rec_time": '0.1',
                            "crf": '25',
                            "video_grab": 'avfoundation',
                            "video_in": '1',
                            "audio_grab": '',
                            "audio_in": '2',
                            "silent": '1',
                            "video_delay": '0.0',
                            "overwriting": '0'},
                }
    cf = Begini(__file__, def_dict)
    doc = ''
    if SYS == 'Linux':
        doc = """Screencast (Linux):  RECORD while a video is playing full screen.\n \
    - Get yourself ready to run the system entirely on one display (unplug the other).\n \
    - Open the streaming source and have it all queued to begin, all except for 'fullscreen.'\n\
    - Press 'RECORD' then go to the video streaming source and make it full screen.\n\
    - To tune the video sync delay play the resulting file and determine if the video needs to be delayed (+delay)\n\
      or advanced (-delay).  Tune the 'Video delay' until happy.   For convenience you may use the 'Tuner' window\n\
      to extract a 10 - 20 second video from the final to iterate quickly.\n\
    - The unsynchronized 'intermediate' result is saved to make this easy.\n\
    - The 'crf' value is used to set video compression.  Smaller is larger file size.\n\
    - Framerate is whatever the source is.  This is a common practice in screencast recording.\n\
      Framerate is hard-coded.\n\
    - When complete, copy or move the named file from the folder listed at the top left of the GUI to your library.\n\
      That is done outside this program."""
    elif SYS == 'Windows':
        doc = """Screencast (Windows):  RECORD while a video is playing full screen.\n \
    - Get yourself ready to run the system entirely on one display (unplug the other).\n \
    - Open the audio settings and point at 'VB-Audio Virtual Cable' or install it as needed.\n\
    - Open the streaming source and have it all queued to begin, all except for 'fullscreen.'\n\
    - Press 'RECORD' then go to the video streaming source and make it full screen.\n\
    - To tune the video sync delay play the resulting file and determine if the video needs to be delayed (+delay)\n\
      or advanced (-delay).  Tune the 'Video delay' until happy.   For convenience you may use the 'Tuner' window\n\
      to extract a 10 - 20 second video from the final to iterate quickly.\n\
    - The unsynchronized 'intermediate' result is saved to make this easy.\n\
    - The 'crf' value is used to set video compression.  Smaller is larger file size.\n\
    - Framerate is whatever the source is.  This is a common practice in screencast recording.\n\
      Framerate is hard-coded.\n\
    - When complete, copy or move the named file from the folder listed at the top left of the GUI to your library.\n\
      That is done outside this program."""
    elif SYS == 'Darwin':
        doc = """Screencast (MacOS):  RECORD while a video is playing on Opera.\n \
    - The MacOS version has choppy continuity and stutters (cause TBD).
    - Get yourself ready to run the system entirely on one display (unplug the other).\n \
    - Open the audio settings and point at 'VB-Audio Virtual Cable' or install it as needed.\n\
    - Open the streaming source using the Opera browser and have it all queued to begin.\n\
    - Press 'RECORD' then go to the video streaming source and make Opera full screen (NOT the streaming source).\n\
    - To tune the video sync delay play the resulting file and determine if the video needs to be delayed (+delay)\n\
      or advanced (-delay).  Tune the 'Video delay' until happy.   For convenience you may use the 'Tuner' window\n\
      to extract a 10 - 20 second video from the final to iterate quickly.\n\
    - The unsynchronized 'intermediate' result is saved to make this easy.\n\
    - The 'crf' value is used to set video compression.  Smaller is larger file size.\n\
    - Framerate is whatever the source is.  This is a common practice in screencast recording.\n\
      Framerate is hard-coded.\n\
    - When complete, copy or move the named file from the folder listed at the top left of the GUI to your library.\n\
      That is done outside this program."""
    else:
        print('os unknown')

    # Frame properties
    min_width = 800
    main_height = 500
    wrap_length = 800
    bg_color = "lightgray"
    box_color = "lightgray"
    relief = tk.FLAT
    pad_x_frames = 1
    pad_y_frames = 2

    # Globals
    root = tk.Tk()
    root.title('Screencast')
    root.wm_minsize(width=min_width, height=main_height)
    tuners = Global(root)
    script_loc = os.path.dirname(os.path.abspath(__file__))
    cwd_path = tk.StringVar(root, os.getcwd())
    folder = tk.StringVar(root, cf[SYS]['folder'])
    root.iconphoto(False, tk.PhotoImage(file=os.path.join(script_loc, 'GUI_screencast_Icon.png')))
    title = tk.StringVar(root, cf[SYS]['title'])
    out_path = tk.StringVar(root, os.path.join(folder.get(), title.get()+'.mkv'))
    short_out_path = tk.StringVar(root, os.path.join(folder.get(), 'short_' + title.get() + '.mkv'))
    rec_time = tk.DoubleVar(root, float(cf[SYS]['rec_time']))
    crf = tk.IntVar(root, int(cf[SYS]['crf']))
    video_grab = tk.StringVar(root, cf[SYS]['video_grab'])
    video_in = tk.StringVar(root, cf[SYS]['video_in'])
    audio_grab = tk.StringVar(root, cf[SYS]['audio_grab'])
    audio_in = tk.StringVar(root, cf[SYS]['audio_in'])
    if cf[SYS]['silent'] == 'False':
        silent = tk.BooleanVar(root, False)
    else:
        silent = tk.BooleanVar(root, True)
    video_delay = tk.DoubleVar(root, float(cf[SYS]['video_delay']))
    if cf[SYS]['overwriting'] == 'False':
        overwriting = tk.BooleanVar(root, False)
    else:
        overwriting = tk.BooleanVar(root, True)
    print(f"after load {overwriting.get()}")
    raw_file_path = tk.StringVar(root, os.path.join(folder.get(), title.get()+'_unsync.mkv'))
    result_ready = tk.BooleanVar(root, os.path.isfile(out_path.get()) and os.path.getsize(out_path.get()))
    start_short = tk.DoubleVar(root, 0.0)
    stop_short = tk.DoubleVar(root, 0.0)
    short_file_path = tk.StringVar(root, os.path.join(folder.get(), title.get()+'_short.mkv'))
    row = -1

    # Root
    outer_frame = tk.Frame(root, bd=5, bg=bg_color)
    outer_frame.pack(fill='x')

    # Image row
    pic_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    pic_frame.pack()
    image = tk.Frame(pic_frame, borderwidth=2, bg=box_color)
    image.pack(side=tk.LEFT, fill="x")
    pic_path = os.path.join(script_loc, 'screencast.png')
    image.picture = tk.PhotoImage(file=pic_path).subsample(5, 5)
    image.label = tk.Label(image, image=image.picture)
    image.label.pack(side="left", fill='x')
    doc_block = tk.Label(pic_frame, text=doc, fg="black", justify='left', bg=bg_color)
    doc_block.pack(side="right", fill='x')

    # Name row
    name_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    name_frame.pack(fill='x')
    folder_butt = None
    title_butt = None
    if SYS == 'Darwin':
        folder_butt = tktt.TTButton(name_frame, text=folder.get(), command=enter_folder, fg="blue", bg=bg_color)
        slash = tk.Label(name_frame, text="/", fg="blue", bg=bg_color)
        title_butt = tktt.TTButton(name_frame, text=title.get(), command=enter_title, fg="blue", bg=bg_color)
    else:
        folder_butt = tk.Button(name_frame, text=folder.get(), command=enter_folder, fg="blue", bg=bg_color)
        slash = tk.Label(name_frame, text="/", fg="blue", bg=bg_color)
        title_butt = tk.Button(name_frame, text=title.get(), command=enter_title, fg="blue", bg=bg_color)
    enter_folder(cf[SYS]['folder'], True)
    enter_title(cf[SYS]['title'], True)
    folder_butt.pack(side="left", fill='x')
    slash.pack(side="left", fill='x')
    title_butt.pack(side="left", fill='x')

    # Recording length row
    length_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    length_frame.pack(fill='x')
    rec_length = tk.Label(length_frame, text="Recording length, minutes:", bg=bg_color)
    time_butt = tk.Button(length_frame, text=rec_time.get(), command=enter_rec_time, fg="green", bg=bg_color)
    hms = "hms=" + str(timedelta(minutes=rec_time.get()))
    hms_label = tk.Label(length_frame, text=hms, wraplength=wrap_length, justify=tk.LEFT, bg=bg_color)
    rec_length.pack(side="left", fill='x')
    time_butt.pack(side="left", fill='x')
    hms_label.pack(side="left", fill='x')

    # Quality row
    quality_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    quality_frame.pack(fill='x')
    crf_label = tk.Label(quality_frame, text="crf quality for ffmpeg:", bg=bg_color)
    crf_butt = tk.Button(quality_frame, text=crf.get(), command=enter_crf, fg="green", bg=bg_color)
    crf_label.pack(side="left", fill='x')
    crf_butt.pack(side="left", fill='x')

    # Video delay row
    video_delay_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    video_delay_frame.pack(fill='x')
    video_delay_label = tk.Label(video_delay_frame, text="Video delay +/-", bg=bg_color)
    video_delay_butt = tk.Button(video_delay_frame, text=str(video_delay.get()), command=enter_video_delay, fg="purple", bg=bg_color)
    video_delay_label.pack(side="left", fill='x')
    video_delay_butt.pack(side="left", fill='x')

    # Video row
    video_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    video_frame.pack(fill='x')
    video_grab_label = tk.Label(video_frame, text="Video:", bg=bg_color)
    video_grab_butt = tk.Button(video_frame, text=video_grab.get(), command=enter_video_grab, fg="purple", bg=bg_color)
    video_in_butt = tk.Button(video_frame, text=video_in.get(), command=enter_video_in, fg="purple", bg=bg_color)
    video_grab_label.pack(side="left", fill='x')
    video_grab_butt.pack(side="left", fill='x')
    video_in_butt.pack(side="left", fill='x')

    # Audio row
    audio_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    audio_frame.pack(fill='x')
    audio_grab_label = tk.Label(audio_frame, text="Audio:", bg=bg_color)
    audio_grab_butt = tk.Button(audio_frame, text=audio_grab.get(), command=enter_audio_grab, fg="purple", bg=bg_color)
    audio_in_butt = tk.Button(audio_frame, text=audio_in.get(), command=enter_audio_in, fg="purple", bg=bg_color)
    audio_grab_label.pack(side="left", fill='x')
    audio_grab_butt.pack(side="left", fill='x')
    audio_in_butt.pack(side="left", fill='x')

    # Silent row
    silent_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    silent_frame.pack(fill='x')
    silent_butt = tk.Checkbutton(silent_frame, text='silent', bg=bg_color, variable=silent, onvalue=True, offvalue=False)
    silent_butt.pack(side="left", fill='x')

    # Action row
    action_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    action_frame.pack(fill='x')
    raw_file_path_label = tk.Label(action_frame, text=raw_file_path.get(), wraplength=wrap_length, justify=tk.RIGHT)
    raw_file_path_label.config(bg=bg_color)
    raw_file_path_label.pack(side="right", fill='x')
    action_label = tk.Label(action_frame, text="Intermediate=", bg=bg_color)
    action_label.pack(side="right", fill='x')

    # Record row
    record_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    record_frame.pack(fill='x')
    record_butt = tk.Button(record_frame, text='****    RECORD     ****', command=record, fg='white', bg='red', wraplength=wrap_length, justify=tk.CENTER)
    tuner_window_butt = tk.Button(record_frame, text="TUNER WINDOW", command=open_tuner_window, bg=bg_color)
    record_butt.pack(side="left", fill='x')
    tuner_window_butt.pack(side="right", fill='x')

    # Begin
    folder_path_handler()
    out_path.trace_add('write', folder_path_handler)
    silent_handler()
    silent.trace_add('write', silent_handler)
    result_ready_handler()
    result_ready.trace_add('write', result_ready_handler)
    root.mainloop()
