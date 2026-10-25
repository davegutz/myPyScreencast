# FAQ for linux myPyScreencast
[Back to myPyScreencast](../README.md)

## How do I install?
Synopsis: Download this repository. Put it in `Documents/GitHub` folder.
Download and install ffmpeg (and a Wayland recorder if on Wayland). Install python3 (3.10+). Use `pip` to install dependencies.

Details: [INSTALL_linux](INSTALL_linux.md).

## Running it: how?
You can run it two ways:
1. Desktop shortcut created with `python3 setuplinux.py` or `python3 install.py`.
2. From a terminal:
   ```bash
   cd ~/Documents/GitHub/myPyScreencast
   python3 GUI_screencast.py
   ```

The first run creates a configuration file (`~/.local/GUI_screencast_linux.ini`) storing your folder paths, recorder options, and sync settings.

## Shortcut: how do I make one?
Run `python3 setuplinux.py` or `python3 install.py` from the `myPyScreencast` folder to generate the `.desktop` launcher.

## Display: what do I set?
You do **not** need to switch your Linux session to X11. Both X11 and Wayland sessions are supported out-of-the-box.

* **Wayland sessions:**
  GUI_screencast automatically detects Wayland (`WAYLAND_DISPLAY` or `XDG_SESSION_TYPE=wayland`). Screen capture on Wayland uses a dedicated Wayland capture utility:
  * `gpu-screen-recorder` (recommended for KDE Plasma, GNOME, and hardware-accelerated capture):
    Set Video grabber to `gpu-screen-recorder` and target to `screen`.
    *Working Example:* Tested and verified on modern KDE Plasma on Wayland (`DESKTOP_SESSION=plasmawayland`). While KDE Plasma historically ran natively under X11, Wayland is fully supported.
  * `wf-recorder` (for wlroots/sway/hyprland or as an apt alternative):
    `sudo apt install wf-recorder`. Set Video grabber to `wf-recorder` and target to `screen`.

* **X11 sessions:**
  * Workstation: `:0.0+0,0`
  * Laptop: `$DISPLAY` in the second box on the 'Video' line with grabber `x11grab`.

[Back to top](../README.md)
