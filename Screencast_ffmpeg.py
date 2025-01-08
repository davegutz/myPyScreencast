# Develop methods
from fileinput import filename

#ffmpeg -threads 4 -f x11grab -probesize 42M -thread_queue_size 1024 -i $DISPLAY \
# -f pulse -thread_queue_size 1024 -i alsa_output.platform-snd_aloop.0.analog-stereo.monitor \
# -vcodec libx264  -pix_fmt yuv420p -crf 29 -t  60.0 -y  "/home/daveg/Videos/test_raw.mp4"

# ffmpeg -threads 4 -f gdigrab -probesize 42M -thread_queue_size 1024 -i desktop \
# -f dshow -thread_queue_size 1024 -i audio="CABLE Output (VB-Audio Virtual Cable)" \
# -vcodec libx264  -pix_fmt yuv420p -crf 28 -t   6.0 -y  "C:/Users/daveg/Videos\test_raw.mp4"

import ffmpeg
import sys
import os

# input
title = 'test'
def_dict = {
 'Linux': {"folder": '<enter working folder>',
           "destination_folder": '/home/daveg/Videos',
           "title": title,
           "rec_time": '0.1',
           "crf": '29',
           "video_grab": 'x11grab',
           "video_in": '$DISPLAY',
           "audio_grab": 'pulse',
           "audio_in": 'alsa_output.platform-snd_aloop.0.analog-stereo.monitor',
           "silent": '0',
           "instructions": '0',
           "video_delay": '0.5'},
 'win32': {"folder": '<enter working folder>',
             "destination_folder": 'C:\\Users\\daveg\\Videos',
             "title": title,
             "rec_time": '0.1',
             "crf": '28',
             "video_grab": "gdigrab",
             "video_in": 'desktop',
             "audio_grab": 'dshow',
             "audio_in": 'audio="CABLE Output (VB-Audio Virtual Cable)"',
             "silent": '0',
             "instructions": '0',
             "video_delay": '0.0'},
 'Darwin': {"folder": '<enter working folder>',
            "destination_folder": title,
            "title": '<enter title>',
            "rec_time": '0.1',
            "crf": '25',
            "video_grab": 'avfoundation',
            "video_in": '1',
            "audio_grab": '',
            "audio_in": '2',
            "silent": '0',
            "instructions": '0',
            "video_delay": '0.0'},
}

SYS = sys.platform

folder = def_dict[SYS]['folder']
destination_folder = def_dict[SYS]['destination_folder']
title = def_dict[SYS]['title']
rec_time = float(def_dict[SYS]['rec_time'])
crf = int(def_dict[SYS]['crf'])
video_in = def_dict[SYS]['video_in']
video_grab = def_dict[SYS]['video_grab']
audio_in = def_dict[SYS]['audio_in']
audio_grab = def_dict[SYS]['audio_grab']
video_delay = float(def_dict[SYS]['video_delay'])
vcodec = 'libx264'
pix_fmt = 'yuv420p'
target_path = os.path.join(destination_folder, title)

input_video_params = {
 'filename': video_in,
 'f': video_grab,
}

input_audio_params = {
 'filename': audio_in,
 'f': audio_grab,
}

# output
output_params = {
 'vcodec': vcodec,
 'pix_fmt': pix_fmt,
 'crf': crf,
 't': rec_time,
 'y': '',  # overwrite output files without asking
}

# Do the work
video_input = ffmpeg.input(**input_video_params)
audio_input = ffmpeg.input(**input_audio_params)
output = ffmpeg.output(video_input, audio_input, target_path, **output_params)
ffmpeg.run(output)


# ffmpeg.input(display, f='x11grab', i=audio, codec=
#
# ffmpeg.input("input.mp4", ss=start_time, to=end_time)
# ffmpeg.input("input.mp4", ss="00:00:15")
# 	.filter('thumbnail')
# 	.filter('thumbnail', n=300)
# 	.output("thumbnail_filter_2.png")
# 	.output('frame_%d.png', vframes=3)
# 	.output('frame%d.png', vf='fps=1')
#     .output('audio.mp3', acodec='libshine')
#     .output('frame%d.png', vf='fps=1')
#     .run()
# ffmpeg.__dir__()
# ['__name__', '__doc__', '__package__', '__loader__', '__spec__', '__path__', '__file__', '__cached__', '__builtins__',
#  'unicode_literals', '_utils', 'dag', 'nodes', '_ffmpeg', '_filters', '_run', '_probe', '_view', 'Stream', 'input',
#  'merge_outputs', 'output', 'overwrite_output', 'colorchannelmixer', 'concat', 'crop', 'drawbox', 'drawtext', 'filter',
#  'filter_', 'filter_multi_output', 'hflip', 'hue', 'overlay', 'setpts', 'trim', 'vflip', 'zoompan', 'probe',
#  'compile', 'Error', 'get_args', 'run', 'run_async', 'view', '__all__']
