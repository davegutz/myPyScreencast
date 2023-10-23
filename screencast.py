#  Prototype cli interface that feeds .wav file to whisper and transcribes it to .pdf
#  Run in PyCharm
#     or
#  'python3 whisper_to_write.py
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
import time
import timeit
import platform
import tkinter as tk
from screencast_util import *
from tkinter import filedialog, messagebox
os.environ['PYTHONIOENCODING'] = 'utf - 8'  # prevents UnicodeEncodeError: 'charmap' codec can't encode character


# Delay audio to sync with video
def delay_audio_sync(delay=0.0, input_file=None, output_file=None, silent=True):
    print(f"{delay=} {input_file=} {output_file=} {silent=}")

    # Initialization
    result_ready = False

    # arg2 = 'ffmpeg -i output.mkv -itsoffset 1.0 -i output.mkv -c:a copy -c:v copy -map 0:a:0 -map 1:v:0 -y output_sync.mkv'

    command = ("ffmpeg -i {:s}".format(input_file) +
               " -itsoffset {:5.3f}".format(delay) +
               " -i {:s}".format(input_file) +
               ' -c:v copy -map 0:v:0 -map 1:a:0 ' +
               " -y {:s}".format(output_file))

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


# Delay video to sync with audio
def delay_video_sync(delay=0.0, input_file=None, output_file=None, silent=True):
    print(f"{delay=} {input_file=} {output_file=} {silent=}")

    # Initialization
    result_ready = False

    # arg2 = 'ffmpeg -i output.mkv -itsoffset 1.0 -i output.mkv -c:a copy -c:v copy -map 0:a:0 -map 1:v:0 -y output_sync.mkv'

    command = ("ffmpeg -i {:s}".format(input_file) +
               " -itsoffset {:5.3f}".format(delay) +
               " -i {:s}".format(input_file) +
               ' -c:v copy -map 0:a:0 -map 1:v:0 ' +
               " -y {:s}".format(output_file))

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
        result_ready = True
        print(Colors.fg.orange, "  The synchronized result is in ", Colors.fg.blue, output_file, Colors.reset)
    else:
        result = run_shell_cmd(command, silent=silent)
        if result == -1:
            return result_ready, False
        result_ready = True


# Wrap the ffmpeg program to make it useful and more portable
def screencast(waiting=False, silent=True, conversation=False, frame_rate=30, duration=30.,
               video_in="desktop",
               audio_in="CABLE Output (VB-Audio Virtual Cable)",
               output_file=None,
               crf=28, rec_time=None):
    print(f"{waiting=} {silent=} {conversation=} {frame_rate=} {duration=} {video_in=} {audio_in=} {output_file=} \
{crf=} {rec_time=}")
    # Initialization
    result_ready = False

    if check_install(platform.system()) != 0:
        print(Colors.fg.red, 'Installation problems.   See suggestions a few lines above')
        # Ask for input to force hold to see stderr
        if silent is False and waiting is True:
            input('\nEnter anything to close window')
        return result_ready, None

    # Screencast
    command = ('ffmpeg -f gdigrab -threads 4' +
               " -r {:d} -framerate {:d}".format(frame_rate, frame_rate) +
               ' -i "{:s}"'.format(video_in) +
               ' -f dshow -i audio="{:s}"'.format(audio_in) +
               ' -vcodec libx265' +
               " -crf {:d}".format(crf) +
               ' -qp 0 -y' +
               " -t {:5.1f} ".format(rec_time) +
               output_file)
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
            duration = 2
        if sync_delay != '':
            print("user requested sync delay '{:s}'".format(sync_delay))
        else:
            sync_delay = 1.0
        raw_file, result_ready = screencast(rec_time=duration, silent=False, output_file=os.path.join(os.getcwd(), 'screencast.mkv'))
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
