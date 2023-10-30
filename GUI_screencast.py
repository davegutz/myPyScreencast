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
    from ttwidgets import TTButton as myButton
else:
    import tkinter as tk
    from tkinter import Button as myButton
from tkinter import filedialog
import tkinter.simpledialog
from screencast import screencast, delay_audio_sync, delay_video_sync, cut_clip, length
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
        self.config_path = os.path.join(config_path, config_txt)
        print('config file', self.config_path)
        if os.path.isfile(self.config_path):
            self.read(self.config_path)
        else:
            with open(self.config_path, 'w') as cfg_file:
                self.read_dict(def_dict_)
                self.write(cfg_file)
            print('wrote', self.config_path)

    # Get an item
    def get_item(self, ind, item):
        return self[ind][item]

    # Put an item
    def put_item(self, ind, item, value):
        self[ind][item] = value
        self.save_to_file()

    # Save again
    def save_to_file(self):
        with open(self.config_path, 'w') as cfg_file:
            self.write(cfg_file)
        print('wrote', self.config_path)


# Executive class to control the global variables
class Global:
    def __init__(self, owner):
        self.sync_tuner_butt = myButton(owner)
        self.sync_clip_tuner_butt = myButton(owner)
        self.video_delay_tuner_butt = myButton(owner)
        self.hms_label = tk.Label(owner)
        self.intermediate_file = tk.Label(owner)
        self.raw_path_label = tk.Label(owner)
        self.clip_path_label = tk.Label(owner)
        self.start_clip_butt = myButton(owner)
        self.stop_clip_butt = myButton(owner)
        self.clip_cut_butt = myButton(owner)


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
    out_file.set(title.get()+'.mkv')
    out_path.set(os.path.join(folder.get(), out_file.get()))
    clip_file.set('clip_' + title.get() + '.mkv')
    clip_path.set(os.path.join(folder.get(), clip_file.get()))


def enter_rec_time():
    rec_time.set(tk.simpledialog.askfloat(title=__file__, prompt="enter record time, minutes", initialvalue=rec_time.get()))
    cf[SYS]['rec_time'] = str(rec_time.get())
    cf.save_to_file()
    time_butt.config(text=rec_time.get())


def enter_start_clip_time():
    start_clip.set(tk.simpledialog.askfloat(title=__file__, prompt="enter clip start, minutes", initialvalue=start_clip.get()))
    tuners.start_clip_butt.config(text=start_clip.get())


def enter_stop_clip_time():
    stop_clip.set(tk.simpledialog.askfloat(title=__file__, prompt="enter clip stop, minutes", initialvalue=stop_clip.get()))
    tuners.stop_clip_butt.config(text=stop_clip.get())


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
    raw_path.set(os.path.join(folder.get(), title.get() + '_unsync.mkv'))
    out_file.set(title.get()+'.mkv')
    out_path.set(os.path.join(folder.get(), out_file.get()))
    clip_file.set('clip_' + title.get() + '.mkv')
    clip_path.set(os.path.join(folder.get(), clip_file.get()))


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


def handle_folder_path(*args):
    print(f"handle_folder_path {out_path.get()=}")
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
    record_time = length(raw_path.get(), silent=silent.get())
    if record_time is not None:
        raw_time.set(record_time / 60.)
    else:
        raw_time.set(0.)
    hms.set("hms=" + str(timedelta(minutes=raw_time.get())))
    hms_label.config(text=hms.get())
    tuners.hms_label.config(text=hms.get())


def handle_raw_path(*args):
    print(f"handle_raw_path: {raw_path.get()=}")
    if os.path.isfile(raw_path.get()) and os.path.getsize(raw_path.get()) > 0:  # bytes
        print("coloring green")
        tuners.raw_path_label.config(text=raw_path.get(), bg='lightgreen', fg='black')
    else:
        print("coloring plain")
        tuners.raw_path_label.config(text=raw_path.get(), bg=bg_color, fg='black')


def handle_result_ready(*args):
    print(f"handle_folder_path {out_path.get()=}")
    if os.path.isfile(out_path.get()) and os.path.getsize(out_path.get()) > 0:  # bytes
        if result_ready.get():
            overwriting.set(False)
            folder_butt.config(bg='lightgreen')
            title_butt.config(bg='lightgreen')
            record_butt.config(bg='yellow', activebackground='yellow', fg='black', activeforeground='purple')
            record_time = length(raw_path.get(), silent=silent.get())
            if record_time is not None:
                raw_time.set(record_time / 60.)
            else:
                raw_time.set(0.)
            hms.set("hms=" + str(timedelta(minutes=raw_time.get())))
            hms_label.config(text=hms.get())
            tuners.hms_label.config(text=hms.get())
        else:
            overwriting.set(True)
            folder_butt.config(bg=bg_color)
            title_butt.config(bg=bg_color)
            record_butt.config(bg='red', activebackground='red', fg='white', activeforeground='purple')


# Tuner window
def handle_clip_path(*args):
    print(f"handle_clip_path {clip_path.get()=}")
    if os.path.isfile(clip_path.get()) and os.path.getsize(clip_path.get()) > 0:  # bytes
        tuners.clip_path_label.config(bg=bg_color)
    else:
        tuners.clip_path_label.config(bg='yellow')


def handle_silent(*args):
    print(f"handle_silent {silent.get()=}")
    cf[SYS]['silent'] = str(silent.get())
    cf.save_to_file()


def open_tuner_window():
    tuner_window = tk.Toplevel(root, bg=bg_color)
    tuner_window.title("Tuner")
    # tuner_window.geometry("700x200")

    # Video delay row
    video_delay_tuner_frame = tk.Frame(tuner_window, bg=box_color, bd=4, relief=relief)
    video_delay_tuner_frame.pack(side=tk.TOP)
    vd_label = tk.Label(video_delay_tuner_frame, text="Video delay +/-", bg=bg_color)
    tuners.video_delay_tuner_butt = myButton(video_delay_tuner_frame, text=video_delay.get(), command=enter_video_delay, fg="purple", bg=bg_color)
    vd_label.pack(side="left", fill='x')
    tuners.video_delay_tuner_butt.pack(side="left", fill='x')

    # Clipcut row
    clipcut_frame = tk.Frame(tuner_window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    clipcut_frame.pack(side=tk.TOP)
    clipcut_label = tk.Label(clipcut_frame, text="Clip range, minutes:", bg=bg_color)
    tuners.start_clip_butt = myButton(clipcut_frame, text=start_clip.get(), command=enter_start_clip_time, fg="green", bg=bg_color)
    tuners.stop_clip_butt = myButton(clipcut_frame, text=stop_clip.get(), command=enter_stop_clip_time, fg="green", bg=bg_color)
    tuners.hms_label = tk.Label(clipcut_frame, text="  within " + "{:8.3f} minutes".format(raw_time.get()), bg=bg_color)
    clipcut_label.pack(side="left", fill='x')
    tuners.start_clip_butt.pack(side="left", fill='x')
    tuners.stop_clip_butt.pack(side="left", fill='x')
    tuners.hms_label.pack(side="left", fill='x')

    # Raw unsync row
    raw_frame = tk.Frame(tuner_window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    raw_frame.pack(fill='x')
    raw_label = tk.Label(raw_frame, text="Raw file=", bg=bg_color)
    tuners.raw_path_label = tk.Label(raw_frame, text=raw_path.get(), wraplength=wrap_length, justify=tk.RIGHT)
    tuners.raw_path_label.config(bg=bg_color)
    raw_label.pack(side="left", fill='x')
    tuners.raw_path_label.pack(side="left", fill='x')

    # Cut clip
    cut_clip_frame = tk.Frame(tuner_window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    cut_clip_frame.pack(side=tk.TOP)
    tuners.clip_cut_butt = myButton(cut_clip_frame, text=" CLIP IT ", command=clip_cut, bg='lightyellow', fg='black')
    cut_clip_label = tk.Label(cut_clip_frame, text="Clip file=", bg=bg_color)
    tuners.clip_path_label = tk.Label(cut_clip_frame, text=clip_file.get(), wraplength=wrap_length, justify=tk.RIGHT)
    tuners.clip_path_label.config(bg=bg_color)
    tuners.clip_cut_butt.pack(side="left", fill='x')
    cut_clip_label.pack(side="left", fill='x')
    tuners.clip_path_label.pack(side="left", fill='x')

    # Sync clip
    sync_clip_frame = tk.Frame(tuner_window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    sync_clip_frame.pack(side=tk.TOP)
    tuners.sync_clip_tuner_butt = myButton(sync_clip_frame, text="  SYNC CLIP  ", command=clip_cut, bg='lightyellow', fg='black')
    sync_clip_label = tk.Label(sync_clip_frame, text="Sync clip=", bg=bg_color)
    tuners.clip_path_label = tk.Label(sync_clip_frame, text=clip_file.get(), wraplength=wrap_length, justify=tk.RIGHT)
    tuners.clip_path_label.config(bg=bg_color)
    tuners.sync_clip_tuner_butt.pack(side="left", fill='x')
    sync_clip_label.pack(side="left", fill='x')
    tuners.clip_path_label.pack(side="left", fill='x')

    # Sync main
    sync_frame = tk.Frame(tuner_window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    sync_frame.pack(side=tk.TOP)
    tuners.sync_tuner_butt = myButton(sync_frame, text="***  SYNC    ***", command=clip_cut, bg='red', fg='white')
    sync_label = tk.Label(sync_frame, text="Sync =", bg=bg_color)
    tuners.out_path_label = tk.Label(sync_frame, text=out_file.get(), wraplength=wrap_length, justify=tk.RIGHT)
    tuners.out_path_label.config(bg=bg_color)
    tuners.sync_tuner_butt.pack(side="left", fill='x')
    sync_label.pack(side="left", fill='x')
    tuners.out_path_label.pack(side="left", fill='x')

    # Instructions
    tuner_doc_frame = tk.Frame(tuner_window, width=250, height=100, bg=bg_color, bd=4, relief=relief)
    tuner_doc_frame.pack(side=tk.TOP)
    tuner_doc = """Tune for video / audio sync.\n\
    - Set range to be within the length of original video.\n\
    - Press 'CLIP IT'.\n\
    - Go to file explorer and verify sync.   Adjust 'Video delay +/-' as necessary."""
    tuner_doc = tk.Label(tuner_doc_frame, text=tuner_doc, fg="black", justify='left', bg=bg_color)
    tuner_doc.pack(side="left", fill='x')

    handle_clip_path()
    clip_path.trace_add('write', handle_clip_path)
    handle_raw_path()
    # handle_folder_path()
    # handle_result_ready()


def record():
    if title.get() == '<enter title>' or title.get() == '' or title.get() == 'None':
        enter_title()
    if title.get() != '<enter title>' and title.get() != '' and title.get() != 'None':
        rf, rr = screencast(silent=silent.get(),
                            video_grabber=video_grab.get(), video_in=video_in.get(),
                            audio_grabber=audio_grab.get(), audio_in=audio_in.get(),
                            crf=crf.get(),
                            rec_time=rec_time.get()*60.,
                            output_file=raw_path.get())
        raw_path.set(rf)  # screencast may cause null filename if fails
        result_ready.set(rr)
        sync()
    else:
        print('aborting recording....need to enter title.  Presently = ', title.get())


def clip_cut():
    sf, rr = cut_clip(silent=silent.get(), raw_file=raw_path.get(),
                      start_clip=start_clip.get()*60., stop_clip=stop_clip.get()*60.,
                      clip_file=clip_path.get())
    if rr:
        tuners.clip_path_label.config(bg='lightgreen', fg='black')
        tuners.clip_cut_butt.config(bg='yellow', fg='black')
    else:
        tuners.clip_path_label.config(bg=bg_color, fg='black')
        tuners.clip_cut_butt.config(bg='red', fg='black')


def sync():
    if result_ready.get():
        if video_delay.get() >= 0.0:
            delay_video_sync(silent=silent.get(), delay=video_delay.get(), input_file=raw_path.get(),
                             output_file=os.path.join(os.getcwd(), out_path.get()))
        else:
            delay_audio_sync(silent=silent.get(), delay=-video_delay.get(), input_file=raw_path.get(),
                             output_file=os.path.join(os.getcwd(), out_path.get()))
        tuners.sync_tuner_butt.config(bg='lightgreen', activebackground='lightgreen', fg='red', activeforeground='purple')
    else:
        print("record first *******")


def sync_clip():
    if result_ready.get():
        if video_delay.get() >= 0.0:
            delay_video_sync(silent=silent.get(), delay=video_delay.get(), input_file=clip_path.get(),
                             output_file=os.path.join(os.getcwd(), clip_path.get()))
        else:
            delay_audio_sync(silent=silent.get(), delay=-video_delay.get(), input_file=clip_path.get(),
                             output_file=os.path.join(os.getcwd(), clip_path.get()))
        tuners.sync_clip_tuner_butt.config(bg='lightgreen', activebackground='lightgreen', fg='red', activeforeground='purple')
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
    raw_time = tk.DoubleVar(root, 0.)
    hms = tk.StringVar(root, '')
    out_file = tk.StringVar(root, title.get()+'.mkv')
    out_path = tk.StringVar(root, os.path.join(folder.get(), out_file.get()))
    clip_file = tk.StringVar(root, 'clip_' + title.get() + '.mkv')
    clip_path = tk.StringVar(root, os.path.join(folder.get(), 'clip_' + title.get() + '.mkv'))
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
    raw_path = tk.StringVar(root, os.path.join(folder.get(), title.get()+'_unsync.mkv'))
    result_ready = tk.BooleanVar(root, os.path.isfile(out_path.get()) and os.path.getsize(out_path.get()))
    start_clip = tk.DoubleVar(root, 0.0)
    stop_clip = tk.DoubleVar(root, 0.0)
    clip_path = tk.StringVar(root, os.path.join(folder.get(), title.get()+'_clip.mkv'))
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
    folder_butt = myButton(name_frame, text=folder.get(), command=enter_folder, fg="blue", bg=bg_color)
    slash = tk.Label(name_frame, text="/", fg="blue", bg=bg_color)
    title_butt = myButton(name_frame, text=title.get(), command=enter_title, fg="blue", bg=bg_color)
    enter_folder(cf[SYS]['folder'], True)
    enter_title(cf[SYS]['title'], True)
    folder_butt.pack(side="left", fill='x')
    slash.pack(side="left", fill='x')
    title_butt.pack(side="left", fill='x')

    # Recording length row
    length_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    length_frame.pack(fill='x')
    rec_length = tk.Label(length_frame, text="Recording length, minutes:", bg=bg_color)
    time_butt = myButton(length_frame, text=rec_time.get(), command=enter_rec_time, fg="green", bg=bg_color)
    hms.set("hms=" + str(timedelta(minutes=raw_time.get())))
    hms_label = tk.Label(length_frame, text=hms.get(), wraplength=wrap_length, justify=tk.LEFT, bg=bg_color)
    rec_length.pack(side="left", fill='x')
    time_butt.pack(side="left", fill='x')
    hms_label.pack(side="left", fill='x')

    # Quality row
    quality_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    quality_frame.pack(fill='x')
    crf_label = tk.Label(quality_frame, text="crf quality for ffmpeg:", bg=bg_color)
    crf_butt = myButton(quality_frame, text=crf.get(), command=enter_crf, fg="green", bg=bg_color)
    crf_label.pack(side="left", fill='x')
    crf_butt.pack(side="left", fill='x')

    # Video delay row
    video_delay_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    video_delay_frame.pack(fill='x')
    video_delay_label = tk.Label(video_delay_frame, text="Video delay +/-", bg=bg_color)
    video_delay_butt = myButton(video_delay_frame, text=str(video_delay.get()), command=enter_video_delay, fg="purple", bg=bg_color)
    video_delay_label.pack(side="left", fill='x')
    video_delay_butt.pack(side="left", fill='x')

    # Video row
    video_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    video_frame.pack(fill='x')
    video_grab_label = tk.Label(video_frame, text="Video:", bg=bg_color)
    video_grab_butt = myButton(video_frame, text=video_grab.get(), command=enter_video_grab, fg="purple", bg=bg_color)
    video_in_butt = myButton(video_frame, text=video_in.get(), command=enter_video_in, fg="purple", bg=bg_color)
    video_grab_label.pack(side="left", fill='x')
    video_grab_butt.pack(side="left", fill='x')
    video_in_butt.pack(side="left", fill='x')

    # Audio row
    audio_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    audio_frame.pack(fill='x')
    audio_grab_label = tk.Label(audio_frame, text="Audio:", bg=bg_color)
    audio_grab_butt = myButton(audio_frame, text=audio_grab.get(), command=enter_audio_grab, fg="purple", bg=bg_color)
    audio_in_butt = myButton(audio_frame, text=audio_in.get(), command=enter_audio_in, fg="purple", bg=bg_color)
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
    raw_path_label = tk.Label(action_frame, text=raw_path.get(), wraplength=wrap_length, justify=tk.RIGHT)
    raw_path_label.config(bg=bg_color)
    raw_path_label.pack(side="right", fill='x')
    action_label = tk.Label(action_frame, text="Intermediate=", bg=bg_color)
    action_label.pack(side="right", fill='x')

    # Record row
    record_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    record_frame.pack(fill='x')
    record_butt = myButton(record_frame, text='****    RECORD     ****', command=record, fg='white', bg='red', wraplength=wrap_length, justify=tk.CENTER)
    tuner_window_butt = myButton(record_frame, text="TUNER WINDOW", command=open_tuner_window, bg=bg_color)
    record_butt.pack(side="left", fill='x')
    tuner_window_butt.pack(side="right", fill='x')

    # Begin
    print("call handle_raw_path")
    handle_raw_path()
    raw_path.trace_add('write', handle_raw_path)
    handle_folder_path()
    out_path.trace_add('write', handle_folder_path)
    handle_silent()
    silent.trace_add('write', handle_silent)
    handle_result_ready()
    result_ready.trace_add('write', handle_result_ready)
    root.mainloop()
