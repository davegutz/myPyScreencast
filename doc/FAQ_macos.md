# FAQ for macOS myPyScreencast
[Back to myPyScreencast](../README.md)

## How do I install?
Synopsis:  Download this repository.   Put it in Documents/GitHub folder.
Download and install ffmpeg.   Download and install python3.10.10.  Use 'pip' and 'pip3' from
'python3.10' to install dependencies.  
Start Google Drive if installed.  Then run 'GUI_screencast.py' using 'python3.10.'

Details:  [INSTALL macOS](INSTALL_macos.md).


## Running it:  how?
You can run it two ways from easiest to hardest:
1. Shortcut that points to `python3 GUI_screencast.py`.  Runs multiple files - only mouse clicks, truly.
2. From a terminal as `python3 GUI_screencast.py`.   Of course, you'll have to type the full path or start from the folder by 'cd' first.  Runs multiple files

The first run creates a preferences file 'GUI_screencast.pref' in the folder where the audio files are.   You may edit this to change the AI model.   There is a balance between accuracy and speed.

The first run with a new model also loads the model into your '$HOME/.cache' folder.

## FAQ

### Shortcut:  how do I make one?
Browse to the folder with GUI_screencast.py in it.  right-click on GUI_screencast.py, select Other, click Create Shortcut.   Move the
resulting file to your desktop or wherever you want it.

### ffmpeg not found
Installation of ffmpeg is difficult, for some reason.   There is path mangling and some code calls the executable and other calls native python.   The following usually resets everything and fixes it.
```commandline
python3 -m pip uninstall ffmpeg
python3 -m pip uninstall ffmpeg-python
pip uninstall ffmpeg-python
pip uninstall ffmpeg
brew uninstall ffmpeg
python3 -m pip install ffmpeg-python
brew install ffmpeg
```
### Audio stutters

This happens on the 2015 (8 year-old) MacBook Air I developed on.  It improved when I downgraded ffmpeg to 4.2.3.

You can grab a prebuilt 4.2 Mac binary from https://evermeet.cx/pub/ffmpeg/ffmpeg-4.2.3.zip (it's linked from https://ffmpeg.org/download.html#build-mac)

Once it's in the download folder, unzip it then
```commandline
mv ffmpeg ffmpeg423
sudo cp ffmpeg423 /opt/local/bin
```

Now browse to it using Finder.  Right-click and select 'Open' - OK to register it as safe.

The line in screencast.py should look like
```commandline
command = .... # Darwin
```
should point to ffmpeg423.

[Back to top](../README.md)

