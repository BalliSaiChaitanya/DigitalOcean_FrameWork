import getpass
import os
from os.path import join as pjoin
import sys
import base64
def dc(self):
    os.chdir("conf_files")
    f= open("user.conf","r")
    contents =f.read()
    key=contents.split("=",1)
    maink=key[1]
    sig= base64.b64decode(maink.decode())
    return sig