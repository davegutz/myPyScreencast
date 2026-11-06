# myPyScreencast for FWG
![icon](screencast.png)
myPyScreencast is a wrap of FFmpeg, an old Linux A/V translater.   I attempt to make it a one-click process, so you can concentrate on your binge-watching.  By using the totally portable FFmpeg program it is possible to run seamlessly on any platform (not phones). This solves the problems of system instability caused by installing freeware.

Phones are not capable now of running these tools.   This is a matter of practicality.   I'm sure in ten years the average phone will transcribe real time.  This tool is a stop gap.

For installation, you either use GitHub desktop app to install or you click on the green '<> Code' box above to download a zip file (easiest).  [source](https://github.com/davegutz/myPyScreencast).   Move into the folder 'Documents/GitHub'

# There are instructions for each platform
Before going there, download the source code now because it's right at the top of this page:  click on the green box titled '<> Code' and 'Download ZIP' file.   Of course, you should skip this step if planning to use the 'GitHub Desktop App'.  Coming back here and locating the download will be difficult later and easy now.   The installation will explain what to do with the '.zip' file.

[macOS](doc/FAQ_macos.md)

[Windows](doc/FAQ_windows.md)

[Linux](doc/FAQ_linux.md)

# There are special developer instructions if desired
[Special Developer Instructions](doc/DEVELOPER.md)

## Approach

We're wrapping an existing tool (FFmpeg) that works on all platforms to make it easy for non-tech people to use.  After installation, only mouse clicks are required to enjoy using it.

### Linux Display Server Support (X11 & Wayland)
myPyScreencast supports both **X11** and **Wayland** display servers on Linux:
- Users do **not** need to use X11 or switch session types.
- Modern desktop environments using Wayland (such as KDE Plasma Wayland or GNOME) are automatically detected and supported via high-performance Wayland capture backends like `gpu-screen-recorder` or `wf-recorder`.
- For X11 desktop sessions, native FFmpeg (`x11grab`) capture is used.

#### Wayland Video Input Options: `screen` vs. `portal`
On Wayland with `gpu-screen-recorder`, you can set the `Video in` parameter to either `screen` or `portal`:

> **Preference for HP OMEN / CachyOS (COSMIC Desktop):**
> On hybrid-GPU laptops like the **HP OMEN** (AMD Cezanne iGPU + NVIDIA RTX 3070 Mobile) running **CachyOS with COSMIC desktop (`cosmic-comp`)**, **`portal` is strongly preferred**.
> Direct KMS display-plane capture (`screen`) accesses hardware DRM buffers on the shared AMD GPU (`/dev/dri/card2`) outside the compositor, leaving `cosmic-comp`'s atomic modesetting state out of sync. This can cause the Linux kernel to hang in uninterruptible sleep (`drm_modeset_lock` freeze timeout) during subsequent system sleep or suspend. Capturing via **`portal`** routes through `xdg-desktop-portal-cosmic` and PipeWire, avoiding direct KMS hardware contention and allowing automatic sleep/suspend to function without issue.

- **`screen` (Best for standard unattended movie recording on single-GPU/KDE/GNOME):**
  - **Pros:**
    - Fully automated: Starts instantly after the countdown with zero prompts or user interaction.
    - Captures directly from hardware KMS/DRM display buffers with maximum performance and no dropped frames.
    - Most reliable for walk-away recording of fullscreen media.
  - **Cons:**
    - Captures the entire monitor: any overlapping windows, mouse movements, or desktop notifications will be recorded.
    - Requires dedicating the display to the video being recorded.

- **`portal` (Recommended for background recording while multitasking):**
  - **Pros:**
    - Window-specific capture: Uses `xdg-desktop-portal` with PipeWire to record **only** a chosen application window (e.g. your browser or media player).
    - You can freely work in other windows, place windows over the player, or switch virtual desktops without them appearing in the recording.
    - Combined with per-app audio routing (directing only the movie player to the loopback device), the movie records silently in the background while you continue working.
    - Automatically restores previous session tokens (`-restore-portal-session yes`) so you don't have to re-select the window on subsequent runs.
    - Smooth 60 fps sampling avoiding uneven browser compositor frame timing or variable framerate judder.
  - **Cons:**
    - Interactive authorization: On first launch, your desktop environment pops up a permission dialog to choose which window or screen to share. If this prompt is not approved, recording cannot begin.
    - Background rendering throttling: If the movie window is completely minimized to the panel, web browsers may throttle frame rate or pause playback to save power. (Best practice: keep the window open on another virtual desktop rather than minimizing it).
    - Same-app audio sharing: If you play audio in other tabs of the same browser instance, that sound may also route to the loopback sink. Use a separate browser for your foreground work.

## Testing
I ran the wrapped 'myPyScreencast' tool on three different laptops I have:  a MacBook Air from 2015, a gaming HP OMEN running Windows 11 from 2022, and a tiny Lenovo running Linux from 2022.

*Linux testing note:* Tested and verified working on:
- Modern KDE Plasma on Wayland (`DESKTOP_SESSION=plasmawayland`) with `gpu-screen-recorder`.
- **HP OMEN (AMD Cezanne + NVIDIA RTX 3070 Mobile) on CachyOS with COSMIC desktop (`cosmic-comp`)** using `gpu-screen-recorder` and `portal` mode.

## Recommendations
1. Use the Linux and Windows versions only.  TODO: The macOS version stutters. 

## License
myPyScreencast's code are released under the MIT License.
