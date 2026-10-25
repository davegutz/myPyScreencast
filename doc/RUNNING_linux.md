# Running Linux 'myPyScreencast'
We're going to make this all run with a mouse click by creating a shortcut.

[Back to Linux INSTALL](INSTALL_linux.md)

[Back to Linux](FAQ_linux.md)

[Back to top](../README.md)

#### Before making the shortcut, try it in a shell to make sure it works.
```bash
cd ~/Documents/GitHub/myPyScreencast
python3 GUI_screencast.py
```
   - Ensure the GUI window opens properly without error.
   - Set your recording **Title**, working **Folder**, and **Destination** (Library) folder.
   - For **Wayland sessions** (e.g. KDE Plasma Wayland `DESKTOP_SESSION=plasmawayland`, GNOME), myPyScreencast automatically detects Wayland and sets the capture backend to `gpu-screen-recorder` or `wf-recorder` with video input `screen`.
   - For **X11 sessions**, it defaults to `x11grab` with `$DISPLAY`.
   - Press **RECORD** to start the recording countdown. Fullscreen video can now be played.
   - Press **STOP** when done to finalize the recording.
   - If needed, use the **Tuner** window to tune audio/video delay synchronization or clip snippets.

#### To make the shortcut do the following:
   - Browse to `myPyScreencast`.
   - Run `python3 setuplinux.py` (or `python3 install.py`).
   - You will now see a new `GUI_screencast` shortcut on the desktop.
   - Right-click on `GUI_screencast.desktop` and open with an editor if you wish to inspect or customize the paths.

```ini
[Desktop Entry]
Name=GUI_screencast
Type=Application
Path=/home/<username>/Documents/GitHub/myPyScreencast
Comment=GUI_screencast
Terminal=true
Icon=/home/<username>/Documents/GitHub/myPyScreencast/screencast.ico
Exec=/usr/bin/python3 /home/<username>/Documents/GitHub/myPyScreencast/GUI_screencast.py
```

[Back to Linux INSTALL](INSTALL_linux.md)

[Back to Linux](FAQ_linux.md)

[Back to top](../README.md)
