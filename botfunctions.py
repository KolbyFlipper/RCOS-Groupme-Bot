import requests
import fileManage
from controller import send


#ECHO: says what the message text is
def echo(msg, botID):
    print("CMD Call: Echo ")
    toRepeat = msg['text'][5:]
    send(toRepeat, botID)
    return;


#RUNPYTHON: takes the message text, which should be python code and runs the code
def runpython(msg, botID):
    content = msg['text'][10:]#parse out the call command

    if(os.path.exists("yup.py")):
        os.remove("yup.py")

    fileManage.writeFile('yup.txt',content)
    fileManage.eExt("yup.txt", '.py')
    os.system("python yup.py")
    os.remove("yup.py")
