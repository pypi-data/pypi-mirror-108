version = "0.7"
from pynotifier import Notification
import sys
import os
import subprocess


def main():
    stream = os.popen("uname")
    op = stream.read()

    try:
        title = sys.argv[1]
    except:
        title = "default title"

    try:
        desc = sys.argv[2]
    except:
        desc = "default description"

    if op == "Darwin":
        subprocess.run(["python", "-m", "notipy", title, desc])
    else:
        Notification(
            title=title,
            description=desc,
            # icon_path='path/to/image/file/icon.png',  # On Windows .ico is required, on Linux - .png
            duration=5,  # Duration in seconds
            urgency='normal'
        ).send()
