import requests
import fileManage
from controller import send
import os
import subprocess


#ECHO: says what the message text is
def echo(msg):
    print("CMD Call: Echo ")
    toRepeat = msg['text'][5:]
    return(toRepeat)


#RUNPYTHON: takes the message text, which should be python code and runs the code
def runpython(msg):
    content = msg['text'][9:]#parse out the call command

    if(os.path.exists("yup.py")):
        os.remove("yup.py")

    fileManage.writeFile('yup.txt',content)
    fileManage.eExt("yup.txt", '.py')
    os.system("python yup.py")
    os.remove("yup.py")

def exec(msg):
    args = msg.split(" ")

    if(args[0]) == 'exit':
        print("whyd he try to exit")

    if(args[0] == 'cd'):
        os.chdir(args[1])
        p = subprocess.Popen([""], shell=True)
        return p
    else:
        p = subprocess.Popen(args, shell=True)
        return p
