import requests
import fileManage
from controller import send


#ECHO: says what the message text is
def echo(msg):
    print("CMD Call: Echo ")
    toRepeat = msg['text'][5:]
    return(toRepeat)

#RUNPYTHON: takes the message text, which should be python code and runs the code
def runpython(msg):
    content = msg['text'][10:]#parse out the call command

    if(os.path.exists("yup.py")):
        os.remove("yup.py")

    fileManage.writeFile('yup.txt',content)
    fileManage.eExt("yup.txt", '.py')
    os.system("python yup.py")
    os.remove("yup.py")

def exec(msg):
    return "NOT IMPLEMENTED"
