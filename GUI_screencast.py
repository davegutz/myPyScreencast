#! /bin/sh
"exec" "`dirname $0`/venv/bin/python3" "$0" "$@"
##! /Users/daveg/Documents/GitHub/myStateOfCharge/SOC_Particle/py/venv/bin/python3.12
# The #! operates for macOS only. 'Python Launcher' (Python Script Preferences) option for 'Allow override with #! in script' is checked.
#  Graphical interface to screencast R
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

from screencast import screencast, delay_audio_sync, delay_video_sync, cut_clip, length_of, kill_ffmpeg
from configparser import ConfigParser
from datetime import timedelta
from tkinter import filedialog
from threading import Thread
import tkinter.simpledialog
import tkinter.messagebox
from myGmail import *
import sys
if sys.version_info < (3, 12):
    import pyautogui
else:
    from pynput.keyboard import Key, Controller
import pyperclip
import platform
import smtplib
import shutil
import time
if platform.system() == 'Darwin':
    # noinspection PyUnresolvedReferences
    from ttwidgets import TTButton as myButton
else:
    import tkinter as tk
    from tkinter import Button as myButton
global putty_shell


class Begini(ConfigParser):
    """Begini - configuration class using .ini files"""
    def __init__(self, name, def_dict_):
        login = os.getlogin()
        ConfigParser.__init__(self)
        (config_file_path, config_basename) = os.path.split(name)
        if sys.platform == 'linux':
            config_txt = os.path.splitext(config_basename)[0] + '_linux.ini'
            self.config_file_path = os.path.join('/home/daveg/.local/', config_txt)
        elif sys.platform == 'darwin':
            config_txt = os.path.splitext(config_basename)[0] + '_macos.ini'
            self.config_file_path = os.path.join('/Users/daveg/.local/', config_txt)
        else:
            config_txt = os.path.splitext(config_basename)[0] + '.ini'
            self.config_file_path = os.path.join(os.getenv('LOCALAPPDATA'), config_txt)
        print('config file path', self.config_file_path)
        if os.path.isfile(self.config_file_path):
            self.read(self.config_file_path)
        else:
            with open(self.config_file_path, 'w') as cfg_file:
                self.read_dict(def_dict_)
                self.write(cfg_file)
            print('wrote', self.config_file_path)

    def __str__(self, prefix=''):
        s = prefix + "begini:\n"
        s += "  config_file_path =  {:s}\n".format(self.config_file_path)
        return s

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


class Global:
    """Executive class to control the global variables"""

    def __init__(self, owner):
        self.sync_tuner_butt = myButton(owner)
        self.sync_clip_tuner_butt = myButton(owner)
        self.video_delay_tuner_butt = myButton(owner)
        self.hms_label = tk.Label(owner)
        self.intermediate_file_label = tk.Label(owner)
        self.raw_path_label = tk.Label(owner)
        self.raw_clip_file_label = tk.Label(owner)
        self.clip_path_label = tk.Label(owner)
        self.start_clip_butt = myButton(owner)
        self.stop_clip_butt = myButton(owner)
        self.clip_cut_butt = myButton(owner)
        self.out_path_label = tk.Label()
        self.window = None

    def update(self):
        self.out_path_label.config(text=R.out_file)
        self.raw_path_label.config(text=R.raw_path.get())
        self.raw_clip_file_label.config(text=raw_clip_file.get())
        self.clip_path_label.config(text=clip_file.get())


class MyRecorder:
    def __init__(self, sys, video_grab_, video_in_, audio_grab_, audio_in_,
                 cwd_path_, title_, folder_, destination_folder_, countdown_time_=10):
        self.sys = sys
        self.video_grab = video_grab_
        self.video_in = video_in_
        self.audio_grab = audio_grab_
        self.audio_in = audio_in_
        self.cwd_path = cwd_path_
        self.title = title_
        self.folder = folder_
        self.destination_folder = destination_folder_
        self.out_file = None
        self.raw_file = None
        self.raw_path = tk.StringVar(root, '')
        self.raw_path_label = tk.Label(root, text='', bg=bg_color, fg='black')
        self.out_file = None
        self.out_path = None
        self.target_path = tk.StringVar(root, '')
        self.new_result_ready = tk.BooleanVar(root)
        self.running = None
        self.thd_num = -1
        self.thread = []
        self.cast_button = myButton()
        self.stop_button = myButton()
        self.video_grab_butt = myButton()
        self.video_in_butt = myButton()
        self.audio_grab_butt = myButton()
        self.audio_in_butt = myButton()
        self.title_butt = myButton()
        self.folder_butt = myButton()
        self.destination_folder_butt = myButton()
        self.run_perm = False
        self.countdown_time = countdown_time_

    def __str__(self, prefix=''):
        s = prefix + "begini:\n"
        s += "  cwd_path =  '{:s}'\n".format(self.cwd_path)
        s += "  folder =  '{:s}'\n".format(self.folder)
        s += "  destination_folder =  '{:s}'\n".format(self.destination_folder)
        s += "  out_file =  '{:s}'\n".format(self.out_file)
        s += "  raw_file =  '{:s}'\n".format(self.raw_file)
        s += "  raw_path =  '{:s}'\n".format(self.raw_path.get())
        s += "  out_file =  '{:s}'\n".format(self.out_file)
        s += "  target_path =  '{:s}'\n".format(self.target_path.get())
        s += "  new_result_ready =  {:d}\n".format(self.new_result_ready.get())
        if self.running is not None:
            s += "  running =  {:d}\n".format(self.running)
        else:
            s += "  running =  None\n"
        s += "  run_perm =  {:d}\n".format(self.run_perm)
        s += "  countdown_time =  {:d}\n".format(self.countdown_time)
        return s

    def enter_audio_grab(self):
        answer = tk.simpledialog.askstring(title=__file__, prompt="ffmpeg audio_grab parameter",
                                           initialvalue=self.audio_grab)
        if answer is None or answer == ():
            print('enter operation cancelled')
            return
        self.audio_grab = answer
        cf[SYS]['audio_grab'] = self.audio_grab
        cf.save_to_file()
        self.audio_grab_butt.config(text=self.audio_grab)

    def enter_audio_in(self):
        answer = tk.simpledialog.askstring(title=__file__, prompt="ffmpeg audio_in parameter",
                                           initialvalue=self.audio_in)
        if answer is None or answer == ():
            print('enter operation cancelled')
            return
        self.audio_in = answer
        cf[SYS]['audio_in'] = self.audio_in
        cf.save_to_file()
        self.audio_in_butt.config(text=self.audio_in)

    def enter_destination_folder(self):
        answer = tk.filedialog.askdirectory(title="Select a destination (i.e. Library) folder",
                                            initialdir=self.destination_folder)
        if answer is not None and answer != '':
            self.destination_folder = answer
        cf[SYS]['destination_folder'] = self.destination_folder
        cf.save_to_file()
        self.destination_folder_butt.config(text=self.destination_folder)
        self.update_file_paths()
        handle_target_path()

    def enter_folder(self):
        answer = tk.filedialog.askdirectory(title="Select a Recordings Folder", initialdir=self.folder)
        if answer is not None and answer != '':
            self.folder = answer
        cf[SYS]['folder'] = self.folder
        cf.save_to_file()
        self.folder_butt.config(text=self.folder)
        self.update_file_paths()
        handle_target_path()

    def enter_title(self):
        answer = tk.simpledialog.askstring(title=__file__, prompt="enter title", initialvalue=self.title)
        if answer is not None:
            self.title = answer
        if self.title == '':
            self.title = '<enter title>'
        cf[SYS]['title'] = self.title
        cf.save_to_file()
        self.title_butt.config(text=self.title)
        self.update_file_paths()
        handle_target_path()

    def enter_video_grab(self):
        answer = tk.simpledialog.askstring(title=__file__, prompt="ffmpeg video_grab parameter",
                                           initialvalue=self.video_grab)
        if answer is None or answer == ():
            print('enter operation cancelled')
            return
        self.video_grab = answer
        cf[SYS]['video_grab'] = self.video_grab
        cf.save_to_file()
        self.video_grab_butt.config(text=self.video_grab)

    def enter_video_in(self):
        answer = tk.simpledialog.askstring(title=__file__, prompt="ffmpeg video_in parameter",
                                           initialvalue=self.video_in)
        if answer is None or answer == ():
            print('enter operation cancelled')
            return
        self.video_in = answer
        cf[SYS]['video_in'] = self.video_in
        cf.save_to_file()
        self.video_in_butt.config(text=self.video_in)

    def record(self):
        if self.running is True:
            print('already recording')
        else:
            self.thd_num += 1
            self.thread.append(FFmpegThread(silent.get(), self.thd_num))
            print('starting thread', self.thd_num, end='...')
            self.thread[self.thd_num].start()
            self.running = True
            print('started casting', self.raw_path.get())

    def kill(self):
        if self.running is not None:
            kill_ffmpeg(SYS)
            self.cast_button.config(bg="red", fg='black')
            self.stop_button.config(bg=bg_color, fg=bg_color)
            self.running = False
            print('Stopped recording; output in ', self.raw_path.get())
        else:
            print('R was not running')
        if self.run_perm is True:
            self.run_perm = False
            self.cast_button.config(bg="red", fg='black')
            self.stop_button.config(bg=bg_color, fg=bg_color)
            print('Interrupted.  Start permission cancelled')
            print(f"record:  actual {length_of(R.target_path.get())} != demand {rec_time.get()}")
            if abs(length_of(R.target_path.get()) - rec_time.get()) < 1:
                msg = 'Interrupted but target ready within 1 min'
                print(msg)
            else:
                msg = 'Interrupted and >1 min size difference'
                thread = Thread(target=send_message, kwargs={'subject': R.title, 'message': msg})
                thread.start()
            handle_target_path()

    def update_file_paths(self):
        """Use 'title' and 'folder' to set paths of all files used"""
        self.out_file = self.title + '.mp4'
        self.out_path = os.path.join(self.folder, self.out_file)
        self.new_result_ready.set(size_of(self.out_path) > 0)
        new_target_path = os.path.join(self.destination_folder, self.out_file)
        if new_target_path != self.target_path.get():
            self.target_path.set(str(new_target_path))  # Trip the trace only on actual change
        self.raw_file = self.title + '_raw.mp4'
        self.raw_path.set(str(os.path.join(self.folder, self.raw_file)))
        self.raw_path_label.config(text=self.raw_path.get())

        # paint
        if self.title == '' or self.title == '<enter title>':
            paint(self.title_butt, bg='pink')
        else:
            paint(self.title_butt, bg=bg_color)
        if os.path.exists(self.folder):
            paint(self.folder_butt, bg='lightgreen')
        else:
            paint(self.folder_butt, bg='pink')
        if self.title != '<enter title>':
            if size_of(self.target_path.get()) > 0:
                paint(self.title_butt, bg='yellow')
            else:
                paint(self.title_butt, bg=bg_color)
        if os.path.exists(self.destination_folder):
            paint(self.destination_folder_butt, bg='lightgreen')
        else:
            paint(self.destination_folder_butt, bg='pink')


class FFmpegThread(Thread):
    """Wrap thread class so can extract resulting filename"""
    def __init__(self, silent_, eyed):
        Thread.__init__(self)
        self.silent = silent_
        self.result_path = None
        self.id = eyed

    def run(self):
        """Start screencast thread.  The 'send_message' separate thread is self terminating."""
        if R.title == '<enter title>' or R.title == '' or R.title == 'None':
            R.enter_title()
        if R.title != '<enter title>' and R.title != '' and R.title != 'None':
            thread_active.set(thread_active.get()+1)
            print('sending message')
            thread = Thread(target=send_message, kwargs={'subject': R.title, 'message': 'Starting ' +
                                                                                        str(rec_time.get())})
            thread.start()
            rf, rr = screencast(silent=silent.get(),
                                video_grabber=R.video_grab, video_in=R.video_in,
                                audio_grabber=R.audio_grab, audio_in=R.audio_in,
                                crf=crf.get(),
                                rec_time=rec_time.get()*60.,
                                output_file=R.raw_path.get())
            R.running = False
            if rf is not None and rr is True:
                R.raw_path.set(rf)  # screencast may cause null filename if fails
                R.new_result_ready.set(rr)
                sync()
            if size_of(R.target_path.get()) > 0:
                root.lift()
                print('sending message')
                if abs(length_of(R.target_path.get()) - rec_time.get()) < 1:
                    msg = 'target ready'
                else:
                    print(f"record:  actual {length_of(R.target_path.get())} != demand {rec_time.get()}")
                    msg = 'Done but >1 min size difference'
                thread = Thread(target=send_message, kwargs={'subject': R.title, 'message': msg})
                thread.start()
                if sys.version_info > (3, 11):
                    keyboard = Controller()
                    keyboard.press(Key.f5)  # Attempt to exit fullscreen
                else:
                    pyautogui.press('F5')  # Attempt to exit fullscreen
                tk.messagebox.showinfo(title='Screencast', message=msg)
                update_all_file_paths()
        else:
            print('aborting recording....need to enter title.  Presently = ', R.title)
        thread_active.set(thread_active.get()-1)


# Global methods
def add_to_clip_board(text):
    pyperclip.copy(text)


def cast():
    """After 'pushing the button' check if over-writing then start countdown"""
    confirmation = tk.messagebox.askokcancel('reminder', 'Have you turned on subtitles?')
    if confirmation is False:
        return
    confirmation = tk.messagebox.askokcancel('reminder', 'Have you redirected sound?')
    if confirmation is False:
        return
    if size_of(R.target_path.get()) > 0:  # bytes
        confirmation = tk.messagebox.askyesno('query overwrite', 'Target exists:  overwrite?')
        if confirmation is False:
            print('enter different folder or title first row')
            tk.messagebox.showwarning(message='enter different folder or title first row')
            return
    R.cast_button.config(bg=bg_color)
    R.stop_button.config(bg='black', activebackground='black', fg='white', activeforeground='white')
    R.run_perm = True
    countdown_time.set(R.countdown_time)
    cast_countdown()


def cast_countdown():
    """Countdown then call record()"""
    if R.run_perm is False:
        return
    msg = 'Counting down'
    countdown_time.set(countdown_time.get() - 1)
    print(f"{msg=}")
    print(f"{countdown_time.get()=}")
    counter_status.config(text=f'{msg} ({countdown_time.get()}sec)')
    if countdown_time.get() > 0:
        counter.deiconify()
        counter.lift()
        center_timer()
        root.after(1000, cast_countdown)
    else:
        counter.withdraw()
        thread = Thread(target=stay_awake, kwargs={'up_set_min': rec_time.get()})
        thread.start()
        R.record()  # this blocks.  'STOP' is used to end early


def center_timer(width=200, height=100):
    # get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # calculate position x and y coordinates
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    counter.geometry('%dx%d+%d+%d' % (width, height, x, y))


def clip_cut():
    print("\nCutting", R.raw_path.get(), "time", start_clip.get(), "-", stop_clip.get(), "min. to", raw_clip_path.get())
    cut_clip(silent=silent.get(), raw_file=R.raw_path.get(),
             start_clip=start_clip.get()*60., stop_clip=stop_clip.get()*60.,
             clip_file=raw_clip_path.get())
    update_all_file_paths()


def contain_all(testpath):
    """Split all information contained in file path"""
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


def enter_crf():
    answer = tk.simpledialog.askinteger(title=__file__, prompt="enter ffmpeg crf, lower is larger file",
                                        initialvalue=crf.get())
    if answer is None or answer == ():
        print('enter operation cancelled')
        return
    crf.set(answer)
    cf[SYS]['crf'] = str(crf.get())
    cf.save_to_file()
    crf_butt.config(text=crf.get())


def enter_rec_time():
    answer = tk.simpledialog.askfloat(title=__file__, prompt="enter record time, minutes",
                                      initialvalue=rec_time.get())
    if answer is None or answer == ():
        print('enter operation cancelled')
        return
    rec_time.set(answer)
    cf[SYS]['rec_time'] = str(rec_time.get())
    cf.save_to_file()
    time_butt.config(text=rec_time.get())


def enter_start_clip_time():
    answer = tk.simpledialog.askfloat(title=__file__, prompt="enter clip start, minutes",
                                      initialvalue=start_clip.get())
    if answer is None or answer == ():
        print('enter operation cancelled')
        return
    start_clip.set(answer)
    tuners.start_clip_butt.config(text=start_clip.get())


def enter_stop_clip_time():
    answer = tk.simpledialog.askfloat(title=__file__, prompt="enter clip stop, minutes",
                                      initialvalue=stop_clip.get())
    if answer is None or answer == ():
        print('enter operation cancelled')
        return
    stop_clip.set(answer)
    tuners.stop_clip_butt.config(text=stop_clip.get())


def enter_video_delay():
    answer = tk.simpledialog.askfloat(title=__file__, prompt="enter seconds video delay audio +/-",
                                      initialvalue=video_delay.get())
    if answer is None or answer == ():
        print('enter operation cancelled')
        return
    video_delay.set(float(answer))
    cf[SYS]['video_delay'] = str(video_delay.get())
    cf.save_to_file()
    video_delay_butt.config(text=str(video_delay.get()))
    tuners.video_delay_tuner_butt.config(text=str(video_delay.get()))


def handle_target_path(*_args):
    R.new_result_ready.set(False)
    if size_of(R.target_path.get()) > 0:  # bytes
        tk.messagebox.showwarning(message='target file exists')
    if size_of(R.raw_path.get()) > 0:  # bytes
        record_time = length_of(R.raw_path.get())
        if record_time is not None:
            raw_time.set(record_time / 60.)
        else:
            raw_time.set(0.)
    else:
        raw_time.set(0.)
    hms.set("hms=" + str(timedelta(minutes=raw_time.get())))
    hms_label.config(text=hms.get())
    tuners.hms_label.config(text=hms.get())
    cf.save_to_file()
    update_all_file_paths()
    # action_label.config(text=tuners.raw_clip_file_label)
    tuners.update()


def handle_raw_path(*_args):
    update_all_file_paths()


def handle_new_result_ready(*_args):
    if size_of(R.out_path) > 0:  # bytes
        if R.new_result_ready.get():
            paint(R.cast_button, bg='yellow', activebackground='yellow', fg='black', activeforeground='purple')
            paint(R.stop_button, bg=bg_color, activebackground=bg_color, fg=bg_color, activeforeground=bg_color)
            record_time = length_of(R.raw_path.get())
            if record_time is not None:
                raw_time.set(record_time / 60.)
            else:
                raw_time.set(0.)
            hms.set("hms=" + str(timedelta(minutes=raw_time.get())))
            hms_label.config(text=hms.get())
            tuners.hms_label.config(text=hms.get())
        else:
            paint(R.cast_button, bg='red', activebackground='red', fg='white', activeforeground='purple')
            paint(R.stop_button, bg=bg_color, activebackground=bg_color, fg=bg_color, activeforeground=bg_color)


def handle_clip_path(*_args):
    """Tuner window"""
    update_all_file_paths()


def handle_instructions(*_args):
    cf[SYS]['instructions'] = str(instructions.get())
    cf.save_to_file()
    if instructions.get():
        doc_block.config(text=doc)
    else:
        doc_block.config(text='')


def handle_silent(*_args):
    cf[SYS]['silent'] = str(silent.get())
    cf.save_to_file()


def open_tuner_window():
    if tuners.window is not None:
        print(f"Tuner already open")
        tuners.window.lift()
        return

    tuners.window = tk.Toplevel(root, bg=bg_color)
    tuners.window.title("Tuner")
    # tuners.window.geometry("700x200")

    # Video delay row
    video_delay_tuner_frame = tk.Frame(tuners.window, bg=box_color, bd=4, relief=relief)
    video_delay_tuner_frame.pack(side=tk.TOP)
    vd_label = tk.Label(video_delay_tuner_frame, text="Video delay +/-", bg=bg_color)
    tuners.video_delay_tuner_butt = myButton(video_delay_tuner_frame, text=video_delay.get(),
                                             command=enter_video_delay, fg="purple", bg=bg_color)
    vd_label.pack(side="left", fill='x')
    tuners.video_delay_tuner_butt.pack(side="left", fill='x')

    # Clipcut row
    clipcut_frame = tk.Frame(tuners.window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    clipcut_frame.pack(side=tk.TOP)
    clipcut_label = tk.Label(clipcut_frame, text="Clip range, minutes:", bg=bg_color)
    tuners.start_clip_butt = myButton(clipcut_frame, text=start_clip.get(),
                                      command=enter_start_clip_time, fg="green", bg=bg_color)
    tuners.stop_clip_butt = myButton(clipcut_frame, text=stop_clip.get(),
                                     command=enter_stop_clip_time, fg="green", bg=bg_color)
    tuners.hms_label = tk.Label(clipcut_frame, text="  within " + "{:8.3f} minutes".format(raw_time.get()), bg=bg_color)
    clipcut_label.pack(side="left", fill='x')
    tuners.start_clip_butt.pack(side="left", fill='x')
    tuners.stop_clip_butt.pack(side="left", fill='x')
    tuners.hms_label.pack(side="left", fill='x')

    # Raw unsync row
    raw_frame = tk.Frame(tuners.window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    raw_frame.pack(fill='x')
    raw_label = tk.Label(raw_frame, text="Raw file=", bg=bg_color)
    tuners.raw_path_label = tk.Label(raw_frame, text=R.raw_path.get(), wraplength=wrap_length, justify=tk.RIGHT)
    tuners.raw_path_label.config(bg=bg_color)
    raw_label.pack(side="left", fill='x')
    tuners.raw_path_label.pack(side="left", fill='x')

    # Raw clip
    raw_clip_frame = tk.Frame(tuners.window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    raw_clip_frame.pack(side=tk.TOP)
    tuners.clip_cut_butt = myButton(raw_clip_frame, text=" CLIP IT ", command=clip_cut, bg=bg_color, fg='black')
    raw_clip_label = tk.Label(raw_clip_frame, text="Clip file=", bg=bg_color)
    tuners.raw_clip_file_label = tk.Label(raw_clip_frame, text=raw_clip_file.get(), wraplength=wrap_length,
                                          justify=tk.RIGHT)
    tuners.raw_clip_file_label.config(bg=bg_color)
    tuners.clip_cut_butt.pack(side="left", fill='x')
    raw_clip_label.pack(side="left", fill='x')
    tuners.raw_clip_file_label.pack(side="left", fill='x')

    # Sync clip
    sync_clip_frame = tk.Frame(tuners.window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    sync_clip_frame.pack(side=tk.TOP)
    tuners.sync_clip_tuner_butt = myButton(sync_clip_frame, text="  SYNC CLIP  ", command=sync_clip, bg=bg_color,
                                           fg='black')
    sync_clip_label = tk.Label(sync_clip_frame, text="Sync clip=", bg=bg_color)
    tuners.clip_path_label = tk.Label(sync_clip_frame, text=clip_file.get(), wraplength=wrap_length, justify=tk.RIGHT)
    tuners.clip_path_label.config(bg=bg_color)
    tuners.sync_clip_tuner_butt.pack(side="left", fill='x')
    sync_clip_label.pack(side="left", fill='x')
    tuners.clip_path_label.pack(side="left", fill='x')

    # Sync main
    sync_frame = tk.Frame(tuners.window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    sync_frame.pack(side=tk.TOP)
    tuners.sync_tuner_butt = myButton(sync_frame, text="***  SYNC    ***", command=sync, bg='red', fg='white')
    sync_label = tk.Label(sync_frame, text="Sync =", bg=bg_color)
    tuners.out_path_label = tk.Label(sync_frame, text=R.out_file, wraplength=wrap_length, justify=tk.RIGHT)
    tuners.out_path_label.config(bg=bg_color)
    tuners.sync_tuner_butt.pack(side="left", fill='x')
    sync_label.pack(side="left", fill='x')
    tuners.out_path_label.pack(side="left", fill='x')

    # Instructions
    tuner_doc_frame = tk.Frame(tuners.window, width=250, height=100, bg=bg_color, bd=4, relief=relief)
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
    tuners.open = True


def paint(tk_object, bg='lightgray', fg='black', activebackground=None, activeforeground=None):
    if activebackground is None:
        activebackground = bg
    if activeforeground is None:
        activeforeground = fg
    tk_object.config(bg=bg, activebackground=activebackground, fg=fg, activeforeground=activeforeground)


def print_vars():
    print("\n\ncf=", cf)
    print("R=", R)
    print(f"GLOBALS")
    print(f"{clip_file.get()=}")
    print(f"{clip_path.get()=}")
    print(f"{countdown_time.get()=}")
    print(f"{crf.get()=}")
    print(f"{cwd_path.get()=}")
    print(f"{instructions.get()=}")
    print(f"{hms.get()=}")
    print(f"{raw_clip_file.get()=}")
    print(f"{raw_clip_path.get()=}")
    print(f"{raw_time.get()=}")
    print(f"{rec_time.get()=}")
    print(f"{silent.get()=}")
    print(f"{start_clip.get()=}")
    print(f"{stop_clip.get()=}")
    print(f"{thread_active.get()=}")
    print(f"{video_delay.get()=}")


def send_message(email=my_email, password=my_app_password, to=my_text, subject='undefined', message='undefined'):
    """Sends email from 'email' to 'to'"""
    try:
        # Only for gmail account.
        with smtplib.SMTP('smtp.gmail.com:587') as server:
            server.ehlo()  # local host
            server.starttls()  # Puts the connection to the SMTP server
            server.login(email, password)
            # Format the subject and message together
            message = 'Subject: {}\n\n{}'.format(subject, message)
            server.sendmail(email, to, message)
            print('Message sent')
    except Exception as e:
        print("send_message failed:", e)


def size_of(path):
    if os.path.isfile(path) and (size := os.path.getsize(path)) > 0:  # bytes
        return size
    else:
        return 0


def stay_awake(up_set_min=3.):
    """Keep computer awake using shift key when recording then return to previous state"""

    # Timer starts
    start_time = float(time.time())
    up_time_min = 0.0
    if sys.version_info < (3, 12):
        # FAILSAFE to FALSE feature is enabled by default so that you can easily stop execution of
        # your pyautogui program by manually moving the mouse to the upper left corner of the screen.
        # Once the mouse is in this location, pyautogui will throw an exception and exit.
        pyautogui.FAILSAFE = False
    while True and (up_time_min < up_set_min):
        time.sleep(30.)
        if sys.version_info > (3, 11):
            keyboard = Controller()
        for i in range(0, 3):
            if sys.version_info > (3, 11):
                keyboard.press(Key.shift)  # shift key does not disturb fullscreen
            else:
                pyautogui.press('shift')  # Shift key does not disturb fullscreen
        up_time_min = (time.time() - start_time) / 60.
        print(f"stay_awake: {up_time_min=}")
    print(f"stay_awake: ending")
        
        
def sync():
    if size_of(R.raw_path.get()) > 0:
        if video_delay.get() >= 0.0:
            delay_video_sync(silent=silent.get(), delay=video_delay.get(), input_file=R.raw_path.get(),
                             output_file=R.out_path)
        else:
            delay_audio_sync(silent=silent.get(), delay=-video_delay.get(), input_file=R.raw_path.get(),
                             output_file=R.out_path)
        if size_of(R.out_path) > 0:
            shutil.move(R.out_path, R.target_path.get())
            print("Moved synchronized result to ", R.target_path.get())
        update_all_file_paths()
    else:
        print("record first *******")


def sync_clip():
    print(f"{raw_clip_path.get()=}")
    if size_of(raw_clip_path.get()) > 0:
        if video_delay.get() >= 0.0:
            delay_video_sync(silent=silent.get(), delay=video_delay.get(), input_file=raw_clip_path.get(),
                             output_file=os.path.join(os.getcwd(), clip_path.get()))
        else:
            delay_audio_sync(silent=silent.get(), delay=-video_delay.get(), input_file=raw_clip_path.get(),
                             output_file=os.path.join(os.getcwd(), clip_path.get()))
        update_all_file_paths()
    else:
        print("record clip first *******")


def update_all_file_paths():
    """Use 'title' and 'folder' to set paths of all files used"""
    R.update_file_paths()
    if size_of(R.raw_path.get()) > 0:
        paint(R.raw_path_label, bg='yellow')
        paint(tuners.raw_path_label, bg='yellow')
        paint(R.cast_button, bg='yellow', activebackground='yellow', fg='black', activeforeground='purple')
    else:
        paint(R.raw_path_label, bg=bg_color)
        paint(tuners.raw_path_label, bg=bg_color)
        paint(R.cast_button, bg='red', activebackground='red', fg='white', activeforeground='purple')
    raw_clip_file.set(R.title + '_clip_raw.mp4')
    raw_clip_path.set(os.path.join(R.folder, raw_clip_file.get()))
    if size_of(raw_clip_path.get()) > 0:
        paint(tuners.raw_clip_file_label, bg='yellow')
    else:
        paint(tuners.raw_clip_file_label, bg=bg_color)
    if size_of(clip_path.get()) > 0:
        paint(tuners.clip_path_label, bg='yellow')
    else:
        paint(tuners.clip_path_label, bg=bg_color)
    clip_file.set(R.title + '_clip.mp4')
    clip_path.set(os.path.join(R.folder, clip_file.get()))


if __name__ == '__main__':
    import os
    import tkinter as tk
    SYS = platform.system()

    # Configuration for entire folder selection read with filepaths
    def_dict = {
                'Linux':   {"folder": '<enter working folder>',
                            "destination_folder": '<enter destination folder>',
                            "title":  '<enter title>',
                            "rec_time": '0.1',
                            "crf": '25',
                            "video_grab": 'x11grab',
                            "video_in": ':0.0+0.0',
                            "audio_grab": 'pulse',
                            "audio_in": 'default',
                            "silent": '1',
                            "instructions": '1',
                            "video_delay": '0.5'},
                'Windows': {"folder": '<enter working folder>',
                            "destination_folder": '<enter destination folder>',
                            "title": '<enter title>',
                            "rec_time": '0.1',
                            "crf": '28',
                            "video_grab": "gdigrab",
                            "video_in": 'desktop',
                            "audio_grab": 'dshow',
                            "audio_in": 'audio="CABLE Output (VB-Audio Virtual Cable)"',
                            "silent": '1',
                            "instructions": '1',
                            "video_delay": '0.0'},
                'Darwin':  {"folder": '<enter working folder>',
                            "destination_folder": '<enter destination folder>',
                            "title":  '<enter title>',
                            "rec_time": '0.1',
                            "crf": '25',
                            "video_grab": 'avfoundation',
                            "video_in": '1',
                            "audio_grab": '',
                            "audio_in": '2',
                            "silent": '1',
                            "instructions": '1',
                            "video_delay": '0.0'},
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
      That is done outside this program.
    - There is no need to start 'caffeine' or equivalent as this app will press the shift key while recording."""
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
      That is done outside this program.
    - There is no need to start 'caffeine' or equivalent as this app will press the shift key while recording."""
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
      That is done outside this program.
    - There is no need to start 'caffeine' or equivalent as this app will press the shift key while recording."""
    else:
        print('os unknown')

    # Frame properties
    min_width = 600
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
    counter = tk.Tk()
    counter.attributes('-topmost', True)
    thread_active = tk.IntVar(root, 0)
    tuners = Global(root)
    script_loc = os.path.dirname(os.path.abspath(__file__))
    cwd_path = tk.StringVar(root, os.getcwd())
    rec_time = tk.DoubleVar(root, float(cf[SYS]['rec_time']))
    crf = tk.IntVar(root, int(cf[SYS]['crf']))
    video_delay = tk.DoubleVar(root, float(cf[SYS]['video_delay']))
    if cf[SYS]['silent'] == 'False':
        silent = tk.BooleanVar(root, False)
    else:
        silent = tk.BooleanVar(root, True)
    if cf[SYS]['instructions'] == 'False':
        instructions = tk.BooleanVar(root, False)
    else:
        instructions = tk.BooleanVar(root, True)
    root.iconphoto(False, tk.PhotoImage(file=os.path.join(script_loc, 'GUI_screencast_Icon.png')))
    raw_time = tk.DoubleVar(root, 0.)
    hms = tk.StringVar(root, '')
    raw_clip_file = tk.StringVar(root)
    raw_clip_path = tk.StringVar(root)
    clip_file = tk.StringVar(root)
    clip_path = tk.StringVar(root)
    # hms_label = tk.Label(root)
    COUNTDOWN_SEC = 10
    R = MyRecorder(SYS, cf[SYS]['video_grab'], cf[SYS]['video_in'], cf[SYS]['audio_grab'], cf[SYS]['audio_in'],
                   cwd_path.get(), cf[SYS]['title'], cf[SYS]['folder'], cf[SYS]['destination_folder'], COUNTDOWN_SEC)
    countdown_time = tk.IntVar(root, R.countdown_time)

    # Pre-define so update_all_file_paths() works
    update_all_file_paths()

    # raw_path = tk.StringVar(root, raw_path.get())
    start_clip = tk.DoubleVar(root, 0.0)
    stop_clip = tk.DoubleVar(root, 0.0)
    clip_path = tk.StringVar(root, clip_path.get())
    # row = -1

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

    # Name rows
    name_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    name_frame.pack(fill='x')
    working_label = tk.Label(name_frame, text="Working folder=", bg=bg_color)
    R.folder_butt = myButton(name_frame, text=R.folder, command=R.enter_folder, fg="blue", bg=bg_color)
    working_label.pack(side='left', fill='x')
    R.folder_butt.pack(side="left", fill='x')
    target_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    target_frame.pack(fill='x')
    destination_label = tk.Label(target_frame, text="Target =", bg=bg_color)
    R.destination_folder_butt = myButton(target_frame, text=R.destination_folder, command=R.enter_destination_folder,
                                         fg="blue", bg=bg_color)
    slash = tk.Label(target_frame, text="/", fg="blue", bg=bg_color)
    R.title_butt = myButton(target_frame, text=R.title, command=R.enter_title, fg="blue", bg=bg_color)
    destination_label.pack(side="left", fill='x')
    R.destination_folder_butt.pack(side="left", fill='x')
    slash.pack(side="left", fill='x')
    R.title_butt.pack(side="left", fill='x')

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
    video_delay_butt = myButton(video_delay_frame, text=str(video_delay.get()), command=enter_video_delay, fg="purple",
                                bg=bg_color)
    video_delay_label.pack(side="left", fill='x')
    video_delay_butt.pack(side="left", fill='x')

    # Video row
    video_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    video_frame.pack(fill='x')
    video_grab_label = tk.Label(video_frame, text="Video:", bg=bg_color)
    R.video_grab_butt = myButton(video_frame, text=R.video_grab, command=R.enter_video_grab, fg="purple", bg=bg_color)
    R.video_in_butt = myButton(video_frame, text=R.video_in, command=R.enter_video_in, fg="purple", bg=bg_color)
    video_grab_label.pack(side="left", fill='x')
    R.video_grab_butt.pack(side="left", fill='x')
    R.video_in_butt.pack(side="left", fill='x')

    # Audio row
    audio_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    audio_frame.pack(fill='x')
    audio_grab_label = tk.Label(audio_frame, text="Audio:", bg=bg_color)
    R.audio_grab_butt = myButton(audio_frame, text=R.audio_grab, command=R.enter_audio_grab, fg="purple", bg=bg_color)
    R.audio_in_butt = myButton(audio_frame, text=R.audio_in, command=R.enter_audio_in, fg="purple", bg=bg_color)
    audio_grab_label.pack(side="left", fill='x')
    R.audio_grab_butt.pack(side="left", fill='x')
    R.audio_in_butt.pack(side="left", fill='x')

    # Silent row
    silent_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    silent_frame.pack(fill='x')
    silent_butt = tk.Checkbutton(silent_frame, text='silent', bg=bg_color, variable=silent, onvalue=True,
                                 offvalue=False)
    instructions_butt = tk.Checkbutton(silent_frame, text='instructions', bg=bg_color, variable=instructions,
                                       onvalue=True, offvalue=False)
    silent_butt.pack(side="left", fill='x')
    instructions_butt.pack(side="left", fill='x')

    # Action row
    action_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    action_frame.pack(fill='x')
    R.raw_path_label = tk.Label(action_frame, text=R.raw_path.get(), wraplength=wrap_length, justify=tk.RIGHT,
                                bg=bg_color)
    R.raw_path_label.pack(side="right", fill='x')
    action_label = tk.Label(action_frame, text="Intermediate=", bg=bg_color)
    action_label.pack(side="right", fill='x')

    # Record row
    cast_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    cast_frame.pack(fill='x')
    R.cast_button = myButton(cast_frame, text='****    START      ****', command=cast, fg='white', bg='red',
                             wraplength=wrap_length, justify=tk.CENTER)
    R.stop_button = myButton(cast_frame, text='****   STOP EARLY  ****', command=R.kill, fg=bg_color, bg=bg_color,
                             wraplength=wrap_length, justify=tk.CENTER)
    tuner_window_butt = myButton(cast_frame, text="TUNER WINDOW", command=open_tuner_window, bg=bg_color)
    R.cast_button.pack(side="left", fill='x')
    R.stop_button.pack(side="left", fill='x')
    tuner_window_butt.pack(side="right", fill='x')
    counter_status = tk.Label(counter, text="Press START to begin recording")
    counter_status.pack()

    # Begin
    handle_raw_path()
    R.raw_path.trace_add('write', handle_raw_path)
    handle_target_path()
    R.target_path.trace_add('write', handle_target_path)
    handle_silent()
    silent.trace_add('write', handle_silent)
    handle_instructions()
    instructions.trace_add('write', handle_instructions)
    handle_new_result_ready()
    R.new_result_ready.trace_add('write', handle_new_result_ready)
    root.mainloop()
    counter.mainloop()
    counter.withdraw()
