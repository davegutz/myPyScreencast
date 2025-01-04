# Develop methods

#ffmpeg -threads 4 -f x11grab -probesize 42M -thr ead_queue_size 1024 -i $DISPLAY \
# -f pulse -thread_queue_size 1024 -i alsa_output.platform-snd_aloop.0.analog-stereo.monitor \
# -vcodec libx264  -pix_fmt yuv420p -crf 29 -t  60.0 -y  "/home/daveg/Videos/test_raw.mp4"

import ffmpeg
display = ':1'
audio = 'alsa_output.platform-snd_aloop.0.analog-stereo.monitor'
vcodec = 'libx264'
ffmpeg.input(display, f='x11grab', i=audio, codec=

ffmpeg.input("input.mp4", ss=start_time, to=end_time)
ffmpeg.input("input.mp4", ss="00:00:15")
	.filter('thumbnail')
	.filter('thumbnail', n=300)
	.output("thumbnail_filter_2.png")
	.output('frame_%d.png', vframes=3)
	.output('frame%d.png', vf='fps=1')
    .output('audio.mp3', acodec='libshine')
    .output('frame%d.png', vf='fps=1')
    .run()
