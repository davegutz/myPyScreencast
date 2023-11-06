#  Prototype cli interface that feeds .wav file to myPyScreencast and transcribes it to .pdf
#  Run in PyCharm
#     or
#  'python3 GUI_screencast.py
#
#  2023-Apr-29  Dave Gutz   Create
# Copyright (C) 2023 Dave Gutz and Sarah E. Gutz
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
# See http://www.fsf.org/licensing/licenses/lgpl.txt for full license text
# import os
import time
import timeit
import platform
# import tkinter as tk
from screencast_util import *
from tkinter import messagebox
os.environ['PYTHONIOENCODING'] = 'utf - 8'  # prevents UnicodeEncodeError: 'charmap' codec can't encode character


# Cut segment out and save to file
def cut_clip(waiting=False, silent=True, conversation=False,
             raw_file=None, start_clip=0., stop_clip=0.,
             clip_file=None):

    print(f"{waiting=} {silent=} {conversation=} {raw_file=} {start_clip=} {stop_clip=} {clip_file=}")

    # Initialization
    result_ready = False

    command = ('ffmpeg -i "{:s}"'.format(raw_file) +
               " -ss {:5.2f}".format(start_clip) +
               " -to {:5.2f}".format(stop_clip) +
               ' -acodec copy -y "{:s}"'.format(clip_file))

    start_time = timeit.default_timer()
    if silent is False:
        print(command + '\n')
        print(Colors.bg.brightblack, Colors.fg.wheat)
        result = run_shell_cmd(command, silent=silent)
        print(Colors.reset)
        print(command + '\n')
        if result == -1:
            print(Colors.fg.blue, 'failed.', Colors.reset)
            return None, False
        print(Colors.fg.orange, 'Recorded for {:6.1f} seconds.'.format(timeit.default_timer() - start_time),
              Colors.reset, end='')
        result_ready = True
        print(Colors.fg.orange, "  The result is in ", Colors.fg.blue, clip_file, Colors.reset)
    else:
        result = run_shell_cmd(command, silent=silent)
        if result == -1:
            return result_ready, False
        result_ready = True

    print('')
    display_result(clip_file, platform.system(), silent, conversation=conversation)

    # Delay a little to allow windows to pop up without hiding each other.
    # The slower the computer, the more needed.
    time.sleep(1.0)

    # After all files are processed, ask for input to force hold to see stdout
    if waiting is True:
        if silent is False:
            input('\nEnter anything to close window')
        else:
            messagebox.showinfo(title='screencast', message='files ready')

    return clip_file, result_ready


# Delay audio to sync with video
def delay_audio_sync(delay=0.0, input_file=None, output_file=None, silent=True):
    print(f"{delay=} {input_file=} {output_file=} {silent=}")

    # arg2 = 'ffmpeg -i output.mkv -itsoffset 1.0 -i output.mkv -c:a copy -c:v copy -map 0:a:0 -map 1:v:0 -y output_sync.mkv'

    command = ('ffmpeg -i "{:s}"'.format(input_file) +
               " -itsoffset {:5.3f}".format(delay) +
               ' -i "{:s}"'.format(input_file) +
               ' -c:v copy -map 0:v:0 -map 1:a:0 ' +
               ' -y "{:s}"'.format(output_file))

    start_time = timeit.default_timer()
    if silent is False:
        print(command + '\n')
        print(Colors.bg.brightblack, Colors.fg.wheat)
        result = run_shell_cmd(command, silent=silent)
        print(Colors.reset)
        print(command + '\n')
        if result == -1:
            print(Colors.fg.blue, 'failed.', Colors.reset)
            return None, False
        print(Colors.fg.orange, 'Recorded for {:6.1f} seconds.'.format(timeit.default_timer() - start_time),
              Colors.reset, end='')
        print(Colors.fg.orange, "  The result is in ", Colors.fg.blue, output_file, Colors.reset)
    else:
        result = run_shell_cmd(command, silent=silent)

    return result, False


# Delay video to sync with audio
def delay_video_sync(delay=0.0, input_file=None, output_file=None, silent=True):
    command = ('ffmpeg -i "{:s}"'.format(input_file) +
               " -itsoffset {:5.3f}".format(delay) +
               ' -i "{:s}"'.format(input_file) +
               ' -c:v copy -map 0:a:0 -map 1:v:0 ' +
               ' -y "{:s}"'.format(output_file))

    start_time = timeit.default_timer()
    if silent is False:
        print(command + '\n')
        print(Colors.bg.brightblack, Colors.fg.wheat)
        result = run_shell_cmd(command, silent=silent)
        print(Colors.reset)
        print(command + '\n')
        if result == -1:
            print(Colors.fg.blue, 'failed.', Colors.reset)
            return None, False
        print(Colors.fg.orange, 'Processed delay for {:6.1f} seconds.'.format(timeit.default_timer() - start_time),
              Colors.reset, end='')
        print(Colors.fg.orange, "  The synchronized result is in ", Colors.fg.blue, output_file, Colors.reset)
    else:
        result = run_shell_cmd(command, silent=silent)
    return result


# Length of a video file
def length_of(input_file: str, silent=True, save_stdout=True):

    # String together the ffmpeg command
    command = 'ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "{:s}"'.format(input_file)
    if silent is False:
        print(command + '\n')
        print(Colors.bg.brightblack, Colors.fg.wheat)
        result_str = run_shell_cmd(command, silent=silent, save_stdout=save_stdout)
        print(Colors.reset)
        print(command + '\n')
        if result_str == -1:
            record_time = 0.
            print(Colors.fg.blue, 'failed.', Colors.reset)
        else:
            record_time = float(result_str[0]) / 60.
        print(Colors.fg.orange, "  length is ", Colors.fg.blue, record_time, Colors.reset)
    else:
        result_str = run_shell_cmd(command, silent=silent, save_stdout=save_stdout)
        if result_str == -1:
            record_time = 0.
        else:
            record_time = float(result_str[0]) / 60.

    return record_time


def kill_ffmpeg(sys_=None, silent=True):
    command = ''
    if sys_ == 'Linux':
        command = 'pkill -e ffmpeg'
    elif sys_ == 'Windows':
        command = 'taskkill /f /im ffmpeg.exe'
    elif sys_ == 'Darwin':
        command = 'pkill ffmpeg'
    else:
        print(f"kill_ffmpeg: SYS = {sys_} unknown")
    if silent is False:
        print(command + '\n')
        print(Colors.bg.brightblack, Colors.fg.wheat)
        result = run_shell_cmd(command, silent=silent)
        print(Colors.reset)
        print(command + '\n')
        if result == -1:
            print(Colors.fg.blue, 'failed.', Colors.reset)
            return None, False
    else:
        result = run_shell_cmd(command, silent=silent)
    return result


def screencast(waiting=False, silent=True, conversation=False,
               video_grabber="gdigrab", video_in='desktop',
               audio_grabber="dshow", audio_in="CABLE Output (VB-Audio Virtual Cable)",
               output_file=None,
               crf=28, rec_time=None):
    """Wrap the ffmpeg program to make it useful and more portable"""

    print(f"{waiting=} {silent=} {conversation=} {video_grabber=} {video_in=} \
{audio_grabber=} {audio_in=} {output_file=} {crf=} {rec_time=}")

    # Initialization
    result_ready = False

    if check_install(platform.system()) != 0:
        print(Colors.fg.red, 'Installation problems.   See suggestions a few lines above')
        # Ask for input to force hold to see stderr
        if silent is False and waiting is True:
            input('\nEnter anything to close window')
        return result_ready, None

    # Screencast
    if audio_grabber is None or audio_grabber == '':  # Darwin
        command = ("ffmpeg423 -threads 4" +
                   " -f {:s}".format(video_grabber) +
                   " -probesize 42M" +
                   " -thread_queue_size 1024" +
                   " -i {:s}:{:s}".format(video_in, audio_in) +
                   " -vf crop=1382:814:57:82" +  # full prime opera
                   " -vcodec libx264 -crf {:d}".format(crf) +
                   " -t {:5.1f} -y ".format(rec_time) +
                   ' "{:s}"'.format(output_file))
    else:
        command = ("ffmpeg -threads 4" +
                   " -f {:s}".format(video_grabber) +
                   " -probesize 42M" +
                   " -thread_queue_size 1024" +
                   " -i {:s}".format(video_in) +
                   " -f {:s}".format(audio_grabber) +
                   " -thread_queue_size 1024" +
                   " -i {:s}".format(audio_in) +
                   " -vcodec libx264 -crf {:d}".format(crf) +
                   " -t {:5.1f} -y ".format(rec_time) +
                   ' "{:s}"'.format(output_file))

    start_time = timeit.default_timer()
    if silent is False:
        print(command + '\n')
        print(Colors.bg.brightblack, Colors.fg.wheat)
        result = run_shell_cmd(command, silent=silent)
        print(Colors.reset)
        print(command + '\n')
        if result == -1:
            print(Colors.fg.blue, 'failed.', Colors.reset)
            return None, False
        print(Colors.fg.orange, 'Recorded for {:6.1f} seconds.'.format(timeit.default_timer() - start_time),
              Colors.reset, end='')
        result_ready = True
        print(Colors.fg.orange, "  The result is in ", Colors.fg.blue, output_file, Colors.reset)
    else:
        result = run_shell_cmd(command, silent=silent)
        if result == -1:
            return result_ready, False
        result_ready = True

    print('')
    display_result(output_file, platform.system(), silent, conversation=conversation)

    # Delay a little to allow windows to pop up without hiding each other.
    # The slower the computer, the more needed.
    time.sleep(1.0)

    # After all files are processed, ask for input to force hold to see stdout
    if waiting is True:
        if silent is False:
            input('\nEnter anything to close window')
        else:
            messagebox.showinfo(title='screencast', message='files ready')

    return output_file, result_ready


if __name__ == '__main__':
    def main(duration='', sync_delay=''):
        if duration != '':
            print("user requested duration '{:s}'".format(duration))
        else:
            duration = 180

        plate = platform.system()
        if plate == 'Windows':
            video_grabber = "gdigrab"
            video_in = "desktop"
            audio_grabber = 'dshow'
            audio_in = 'audio="CABLE Output (VB-Audio Virtual Cable)"'
            crf = 28
            if sync_delay != '':
                print("user requested sync delay '{:s}'".format(sync_delay))
            else:
                sync_delay = 0.0
        elif plate == 'Linux':
            video_grabber = "x11grab"
            video_in = ":0.0+0,0"
            audio_grabber = 'pulse'
            audio_in = 'default'
            crf = 25
            if sync_delay != '':
                print("user requested sync delay '{:s}'".format(sync_delay))
            else:
                sync_delay = -0.3
        elif plate == 'Darwin':
            video_grabber = 'avfoundation'
            video_in = '1'
            audio_grabber = None
            audio_in = '2'
            crf = 25
            if sync_delay != '':
                print("user requested sync delay '{:s}'".format(sync_delay))
            else:
                sync_delay = 0.0
        else:
            print(f"unknown platform {platform}")
            exit(-1)
        # result_ready = True
        # raw_file = os.path.join(os.getcwd(), 'screencast.mkv')
        raw_file, result_ready = screencast(silent=False,
                                            video_grabber=video_grabber, video_in=video_in,
                                            audio_grabber=audio_grabber, audio_in=audio_in,
                                            crf=crf,
                                            rec_time=duration,
                                            output_file=os.path.join(os.getcwd(), 'screencast.mkv'))
        if result_ready:
            if sync_delay >= 0.0:
                delay_video_sync(silent=False, delay=sync_delay, input_file=raw_file,
                                 output_file=os.path.join(os.getcwd(), 'screencast_sync.mkv'))
            else:
                delay_audio_sync(silent=False, delay=-sync_delay, input_file=raw_file,
                                 output_file=os.path.join(os.getcwd(), 'screencast_sync.mkv'))

    # Main call
    # windows cli run from location of screencast.py:   python .\screencast.py base "silent=True"
    # windows shortcut:  Target:    C:\Users\<user>\Documents\GitHub\myPyScreencast\screencast.py base "silent=True"
    #                    Start in:  C:\Users\<user>\Documents\GitHub\myPyScreencast
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
