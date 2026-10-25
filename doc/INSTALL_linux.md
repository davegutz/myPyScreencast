# INSTALL and run for Linux 'myPyScreencast'
[Back to Linux](FAQ_linux.md)

[Back to top](../README.md)

## INSTALL
Synopsis: Download this repository. Put it in `Documents/GitHub` folder.
Download and install ffmpeg and (if on Wayland) a Wayland screen recorder backend. Install python3 (3.10 or greater). Use `pip` to install dependencies.

Then run `GUI_screencast.py` using `python3`.

### Download the repository [myPyScreencast](http://www.github.com/davegutz/myPyScreencast)
For most people it's easiest to click on the green '<> Code' box and download the '.zip' file. Extract to `Documents/GitHub`. Make that folder if you need to. When done, there will be a folder named `myPyScreencast`.

If you're so inclined, use git or GitHub Desktop:
```bash
cd ~/Documents/GitHub
git clone https://github.com/davegutz/myPyScreencast.git
```

### Perform a standard update to ensure dependencies are the latest
`sudo apt update && sudo apt upgrade`

### Add .local/bin to paths
Edit `.bashrc` and put the following at the bottom if not already present:

```bash
# set PATH so it includes user's private bin if it exists
if [ -d "$HOME/bin" ] ; then
    PATH="$HOME/bin:$PATH"
fi

if [ -d "$HOME/.local/bin" ] ; then
    PATH="$HOME/.local/bin:$PATH"
fi
```
Close and reopen any terminal windows to incorporate the new PATH, or run:
`. ~/.bashrc`

### Install python3
1. See what you have: `python3 --version`. You need Python 3.10 or greater.
2. If needed:
   `sudo apt install python3 python3-pip python3-tk`

### Install the dependencies using 'pip'
Open a terminal and run:

```bash
python3 -m pip install --upgrade pip

# Dependencies
python3 -m pip install pyshortcuts
python3 -m pip install pydub
python3 -m pip install pvrecorder
python3 -m pip install ttwidgets
python3 -m pip install evdev pyperclip
```

### Screen Capture Backends (X11 & Wayland)
myPyScreencast supports both **X11** and **Wayland** display servers. You do **not** need to switch to an X11 session.

- **FFmpeg (Required for both X11 and Wayland audio/video processing):**
  ```bash
  sudo apt install ffmpeg
  ```

- **Wayland Sessions (e.g. KDE Plasma Wayland `DESKTOP_SESSION=plasmawayland`, GNOME Wayland):**
  GUI_screencast automatically detects Wayland sessions and uses a Wayland-native screen recorder backend. Install either of the following:
  - **`gpu-screen-recorder`** (recommended for KDE Plasma, GNOME, and hardware-accelerated capture):
    Install via Flatpak:
    ```bash
    flatpak install flathub com.dec05eba.gpu_screen_recorder
    ```
    Or compile/install natively from [git.dec05eba.com/gpu-screen-recorder](https://git.dec05eba.com/gpu-screen-recorder).
    *(Verified working configuration: KDE Plasma on Wayland with `DESKTOP_SESSION=plasmawayland` using `gpu-screen-recorder`).*
  - **`wf-recorder`** (easy install via apt, works great on wlroots/sway/hyprland or as an alternative):
    ```bash
    sudo apt install wf-recorder
    ```

- **X11 Sessions:**
  Standard FFmpeg with `x11grab` is used. While older KDE Plasma natively ran under X11, modern Plasma on Wayland is fully supported out of the box.

---

# Running
We're going to make this all run with a mouse click by creating a shortcut.

#### Before making the shortcut, try it in a shell to make sure it works.
```bash
cd ~/Documents/GitHub/myPyScreencast
python3 GUI_screencast.py
```
   - Ensure the GUI window opens without errors.
   - Check the title, recordings folder, and destination folder buttons.
   - On Wayland, the backend will automatically be set to your installed Wayland recorder (`gpu-screen-recorder` or `wf-recorder`) with target `screen`.
   - On X11, the backend defaults to `x11grab` with target `$DISPLAY`.
   - Click 'RECORD' to verify countdown and recording, and click 'STOP' when finished.

#### To make the desktop shortcut:
   - Browse to `myPyScreencast`.
   - Run `python3 setuplinux.py` (or `python3 install.py`).
   - You will see a `GUI_screencast` shortcut on the desktop.
   - Right-click on `GUI_screencast.desktop` to inspect or customize if needed.

### Special Developer Instructions: [here](DEVELOPER.md)

[Back to Linux](FAQ_linux.md)

[Back to top](../README.md)
