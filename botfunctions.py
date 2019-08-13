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
    content = msg['text'][7:]#parse out the call command
    print(content)
    if(os.path.exists("yup.py")):
        os.remove("yup.py")
    fileManage.writeFile('yup.txt',content)
    fileManage.eExt("yup.txt", '.py')
    tort = subprocess.check_output(['python', 'yup.py'])
    #os.system("python yup.py")
    os.remove("yup.py")
    return tort

def exec(msg):
    return "NOT IMPLEMENTED"

def restart():
    os.startfile('controller.py')
    print("restarted succefssfuklly i think")
    return "end"
