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

        if('echo' in message['text']):
            send(botfunctions.echo(message))

        if('whois' in message['text'].lower() ):
            send(os.getlogin())

        # if('exec' in message['text'][0:4]):
        #     send(botfunctions.exec(message))

        if('lmgtfy' in message['text'].lower()):
            send(webScraping.letMeGoogleThatForYou(message['text'][7:]))


        # regular stop
        if (message['text'].lower() == 'exit'):
            print('ended')
            exit()
        #
        if ("weather" in message['text'].lower() and message['text'].lower() != "weather" and message['text'].lower() != "weather "):
            send(webScraping.getWeather(message['text'][8:]))

        if ("image" in message['text'].lower()):
            send(webScraping.getImage(message['text'][6:]))

        if ("weather" in message['text'].lower()):
            
            try: #error checking, this covers if user types weathertroy instead of weather troy
                send(webScraping.getWeather(message['text'][8:]))
            except:
                send(webScraping.getWeather(message['text'][7:]))
            else:
                send("City Not Found - Syntax is \n \"Weather city\" or \n \"Weather ZipCode\"" +
                          "\n Ex1: Weather Troy \n Ex2: Weather 1218")

#main
if __name__ == '__main__':

    botinfo() #fetch sensitive bot info
    request_params = {'token': uID}

    #if there is no recorded last run of time make the current time the last time read
    if(not os.path.exists("time.txt")):
        fileManage.writeFile('time.txt', str(0))

    #User.assign()

    while True:
        response = requests.get('https://api.groupme.com/v3/groups/47728196/messages', params=request_params)

        #Get the messages
        if (response.status_code == 200):
            response_messages = response.json()['response']['messages']

            #get the last time messages were read and write the current time as the last time messages were read
            last_time = int(fileManage.readFile("time.txt"))
            valid_messages = []
            most_recent_message_time = 0
            print(last_time)

            # Iterate through each message, checking that it is a message that is not read before and not sent by the bot
            for message in response_messages:
                if( message['created_at'] > last_time and message['name'] != botName):
                    valid_messages.append(message)

                    if(most_recent_message_time < message['created_at']):
                        most_recent_message_time = message['created_at']

            if(last_time == 0):
                valid_messages = []

            if(most_recent_message_time != 0):
                fileManage.writeFile('time.txt', str(most_recent_message_time))

            parse_messages(valid_messages)

        time.sleep(1)