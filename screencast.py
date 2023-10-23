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


# Wrap the openai Whisper program to make it useful and more portable
def screencast(path_in=None, waiting=True, silent=True, conversation=False, frame_rate=30,
               audio_in="CABLE Output (VB-Audio Virtual Cable)",
               crf=28, rec_time=None):
    print(f"{path_in=} {path_in=} {waiting=} {silent=} {conversation=} {crf=}")
    # Initialization
    result_ready = False
    if path_in is None:
        filepaths = None
    else:
        filepaths = [path_in]

    if check_install(platform.system()) != 0:
        print(Colors.fg.red, 'Installation problems.   See suggestions a few lines above')
        # Ask for input to force hold to see stderr
        if silent is False and waiting is True:
            input('\nEnter anything to close window')
        return None, None

    # Screencast
    command = ('ffmpeg -f gdigrab -threads 4 ' +
               "-r {:d2} -framerate {:d2}".format(frame_rate, frame_rate) +
               ' -i desktop -f dshow -i ' +
               ' audio=' + audio_in +
               ' -vcodec libx265 ' +
               "-crf {:2d}".format(crf) +
               '-qp 0 -y -t 30 output.mkv')
    start_time = timeit.default_timer()
    if silent is False:
        print(command + '\n')
        writer = get_writer('txt', path)
        wh_model = whisper.load_model(model, device=device, download_root=cache_path)
        print(Colors.bg.brightblack, Colors.fg.wheat)
        result = whisper.transcribe(wh_model, filepath, temperature=0.0, fp16=False, verbose=True)
        print(Colors.reset)
        print(command + '\n')
        if result == -1:
            print(Colors.fg.blue, 'failed...on to next file', Colors.reset)
            continue
        print(Colors.fg.orange, 'Transcribed in {:6.1f} seconds.'.format(timeit.default_timer() - start_time),
              Colors.reset, end='')
        # Save the result in a text file and display it for pasting to writing documents
        #            writer and writer_args are defined in openai-whisper/transcribe.py
        writer_args = {'highlight_words': False, 'max_line_count': None, 'max_line_width': None}
        writer(result, txt_path, writer_args)
        result_ready = True
        print(Colors.fg.orange, "  The result is in ", Colors.fg.blue, txt_path, Colors.reset)
    else:
        writer = get_writer('txt', path)
        wh_model = whisper.load_model(model, device=device, download_root=cache_path)
        result = whisper.transcribe(wh_model, filepath, temperature=0.0, fp16=False, verbose=True)
        if result == -1:
            continue
        # Save the result in a text file and display it for pasting to writing documents
        #            writer and writer_args are defined in openai-whisper/transcribe.py
        writer_args = {'highlight_words': False, 'max_line_count': None, 'max_line_width': None}
        writer(result, txt_path, writer_args)
        result_ready = True

    print('')
    display_result(txt_path, platform.system(), silent, conversation=conversation)

    # Delay a little to allow windows to pop up without hiding each other.
    # The slower the computer, the more needed.
    time.sleep(1.0)

    # After all files are processed, ask for input to force hold to see stdout
    if waiting is True:
        if silent is False:
            input('\nEnter anything to close window')
        else:
            messagebox.showinfo(title='openAI whisper', message='files ready')

    return txt_path, result_ready


if __name__ == '__main__':
    def main(model=''):
        if model != '':
            print("user requested model '{:s}'".format(model))
        screencast(model=model)

    # Main call
    # windows cli run from location of screencast.py:   python .\screencast.py base "silent=True"
    # windows shortcut:  Target:    C:\Users\<user>\Documents\GitHub\myPyScreencast\screencast.py base "silent=True"
    #                    Start in:  C:\Users\<user>\Documents\GitHub\myPyScreencast
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main()
