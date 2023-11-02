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

from screencast import screencast, delay_audio_sync, delay_video_sync, cut_clip, length_of
from configparser import ConfigParser
from datetime import timedelta
from tkinter import filedialog
from threading import Thread
import tkinter.simpledialog
import tkinter.messagebox
from myGmail import *
import pyautogui
import pyperclip
import platform
import smtplib
import shutil
import time
if platform.system() == 'Darwin':
    from ttwidgets import TTButton as myButton
else:
    import tkinter as tk
    from tkinter import Button as myButton
global putty_shell


class Begini(ConfigParser):
    """Begini - configuration class using .ini files"""
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


# Global methods
def add_to_clip_board(text):
    pyperclip.copy(text)


def size_of(path):
    if os.path.isfile(path) and (size := os.path.getsize(path)) > 0:  # bytes
        return size
    else:
        return 0


def clip_cut():
    cut_clip(silent=silent.get(), raw_file=raw_path.get(),
             start_clip=start_clip.get()*60., stop_clip=stop_clip.get()*60.,
             clip_file=clip_path.get())
    update_file_paths()


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


def enter_destination_folder():
    answer = tk.filedialog.askdirectory(title="Select a destination (i.e. Library) folder", initialdir=destination_folder.get())
    if answer is not None and answer != '':
        destination_folder.set(answer)
    cf[SYS]['destination_folder'] = destination_folder.get()
    cf.save_to_file()
    destination_folder_butt.config(text=destination_folder.get())
    update_file_paths()


def enter_folder():
    answer = tk.filedialog.askdirectory(title="Select a Recordings Folder", initialdir=folder.get())
    if answer is not None and answer != '':
        folder.set(answer)
    cf[SYS]['folder'] = folder.get()
    cf.save_to_file()
    folder_butt.config(text=folder.get())
    update_file_paths()


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


def enter_title():
    answer = tk.simpledialog.askstring(title=__file__, prompt="enter title", initialvalue=title.get())
    if answer is not None:
        title.set(answer)
    if title.get() == '':
        title.set('<enter title>')
    cf[SYS]['title'] = title.get()
    cf.save_to_file()
    title_butt.config(text=title.get())
    update_file_paths()


def enter_video_delay():
    video_delay.set(float(tk.simpledialog.askfloat(title=__file__, prompt="enter seconds video delay audio +/-", initialvalue=video_delay.get())))
    cf[SYS]['video_delay'] = str(video_delay.get())
    cf.save_to_file()
    video_delay_butt.config(text=str(video_delay.get()))
    tuners.video_delay_tuner_butt.config(text=str(video_delay.get()))


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


def handle_target_path(*args):
    new_result_ready.set(False)
    if size_of(target_path.get()) > 0:  # bytes
        tk.messagebox.showwarning(message='target file exists')
    if size_of(raw_path.get()) > 0:  # bytes
        record_time = length_of(raw_path.get(), silent=silent.get())
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
    update_file_paths()


def handle_raw_path(*args):
    update_file_paths()


def handle_new_result_ready(*args):
    if size_of(out_path.get()) > 0:  # bytes
        if new_result_ready.get():
            paint(record_butt, bg='yellow', activebackground='yellow', fg='black', activeforeground='purple')
            record_time = length_of(raw_path.get(), silent=silent.get())
            if record_time is not None:
                raw_time.set(record_time / 60.)
            else:
                raw_time.set(0.)
            hms.set("hms=" + str(timedelta(minutes=raw_time.get())))
            hms_label.config(text=hms.get())
            tuners.hms_label.config(text=hms.get())
        else:
            paint(record_butt, bg='red', activebackground='red', fg='white', activeforeground='purple')


def handle_clip_path(*args):
    """Tuner window"""
    update_file_paths()


def handle_instructions(*args):
    cf[SYS]['instructions'] = str(instructions.get())
    cf.save_to_file()
    if instructions.get():
        doc_block.config(text=doc)
    else:
        doc_block.config(text='')


def handle_silent(*args):
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

    # Raw clip
    raw_clip_frame = tk.Frame(tuner_window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    raw_clip_frame.pack(side=tk.TOP)
    tuners.clip_cut_butt = myButton(raw_clip_frame, text=" CLIP IT ", command=clip_cut, bg=bg_color, fg='black')
    raw_clip_label = tk.Label(raw_clip_frame, text="Clip file=", bg=bg_color)
    tuners.raw_clip_file_label = tk.Label(raw_clip_frame, text=raw_clip_file.get(), wraplength=wrap_length, justify=tk.RIGHT)
    tuners.raw_clip_file_label.config(bg=bg_color)
    tuners.clip_cut_butt.pack(side="left", fill='x')
    raw_clip_label.pack(side="left", fill='x')
    tuners.raw_clip_file_label.pack(side="left", fill='x')

    # Sync clip
    sync_clip_frame = tk.Frame(tuner_window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    sync_clip_frame.pack(side=tk.TOP)
    tuners.sync_clip_tuner_butt = myButton(sync_clip_frame, text="  SYNC CLIP  ", command=sync_clip, bg=bg_color, fg='black')
    sync_clip_label = tk.Label(sync_clip_frame, text="Sync clip=", bg=bg_color)
    tuners.clip_path_label = tk.Label(sync_clip_frame, text=clip_file.get(), wraplength=wrap_length, justify=tk.RIGHT)
    tuners.clip_path_label.config(bg=bg_color)
    tuners.sync_clip_tuner_butt.pack(side="left", fill='x')
    sync_clip_label.pack(side="left", fill='x')
    tuners.clip_path_label.pack(side="left", fill='x')

    # Sync main
    sync_frame = tk.Frame(tuner_window, width=250, height=100, bg=box_color, bd=4, relief=relief)
    sync_frame.pack(side=tk.TOP)
    tuners.sync_tuner_butt = myButton(sync_frame, text="***  SYNC    ***", command=sync, bg='red', fg='white')
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


def paint(tk_object, bg='lightgray', fg='black', activebackground=None, activeforeground=None):
    if activebackground is None:
        activebackground = bg
    if activeforeground is None:
        activeforeground = fg
    tk_object.config(bg=bg, activebackground=activebackground, fg=fg, activeforeground=activeforeground)


def record():
    if title.get() == '<enter title>' or title.get() == '' or title.get() == 'None':
        enter_title()
    if title.get() != '<enter title>' and title.get() != '' and title.get() != 'None':
        print('sending message')
        thread = Thread(target=send_message, kwargs={'subject': title.get(), 'message': 'Starting ' + str(rec_time.get())})
        thread.start()
        rf, rr = screencast(silent=silent.get(),
                            video_grabber=video_grab.get(), video_in=video_in.get(),
                            audio_grabber=audio_grab.get(), audio_in=audio_in.get(),
                            crf=crf.get(),
                            rec_time=rec_time.get()*60.,
                            output_file=raw_path.get())
        raw_path.set(rf)  # screencast may cause null filename if fails
        new_result_ready.set(rr)
        sync()
        shutil.move(out_path.get(), target_path.get())
        if size_of(target_path.get()) > 0:
            root.lift()
            print('sending message')
            print("record:  target_path.get()=", target_path.get(), " type =", type(target_path.get()))
            if abs(length_of(target_path.get()) - rec_time.get()) < 1:
                msg = 'target ready'
                print(f"record:  actual {length_of(target_path.get())} != demand {rec_time.get()}")
            else:
                msg = 'Done but >1 min size difference'
            thread = Thread(target=send_message, kwargs={'subject': title.get(), 'message': msg})
            thread.start()
            pyautogui.press('F5')  # Attempt to exit fullscreen
            tk.messagebox.showinfo(title='Screencast', message=msg)
            update_file_paths()
        else:
            print('aborting recording....need to enter title.  Presently = ', title.get())


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


def start():
    """After 'pushing the button' check if over-writing then start countdown"""
    if size_of(target_path.get()) > 0:  # bytes
        confirmation = tk.messagebox.askyesno('query overwrite', 'Target exists:  overwrite?')
        if confirmation is False:
            print('enter different folder or title first row')
            tk.messagebox.showwarning(message='enter different folder or title first row')
            return
    start_countdown()


def start_countdown():
    """Countdown then call record()"""
    msg = 'Counting down'
    print(f"countdown {countdown_time.get()=}")
    countdown_time.set(countdown_time.get() - 1)
    counter_status.config(text=f'{msg} ({countdown_time.get()}sec)')
    if countdown_time.get() > 0:
        root.after(1000, start_countdown)
    else:
        counter.withdraw()
        thread = Thread(target=stay_awake, kwargs={'up_set_min': rec_time.get()})
        thread.start()
        record()  # if job is blocking then create start_button thread


def stay_awake(up_set_min=3.):
    """Keep computer awake using shift key when recording then return to previous state"""

    # Timer starts
    start_time = float(time.time())
    up_time_min = 0.0
    # FAILSAFE to FALSE feature is enabled by default so that you can easily stop execution of
    # your pyautogui program by manually moving the mouse to the upper left corner of the screen.
    # Once the mouse is in this location, pyautogui will throw an exception and exit.
    pyautogui.FAILSAFE = False
    while True and (up_time_min < up_set_min):
        time.sleep(30.)
        for i in range(0, 3):
            pyautogui.press('shift')  # Shift key does not disturb fullscreen
        up_time_min = (time.time() - start_time) / 60.
        print(f"stay_awake: {up_time_min=}")
    print(f"stay_awake: ending")
        
        
def sync():
    if size_of(raw_path.get()) > 0:
        if video_delay.get() >= 0.0:
            delay_video_sync(silent=silent.get(), delay=video_delay.get(), input_file=raw_path.get(),
                             output_file=out_path.get())
        else:
            delay_audio_sync(silent=silent.get(), delay=-video_delay.get(), input_file=raw_path.get(),
                             output_file=out_path.get())
        update_file_paths()
    else:
        print("record first *******")


def sync_clip():
    if size_of(raw_clip_path.get()) > 0:
        if video_delay.get() >= 0.0:
            delay_video_sync(silent=silent.get(), delay=video_delay.get(), input_file=raw_clip_path.get(),
                             output_file=os.path.join(os.getcwd(), clip_path.get()))
        else:
            delay_audio_sync(silent=silent.get(), delay=-video_delay.get(), input_file=raw_clip_path.get(),
                             output_file=os.path.join(os.getcwd(), clip_path.get()))
        update_file_paths()
    else:
        print("record first *******")


def update_file_paths():
    """Use 'title' and 'folder' to set paths of all files used"""
    if title.get() == '' or title.get() == '<enter title>':
        paint(title_butt, bg='pink')
    else:
        paint(title_butt, bg=bg_color)
    out_file.set(title.get()+'.mkv')
    if os.path.exists(folder.get()):
        paint(folder_butt, bg='lightgreen')
    else:
        paint(folder_butt, bg='pink')
    out_path.set(os.path.join(folder.get(), out_file.get()))
    new_target_path = os.path.join(destination_folder.get(), out_file.get())
    if new_target_path != target_path.get():
        target_path.set(new_target_path)
    if size_of(target_path.get()) > 0:
        paint(title_butt, bg='yellow')
    else:
        paint(title_butt, bg=bg_color)
    if os.path.exists(destination_folder.get()):
        paint(destination_folder_butt, bg='lightgreen')
    else:
        paint(destination_folder_butt, bg='pink')
    raw_file.set(title.get() + '_raw.mkv')
    raw_path.set(os.path.join(folder.get(), raw_file.get()))
    if size_of(raw_path.get()) > 0:
        paint(raw_path_label, bg='yellow')
        paint(tuners.raw_path_label, bg='yellow')
    else:
        paint(raw_path_label, bg=bg_color)
        paint(tuners.raw_path_label, bg=bg_color)
    raw_clip_file.set(title.get() + '_clip_raw.mkv')
    raw_clip_path.set(os.path.join(folder.get(), raw_clip_file.get()))
    if size_of(raw_clip_path.get()) > 0:
        paint(tuners.raw_clip_file_label, bg='yellow')
    else:
        paint(tuners.raw_clip_file_label, bg=bg_color)
    if size_of(clip_path.get()) > 0:
        paint(tuners.clip_path_label, bg='yellow')
    else:
        paint(tuners.clip_path_label, bg=bg_color)
    clip_file.set(title.get() + '_clip.mkv')
    clip_path.set(os.path.join(folder.get(), clip_file.get()))


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
                            "video_delay": '0.0'},
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
    countdown_time = tk.IntVar(root, 8)
    tuners = Global(root)
    script_loc = os.path.dirname(os.path.abspath(__file__))
    cwd_path = tk.StringVar(root, os.getcwd())
    folder = tk.StringVar(root, cf[SYS]['folder'])
    destination_folder = tk.StringVar(root, cf[SYS]['destination_folder'])
    title = tk.StringVar(root, cf[SYS]['title'])
    rec_time = tk.DoubleVar(root, float(cf[SYS]['rec_time']))
    crf = tk.IntVar(root, int(cf[SYS]['crf']))
    video_grab = tk.StringVar(root, cf[SYS]['video_grab'])
    video_in = tk.StringVar(root, cf[SYS]['video_in'])
    audio_grab = tk.StringVar(root, cf[SYS]['audio_grab'])
    audio_in = tk.StringVar(root, cf[SYS]['audio_in'])
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
    out_file = tk.StringVar(root)
    out_path = tk.StringVar(root)
    target_path = tk.StringVar(root)
    raw_file = tk.StringVar(root)
    raw_path = tk.StringVar(root)
    raw_clip_file = tk.StringVar(root)
    raw_clip_path = tk.StringVar(root)
    clip_file = tk.StringVar(root)
    clip_path = tk.StringVar(root)

    # Pre-define so update_file_paths() works
    title_butt = myButton()
    folder_butt = myButton()
    raw_path_label = tk.Label()
    destination_folder_butt = myButton()
    update_file_paths()

    # raw_path = tk.StringVar(root, raw_path.get())
    new_result_ready = tk.BooleanVar(root, size_of(out_path.get()) > 0)
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
    folder_butt = myButton(name_frame, text=folder.get(), command=enter_folder, fg="blue", bg=bg_color)
    working_label.pack(side='left', fill='x')
    folder_butt.pack(side="left", fill='x')
    target_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    target_frame.pack(fill='x')
    destination_label = tk.Label(target_frame, text="Target =", bg=bg_color)
    destination_folder_butt = myButton(target_frame, text=destination_folder.get(), command=enter_destination_folder, fg="blue", bg=bg_color)
    slash = tk.Label(target_frame, text="/", fg="blue", bg=bg_color)
    title_butt = myButton(target_frame, text=title.get(), command=enter_title, fg="blue", bg=bg_color)
    destination_label.pack(side="left", fill='x')
    destination_folder_butt.pack(side="left", fill='x')
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
    instructions_butt = tk.Checkbutton(silent_frame, text='instructions', bg=bg_color, variable=instructions, onvalue=True, offvalue=False)
    silent_butt.pack(side="left", fill='x')
    instructions_butt.pack(side="left", fill='x')

    # Action row
    action_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    action_frame.pack(fill='x')
    raw_path_label = tk.Label(action_frame, text=raw_path.get(), wraplength=wrap_length, justify=tk.RIGHT, bg=bg_color)
    raw_path_label.pack(side="right", fill='x')
    action_label = tk.Label(action_frame, text="Intermediate=", bg=bg_color)
    action_label.pack(side="right", fill='x')

    # Record row
    record_frame = tk.Frame(outer_frame, bd=5, bg=bg_color)
    record_frame.pack(fill='x')
    record_butt = myButton(record_frame, text='****    START      ****', command=start, fg='white', bg='red',
                           wraplength=wrap_length, justify=tk.CENTER)
    tuner_window_butt = myButton(record_frame, text="TUNER WINDOW", command=open_tuner_window, bg=bg_color)
    record_butt.pack(side="left", fill='x')
    tuner_window_butt.pack(side="right", fill='x')
    counter_status = tk.Label(counter, text="Press START to begin recording")
    counter_status.pack()

    # Begin
    handle_raw_path()
    raw_path.trace_add('write', handle_raw_path)
    handle_target_path()
    target_path.trace_add('write', handle_target_path)
    handle_silent()
    silent.trace_add('write', handle_silent)
    handle_instructions()
    instructions.trace_add('write', handle_instructions)
    handle_new_result_ready()
    new_result_ready.trace_add('write', handle_new_result_ready)
    root.mainloop()
    counter.mainloop()
    counter.withdraw()
