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

def randomString(msg):
    value = int(msg['text'][7:])
    if(value>1000):
        return "That's too long! Maximum length is 1000"
    if(value<1):
        return "Obviously, you can't have a negative or zero length string. Stop it."
    alphaBET = "abcdefghijklmnopqrstuvwxyz1234567890!?"
    strang = []
    for x in range(value):
        strang.append(alphaBET[random.randint(0,37)])

    return "".join(strang)

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

def getHelp():
    commands = []
    commands.append("1. help: Will display this comment to the user. Example: help")
    commands.append("\n 2. google: Will generate a lightly sardonic google link. \n Example: google where is alaska  ")
    commands.append("\n 3. weather: Will give you the weather in a zip code or city \n Example: weather 11742 or weather Detroit")
    commands.append("\n 4. runpython: This will allow you to run python code from your groupchat! Example: runpython for x in range(10): \n \t print(\"hello\")")
    commands.append("\n 5. string: a simple command to generate random strings of a given length 1-1000. Example: string 100")
    commands.append("\n 6. echo: Repeats the phrase that you have sent. \n Example: echo hello world ")
    commands.append("\n 7. promote: will either increase a user's rank by one or set it to another rank \n Example: promote Bob OR promote Bob admin")
    commands.append("\n 8. users: displays the group members and their ranks")
    commands.append("\n 9. whois: Will display the system name of the user running the program")
    commands.append("\n 10. exit: exits the program.")
    return " ".join(commands)

def who(groupdata):
    retval = "Users:\n"
    whoswho = dict()
    order = ['owner', 'admin', 'moderator', 'trusted', 'user']
    whoswho['owner'] = []
    whoswho['admin'] = []
    whoswho['moderator'] = []
    whoswho['trusted'] = []
    whoswho['user'] = []
    for member in groupdata.keys():
        whoswho[groupdata[member].rank].append(groupdata[member].name)
    for rank in order:
        whoswho[rank].sort()
        for person in whoswho[rank]:
            retval += "{}: {}\n".format(rank.capitalize(), person)
    return retval
        
        
