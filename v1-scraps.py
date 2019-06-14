import requests
import string
import fileManage
import time
import os
import subprocess

botName = "Thanos"

def botinfo():
    global botID
    global uID

    f = open("pass.txt", "r")
    lines = [line.rstrip('\n') for line in f]
    botID = lines[0]
    uID = lines[1]

def echo(toRepeat):
    print("CMD Call: Echo ")
    ret(toRepeat)
    return;

#Controls the out flow message
def ret(msg):
    post_params = {'bot_id': botID, 'text': msg}
    requests.post('https://api.groupme.com/v3/bots/post', params=post_params)
    return;

#main
if __name__ == '__main__':

    botinfo() #fetch sensitive bot info
    request_params = {'token': uID}
    ender = 0
    fc = []


    for x in range(20):
        ret('flsh')

    if(os.path.exists("yup.py")):
        os.remove("yup.py")




    while True:
        response = requests.get('https://api.groupme.com/v3/groups/47728196/messages', params=request_params)

        # If there are new messages, check whether any of them are making queries to the bot
        if (response.status_code == 200):
            response_messages = response.json()['response']['messages']

                # Iterate through each message, checking its text
            for message in response_messages:
                if(message['id'] in fc):
                    continue

                fc.append(message['id'])
                print(message['text'])

                if('echo' in message['text'] and message['name'] != botName):
                    fc.append(message['id'])
                    echo(message['text'][5:])

                # resume normal actions
                if (message['text'] == 'resume' and message['name'] != botName ):
                    fc.append(message['id'])
                    ender = 0
                    print('resume')

                if ('fojrthtry' in message['text']and message['name'] != botName and message['name'] == 'Aidan' ):
                    fc.append(message['id']) #add the message id
                    content = message['text'][10:]#parse out the call command
                    fileManage.writeFile('yup.txt',content)
                    fileManage.eExt("yup.txt", '.py')
                    os.system("python yup.py")

                    os.remove("yup.py")






                # emergency stop
                if (message['text'] == 'pause' and message['name'] != botName ):
                    fc.append(message['id'])
                    print('ended')
                    #exit()

                if (('?' in message['text'] or 'should' in message['text']) ):
                    to_r = 'Nah man'
                    fc.append(message['id'])
                    post_params = {'bot_id': botID, 'text': to_r}
                    requests.post('https://api.groupme.com/v3/bots/post', params=post_params)
                    request_params['since_id'] = message['id']

        time.sleep(5)
