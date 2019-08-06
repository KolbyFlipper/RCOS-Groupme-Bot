<<<<<<< HEAD
import requests
import fileManage
from controller import send
import random


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

def randomString(msg):
    value = int(msg['text'][7:])
    if(value>1000):
        return "That's too long! Maximum length is 1000"
    if(value<0):
        return "Obviously, you can't have a negative length string. Stop it."
    alphaBET = "abcdefghijklmnopqrstuvwxyz1234567890!?"
    strang = []
    for x in range(value):
        strang.append(alphaBET[random.randint(0,37)])

    return "".join(strang)

def getHelp():
    commands = []
    commands.append("1. help: Will display this comment to the user. Example: help")
    commands.append("\n 2. google: Will generate a lightly sardonic google link. \n Example: google where is alaska  ")
    commands.append("\n 3. weather: Will give you the weather in a zip code or city \n Example: weather 11742 or weather Detroit")
    commands.append("\n 4. runpython: This will allow you to run python code from your groupchat! Example: runpython for x in range(10): \n \t print(\"hello\")")
    commands.append("\n 5. string: a simple command to generate random strings of a given length 1-1000. Example: string 100")
    commands.append("\n 6. echo: Repeats the phrase that you have sent. \n Example: echo hello world ")
    commands.append("\n 7. whois: Will display the system name of the user running the program")
    commands.append("\n 8. exit: exits the program.")
    
    return " ".join(commands)
# def sendImg(msg):
=======
import requests
import fileManage
from controller import send
import os


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
    return "NOT IMPLEMENTED"
>>>>>>> master
