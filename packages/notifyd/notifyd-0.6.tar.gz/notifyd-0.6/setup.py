from setuptools import setup
import re

version_read = re.search(
    '^version\s*=\s*"(.*)"',
    open('notifyd/notifyd.py').read(),
    re.M
)

if version_read is not None:
    version = version_read.group(1)
else:
    version = "0.1"

print("version is " + version)

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

setup(
    name='notifyd',
    version=version,
    entry_points={
        "console_scripts": ['notifyd = notifyd.notifyd:main']
    },
    packages=['notifyd'],
    url='',
    license='',
    author='madhavth',
    install_requires=[
        "py-notifier", "notipy"
    ],
    author_email='',
    description="cross platform notify cli",
    long_description=long_descr
)
