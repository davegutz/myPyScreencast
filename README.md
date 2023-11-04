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

## Testing
I ran the wrapped 'myPyScreencast' tool on three different laptops I have:  a MacBook Air from 2015, a gaming HP OMEN running Windows 11 from 2022, and a tiny Lenovo running Linux from 2022.

## Recommendations
1. Use the Linux and Windows versions only.  TODO: The macOS version stutters. 

## License
myPyScreencast's code are released under the MIT License.
See [LICENSE](https://github.com/openai/whisper/blob/main/LICENSE) for further details.
