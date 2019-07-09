import fileManage
import botfunctions
import webScraping

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
    global first_run
    first_run = True

    f = open("pass.txt", "r")
    lines = [line.rstrip('\n') for line in f]
    botID = lines[0]
    uID = lines[1]


#SENDS A MESSAGE TO THE GROUP
def send(msg):
    post_params = {'bot_id': botID, 'text': msg}
    requests.post('https://api.groupme.com/v3/bots/post', params=post_params)
    return;

#CHECKS ALL THE MESSAGES FOR KEYWORDS
def parse_messages(valid_messages):
    for message in valid_messages:
        print(message['text'])
        text = message['text'].lower().rstrip()

        if('echo' == text[0:4]):
            send(botfunctions.echo(message))

        if('whois' == text):
            send(os.getlogin())

        # if ('fojrthtry' in message['text']):
        #     send(botfunctions.runpython(message))

        if('exec' == text[0:4]):
            send(botfunctions.exec(message))

        # regular stop
        if (text == 'exit' and not first_run):
            print('ended')
            exit()

        if ("weather" in text[0:7] and text != "weather"):
            send(webScraping.getWeather(message['text'][8:]))

        if ("image" in text[0:5] and text != "image"):
            send(webScraping.getImage(message['text'][6:]))

#main
if __name__ == '__main__':

    botinfo() #fetch sensitive bot info
    request_params = {'token': uID}

    #if there is no recorded last run of time make the current time the last time read
    if(not os.path.exists("time.txt")):
        fileManage.writeFile('time.txt', str(0))

    while True:
        response = requests.get('https://api.groupme.com/v3/groups/47728196/messages', params=request_params)

        #Get the messages
        if (response.status_code == 200):
            response_messages = response.json()['response']['messages']

            #get the last time messages were read and write the current time as the last time messages were read
            last_time = int(fileManage.readFile("time.txt")) #LAST CONFIRMEND SECOND THAT ALL MESSAGES WERE READ
            valid_messages = []
            most_recent_message_time = 0

            # Iterate through each message, checking that it is a message that is not read before and not sent by the bot
            for message in response_messages:
                if(message['name'] != botName and most_recent_message_time < message['created_at']):
                    most_recent_message_time = message['created_at']


            if(most_recent_message_time == last_time + 1):
                most_recent_message_time += 1

            for message in response_messages:
                if(message['created_at'] > last_time and message['created_at'] < most_recent_message_time and message['name'] != botName):
                    valid_messages.append(message)


            if(last_time == 0):
                valid_messages = []

            if(most_recent_message_time != 0 and most_recent_message_time != last_time):
                fileManage.writeFile('time.txt', str(most_recent_message_time-1))

            parse_messages(valid_messages)

        first_run = False
        time.sleep(1)
