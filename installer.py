import getpass
import os
from os.path import join as pjoin
import sys
import base64
import signal

def handler(signum, frame):
    print("\n\n\n\n!!!!--->FrameWork Execution is terminated<---!!!!\n\n\n\n")
    sys.exit()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, handler)


class installer:
    print(  " 1. ConfigParser,\n2. paramiko,\n3. SCPClient,\n4. getpass,\n5. datetime,\n6. argparse,\n7. subprocess,\n8. sys,\n9. signal,\n10. time,\n11. csv,\n12. requests,\n13. json.\n\n")
    print("---->These are the 13 Modules which are Required if these modules are not installed this installer will install all these modules Automatically\n")
    ver=sys.version_info.major
    if ver < 3:
        permission=raw_input("\n---->To continue with the Installation type 'Yes'----->")
        print("installed Python version is python 2.7")
    elif ver >= 3:
        permission=input("\n---->To continue with the Installation type 'Yes'----->")  
        print("installed Python version is python 3")
    elif ver <= 2.6:
        print("!-----------!> INSTALLED PYTHON VERSION NOT MEET WITH REQUIRED VERSION <!-----------!")
    yes_permission=("yes","y","Yes","YES")
    
    
    if permission in yes_permission:
        try:
            import ConfigParser
        except ImportError as e:
            print("ConfigParser is not installed") # module doesn't exist  deal with it.
            os.system("pip install ConfigParser --user")
        try:
            import paramiko
        except ImportError as e:
            print("paramiko is not installed") # module doesn't exist  deal with it.
            os.system("pip install paramiko --user")
        try:
            import scpclient
        except ImportError as e:
            print("scpclient is not installed") # module doesn't exist  deal with it.
            os.system("pip install scpclient --user")
        try:
            import getpass
        except ImportError as e:
            print("getpass is not installed") # module doesn't exist  deal with it.
            os.system("pip install getpass --user")
        try:
            import datetime
        except ImportError as e:
            print("datetime is not installed") # module doesn't exist  deal with it.
            os.system("pip install datetime --user")
        try:
            import argparse
        except ImportError as e:
            print("argparse is not installed") # module doesn't exist as deal with it.
            os.system("pip install argparse --user")
        try:
            import subprocess
        except ImportError as e:
            print("subprocess is not installed") # module doesn't exist as deal with it.
            os.system("pip install subprocess --user")
        try:
            import signal
        except ImportError as e:
            print("signal is not installed") # module doesn't exist as deal with it.
            os.system("pip install signal --user")
        try:
            import csv
        except ImportError as e:
            print("csv is not installed") # module doesn't exist as deal with it.
            os.system("pip install csv --user")
        try:
            import requests
        except ImportError as e:
            print("requests is not installed") # module doesn't exist as deal with it.
            os.system("pip install requests --user")
        try:
            import simplecrypt
        except ImportError as e:
            print("simplecrypt is not installed") # module doesn't exist as deal with it.
            os.system("pip install simple-crypt")
        try:
            import json
        except ImportError as e:
            print("json is not installed") # module doesn't exist as deal with it.
            os.system("pip install json --user")     
        print("|\n|\n|\n|\n|----->All Modules Installed Successfully<------|\n|\n|\n|\n|")
    else:
        print("-----!> Installer Aborted <!-----")
       
    def ecrypt(self,p_key):
        enc=base64.b64encode(p_key.encode())
        print("|\n|\n|\n|\n|---->DONE<----|\n|\n|\n|")
        #print("Current directory is this---> "+os.getcwd())
        #base_dir=os.getcwd()
        os.chdir("conf_files")
        conf_dir=os.getcwd()
        f= open("user.conf","w+")
        #f.write("!!!------Alert Confidential File Please Close------!!!\n")
        f.write("signal="+enc)

print("please Enter Digital Ocean user Key! key length would be approx 20 characters!\n")
key=getpass.getpass(prompt='Key: ', stream=None)
ins=installer()
ins.ecrypt(key)









           