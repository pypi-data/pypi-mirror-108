version = "0.5"
from pynotifier import Notification
import sys


def main():
    try:
        title = sys.argv[1]
    except:
        title = "default title"

    try:
        desc = sys.argv[2]
    except:
        desc = "default description"

    Notification(
        title=title,
        description=desc,
        # icon_path='path/to/image/file/icon.png',  # On Windows .ico is required, on Linux - .png
        duration=5,  # Duration in seconds
        urgency='normal'
    ).send()
