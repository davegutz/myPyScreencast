#  install.py
#  2024-Apr-13  Dave Gutz   Create
# Copyright (C) 2024 Dave Gutz
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation;
# version 2.1 of the License.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# See http://www.fsf.org/licensing/licenses/lgpl.txt for full license text.
import sys
from screencast_util import run_shell_cmd
from Colors import Colors
import os
import shutil

test_cmd_create = None
test_cmd_copy = None

# Create executable
if sys.platform == 'linux':
    # screencast_path = os.path.join(os.getcwd(), 'screencast.png')
    # screencast_dest_path = os.path.join(os.getcwd(), 'dist', 'GUI_screencast', 'screencast.png')
    # GUI_screencast_path = os.path.join(os.getcwd(), 'GUI_screencast_Icon.png')
    # GUI_screencast_dest_path = os.path.join(os.getcwd(), 'dist', 'GUI_screencast', 'GUI_screencast.png')
    #
    # # Provide dependencies
    # shutil.copyfile(screencast_path, screencast_dest_path)
    # shutil.copystat(screencast_path, screencast_dest_path)
    # shutil.copyfile(GUI_screencast_path, GUI_screencast_dest_path)
    # shutil.copystat(GUI_screencast_path, GUI_screencast_dest_path)
    # print(Colors.fg.green, "copied files", Colors.reset)
    pass
elif sys.platform == 'win32':
    test_cmd_create = 'pyinstaller .\\GUI_screencast.py --i screencast.ico -y'
    result = run_shell_cmd(test_cmd_create, silent=False)
    if result == -1:
        print(Colors.fg.red, 'failed', Colors.reset)
        exit(1)
    else:
        print(Colors.fg.green, 'success', Colors.reset)

    # Provide dependencies
    screencast_path = os.path.join(os.getcwd(), 'screencast.png')
    screencast_dest_path = os.path.join(os.getcwd(), 'dist', 'GUI_screencast', '_internal', 'screencast.png')
    shutil.copyfile(screencast_path, screencast_dest_path)
    shutil.copystat(screencast_path, screencast_dest_path)
    GUI_screencast_path = os.path.join(os.getcwd(), 'GUI_screencast_Icon.png')
    GUI_screencast_dest_path = os.path.join(os.getcwd(), 'dist', 'GUI_screencast', '_internal', 'GUI_screencast_Icon.png')
    shutil.copyfile(GUI_screencast_path, GUI_screencast_dest_path)
    shutil.copystat(GUI_screencast_path, GUI_screencast_dest_path)
    print(Colors.fg.green, "copied files", Colors.reset)

# Install as deeply as possible
test_cmd_install = None
login = os.getlogin()
if sys.platform == 'linux':

    # Install
    desktop_entry = f"""[Desktop Entry]
Name=GUI_screencast
Exec=/home/{login}/Documents/GitHub/myPyScreencast/venv/bin/python3.12 /home/{login}/Documents/GitHub/myPyScreencast/GUI_screencast.py
Path=/home/{login}/Documents/GitHub/myPyScreencast
Icon=/home/{login}/Documents/GitHub/myPyScreencast/screencast.ico
comment=app
Type=Application
Terminal=true
Encoding=UTF-8
Categories=Utility
"""
    with open("/home/daveg/Desktop/GUI_screencast.desktop", "w") as text_file:
        result = text_file.write("%s" % desktop_entry)
    if result == -1:
        print(Colors.fg.red, 'failed', Colors.reset)
    else:
        print(Colors.fg.green, 'success', Colors.reset)

    #  Launch permission
    test_cmd_launch = 'gio set /home/daveg/Desktop/GUI_screencast.desktop metadata::trusted true'
    result = run_shell_cmd(test_cmd_launch, silent=False)
    if result == -1:
        print(Colors.fg.red, 'gio set failed', Colors.reset)
    else:
        print(Colors.fg.green, 'gio set success', Colors.reset)
    test_cmd_perm = 'chmod a+x ~/Desktop/GUI_screencast.desktop'
    result = run_shell_cmd(test_cmd_perm, silent=False)
    if result == -1:
        print(Colors.fg.red, 'failed', Colors.reset)
    else:
        print(Colors.fg.green, 'success', Colors.reset)

    # Execute permission
    test_cmd_perm = 'chmod a+x ~/Desktop/GUI_screencast.desktop'
    result = run_shell_cmd(test_cmd_perm, silent=False)
    if result != 0:
        print(Colors.fg.red, f"'chmod ...' failed code {result}", Colors.reset)
    else:
        print(Colors.fg.green, 'chmod success', Colors.reset)

    # Move file
    try:
        result = shutil.move('/home/daveg/Desktop/GUI_screencast.desktop',
                             '/usr/share/applications/GUI_screencast.desktop')
    except PermissionError:
        print(Colors.fg.red, f"Stop and establish sudo permissions", Colors.reset)
        print(Colors.fg.red, f"  or", Colors.reset)
        print(Colors.fg.red, f"sudo mv /home/daveg/Desktop/GUI_screencast.desktop /usr/share/applications/.",
              Colors.reset)
        exit(1)
    if result != '/usr/share/applications/GUI_screencast.desktop':
        print(Colors.fg.red, f"'mv ...' failed code {result}", Colors.reset)
    else:
        print(Colors.fg.green, 'mv success.  Browse apps :: and make it favorites.  Open and set path to dataReduction',
              Colors.reset)
        print(Colors.fg.green, "you shouldn't have to remake shortcuts", Colors.reset)
elif sys.platform == 'darwin':
    print(Colors.fg.green, f"macOS: modify #! at top of 'GUI_screencast.py' to be the same as what PyCharm calls\n"
                           f"  - see first line of PyCharm execution at the top of the screen your looking at.  Copy/past that whole line.\n"
                           f"Make sure 'Python Launcher' (Python Script Preferences) option for 'Allow override with #! in script' is checked.\n"
                           f"in Finder ctrl-click on 'GUI_screencast.py' select 'duplicate.'\n"
                           f"   - Open and copy icon into paste buffer.\n"
                           f"   - Then 'Get Info' on the duplicate, click on 2nd icon, paste.   Drag duplicate item to taskbar.",
          Colors.reset)
else:
    print(Colors.fg.green, f"Browse to dist/GUI_screencast.  Make shortcut of .exe and move to Desktop.\ndouble-click on  'GUI_screencast.exe - Shortcut', set paths on buttons, pin to taskbar",
          Colors.reset)
    print(Colors.fg.green, "you shouldn't have to remake shortcuts", Colors.reset)
