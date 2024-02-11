# INSTALL and run for Linux 'myPyScreencast'
[Back to Linux](FAQ_linux.md)

[Back to top](../README.md)

## INSTALL
Synopsis:  Download this repository.   Put it in Documents/GitHub folder.
Download and install ffmpeg.   Download and install python3.10.10 if at least 3.10.6 is not installed.  Use 'pip' and 'pip3' from
'python3.10' to install dependencies.

Then run 'GUI_screencast.py' using 'python3.10.'


### Download the repository [myPyScreencast](http://www.github.com/famouswriter978/myPyScreencast)
For most people it's easiest to click on the green '<> Code' box and download the '.zip' file.  Extract to Documents/GitHub.  Make that folder if you need to.  When done, there will be a folder similar to 'myPyScreencast' where 'main' refers to the Current Branch in GitHub.

If you're so inclined, use the GitHub desktop app to perform this download.  If you don't know what I'm talking about, use the method above.


### Perform a standard update to ensure dependencies are the latest
`sudo apt update && sudo apt upgrade`


### Add .local/bin to paths
Edit '.bashrc' and put the following at the bottom:

```
# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi
```
Close and reopen any terminal windows to incorporate the new PATH.   Alternatively you could run in any open terminal:
`. ~/.bashrc`


### Install python3
'python3.10.6' is what I used to develop these instructions.  I tried to use venv in PyCharm but the pyCharm manager would not install 'openai-whisper'.

1. See what you have:  `python3`   It will say which version in the first line.  You need 3.10 or greater.  Known to work with 3.10.6 and 3.10.10.  Type `ctrl-z` and possibly `ENTER` to exit the python shell.
2. Go to the [python website](https://www.python.org/downloads/) and get what you need.  Install as instructed.


### Install the dependencies using 'pip'
Open a terminal (Launchpad - terminal) and run the following as yourself no matter where it opens to

```
# Try this
python3 -m pip install --upgrade pip

# If pip not found then do this
sudo apt install python3-pip
python3 -m pip install --upgrade pip

# Continue with these dependencies

python3 -m pip install pyshortcuts
python3 -m pip install pydub
python3 -m pip install pvrecorder
python3 -m pip install ttwidgets
. ~/.bashrc
sudo apt install ffmpeg
```

### Running:  [here](RUNNING_linux.md)

# Running
We're going to make this all run with a mouse click by creating a shortcut.

#### Before making the shortcut, try it in a shell to make sure it works.
``` commandline
cd Documents/GitHub/myPyScreencast
python3 GUI_screencast.py
```
   - Ensure there are no failures in the checks.  You will know it has passed if it pops up a file selection box
   - Select one of the test files that came with 'myPyScreencast.'  The file 'FGP_160kbps_m4a.m4a' file is a good, short choice.
   - Select a model.  'tiny.en' is a good quick test.  'small.en' gives very good results for your normal use later.
   - You should see text streaming:   '<time stamp> Title, flying goat pose'
   - Let it run to confirm a text editor 'notepad' process opens with the transcribed text.   Sometimes this opens below other windows so check the taskbar for notepad processes.
   - Click in the run window 'GUI_screencast.py - Shortcut' and press 'enter' when you're ready to close the run window
   - You will be copying from this type of 'notepad' window into your writing!

#### To make the shortcut do the following:
   - Browse to 'myPyScreencast.'
   - run `python3 setuplinux.py`
   - You will now see a new file 'GUI_screencast' shortcut on the desktop
   - Right-click on 'GUI_screencast' and open with an editor.  It will look something like, with your username in place of '<user>'.
        [GUI_screencast.desktop](../GUI_screencast.desktop)
   - Change the 'Path' line to something more useful, so it opens to where your recordings are:
`Path=/home/<username>/Documents/GitHub/myPyScreencast`

   - If you want, make life easier by adding 'small.en' after the 'Target:' data to force it to always run the excellent small model without having to select it everytime the program runs

   - 'Exec=/usr/bin/python3.10 /home/<username>/Documents/GitHub/myPyScreencast/GUI_screencast.py small.en'

### Special Developer Instructions:  [here](DEVELOPER.md)

[Back to Linux](FAQ_linux.md)

[Back to top](../README.md)
