#setup.py
from setuptools import setup
import re

#change version number in dnotify file  add/edit version="DESIRED_VERSION NUMBER" at the top of file

with open("README.md", "rb") as f:
    long_descr = f.read().decode("utf-8")

version_read = re.search(
    '^version\s*=\s*"(.*)"',
    open('dnotify').read(),
    re.M
)

if version_read is not None:
    version = version_read.group(1)
else:
    version = "0.1"


setup(
    name='dnotify',
    scripts=['dnotify'],
    version= version,
	install_requires=["notifyd", "notipy"],
    description = 'attempt at a cross platform desktop notification cli',
    long_description = long_descr,
    author = 'madhavth'
)
