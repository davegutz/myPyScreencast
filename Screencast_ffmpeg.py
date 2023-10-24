
# install uscreen https://www.nerdlogger.com/2011/11/03/stream-your-windows-desktop-using-ffmpeg/
# install ffmpeg

import os
# import time

# view sources
# ffmpeg -list_devices true -f dshow -i dummy'

# linux
# pactl list sources
# ffmpeg -f pulse -i default /tmp/pulse.wav
# xwininfo  # last line feeds into following, for a selected window
# ffmpeg -f x11grab -video_size 1530x900 -framerate 30 -i :0.0+0,0 -vf format=yuv420p output.mp4
# full screen
# xdpyinfo | grep 'dimensions:'
# ffmpeg -f x11grab -video_size 1600x900 -framerate 30 -i :0.0+0,0 -vf format=yuv420p output.mp4
# full screen with sound; huge and stuttery
# ffmpeg -video_size 1600x900 -framerate 30 -f x11grab -i :0.0+0,0 -f pulse -i default -c:v libx264rgb -crf 0 -preset ultrafast -y sample.mkv
#    - add threads for stutter...none of these help
# ffmpeg -video_size 1600x900 -framerate 30 -threads 4 -f x11grab -i :0.0+0,0 -f pulse -i default -c:v libx264rgb -crf 0 -preset ultrafast -y sample.mkv
# ffmpeg -video_size 1600x900 -framerate 30 -threads 4 -f x11grab -i :0.0+0,0 -f pulse -i default -c:v libx265 -crf 28 -preset ultrafast -y sample.mkv
# ffmpeg -video_size 1600x900 -framerate 30 -threads 4 -f x11grab -i :0.0+0,0 -f pulse -i default -c:v libx265 -crf 28 -y sample.mkv
# ffmpeg -video_size 1600x900 -framerate 30 -threads 4 -f x11grab -i :0.0+0,0 -f pulse -i default -vcodec libx265 -crf 28 -y sample.mkv
# hardware accel doesn't help stutter
# ffmpeg -video_size 1600x900 -framerate 30 -threads 4 -f x11grab  -hwaccel vaapi -i :0.0+0,0 -f pulse -i default -vcodec libx265 -crf 28 -y sample.mkv
# ffmpeg -video_size 1600x900 -framerate 30 -threads 4 -f x11grab -i :0.0+0,0 -f pulse -i default -vcodec libx265 -crf 28 -y sample.mkv
# maybe it's the drive backup process running at same time. need to turn that off

path_mkv = os.path.join(os.getcwd(), 'output.mkv')
if os.path.exists(path_mkv):
    os.remove(path_mkv)
# These work
# arg = 'ffmpeg -f dshow -threads 4 -r 30 -framerate 60 -video_size 1280x720 \
#     -y -i video="HP Wide Vision HD Camera":audio="CABLE Output (VB-Audio Virtual Cable)" output.mkv'
# arg = 'ffmpeg -f dshow -i video="HP Wide Vision HD Camera":audio="CABLE Output (VB-Audio Virtual Cable)" output.mkv'
# arg = 'ffmpeg -f gdigrab -framerate 30 -i desktop output.mkv'
# arg = 'ffmpeg -f gdigrab -framerate 24 -i desktop -c:v h264_nvenc -qp 0 output.mkv'

# following slow frame rate ~1 /s.  even when raw in desktop
# arg = 'ffmpeg -f gdigrab -framerate 24 -i desktop -f dshow -i audio="CABLE Output (VB-Audio Virtual Cable)" -c:v h264_nvenc -qp 0 output.mkv'
# arg = 'ffmpeg -f gdigrab -framerate 24 -i desktop -f dshow -i audio="CABLE Output (VB-Audio Virtual Cable)" output.mkv'
# arg = 'ffmpeg -f gdigrab -framerate 24 -i desktop -f dshow -i audio="CABLE Output (VB-Audio Virtual Cable)" -c:v h264_nvenc -qp 0 -preset ultrafast output.mkv'
# followig huge
# arg = 'ffmpeg -f gdigrab -threads 4 -r 30 -framerate 30 -i desktop -f dshow -i audio="CABLE Output (VB-Audio Virtual Cable)" -c:v h264_nvenc -qp 0 output.mkv'
# didn't help
# arg = 'ffmpeg -f gdigrab -threads 4 -r 30 -framerate 30 -i desktop -f dshow -i audio="CABLE Output (VB-Audio Virtual Cable)" -c:v libx265 -qp 0 -y output.mkv'
# this is good
#arg = 'ffmpeg -f gdigrab -threads 4 -r 30 -framerate 30 -i desktop -f dshow -i audio="CABLE Output (VB-Audio Virtual Cable)" -vcodec libx265 -crf 28 -qp 0 -y output.mkv'
# add time limit
arg = 'ffmpeg -f gdigrab -threads 4 -r 30 -framerate 30 -i desktop -f dshow -i audio="CABLE Output (VB-Audio Virtual Cable)" -vcodec libx265 -crf 28 -qp 0 -y -t 30 output.mkv'

# doesn't work
# arg = 'ffmpeg -f gdigrab -threads 4 -r 30 -framerate 30 -i desktop -f dshow -itsoffset 2.0 -i audio="CABLE Output (VB-Audio Virtual Cable)" -c:v h264_nvenc -qp 0 output.mkv'

os.system(arg)

# audio ahead
# ffmpeg -i file.mkv -itsoffset 3 -i file.mkv -c:a copy -c:v copy -map 0:v:0 -map 1:a:0 out.mkv
# audio behind
# 'ffmpeg -i file.mkv -itsoffset 3 -i file.mkv -c:a copy -c:v copy -map 0:a:0 -map 1:v:0 out.mkv'
# arg2 = 'ffmpeg -i output.mkv -itsoffset 00:00:0.6 -i output.mkv -c:a copy -c:v copy -map 0:v:0 -map 1:a:0 -y output_sync.mkv'
arg2 = 'ffmpeg -i output.mkv -itsoffset 1.0 -i output.mkv -c:a copy -c:v copy -map 0:a:0 -map 1:v:0 -y output_sync.mkv'
os.system(arg2)
# arg3 = 'ffmpeg -i output_sync.mkv -filter:v scale=960:540 -c:a copy -y output_sync_scale.mkv'
# os.system(arg3)
# arg4 = 'ffmpeg -i output_sync.mkv -filter:v scale=1920:1080 -c:a copy -y output_sync_scale.mkv'
# os.system(arg4)



# time.sleep(5.0)
# os.system('taskkill /im ffmpeg.exe /t /f')
