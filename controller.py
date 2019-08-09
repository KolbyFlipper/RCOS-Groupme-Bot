import fileManage
import botfunctions
import webScraping
import requests
import string
import time
import os
import subprocess
import time
import user

botName = "Thanos"
localBotName = ""

#GETS THE SENSITVE BOT INFO
def botinfo():
    global botID
    global uID
    global groupID
    global first_run
    first_run = True

    f = open("pass.txt", "r")
    lines = [line.rstrip('\n') for line in f]
    botID = lines[0]
    uID = lines[1]
    groupID = lines[2]


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

        if('echo' == text[0:4] and user.allowed('echo', groupdata[message['name']])):
            send(botfunctions.echo(message))

        if('whois' == text and user.allowed('whois', groupdata[message['name']])):
            send(os.getlogin())

        if('exec' == text[0:4] and user.allowed('exec', groupdata[message['name']])):
            send(botfunctions.exec(message))

        # regular stop
        if (text == 'exit' and not first_run and user.allowed('exit', groupdata[message['name']])):
            print('ended')
            exit()

        if ("weather" in text[0:7] and text != "weather" and user.allowed('weather', groupdata[message['name']])):
            send(webScraping.getWeather(text[8:]))

        if ("google" in message['text'].lower() and user.allowed('google', groupdata[message['name']])):
            send(webScraping.letMeGoogleThatForYou(message['text']))
            #sends entire message to lmgtfy function
        
        if ("promote" in message['text'].lower() and user.allowed('promote', groupdata[message['name']])):
            msg = message['text'].split()
            if (msg.index("promote") <= len(msg)-2):
                if (msg.index("promote") == len(msg)-2 and msg[len(msg)-1] in groupdata.keys()):
                    send(groupdata[msg[len(msg)-1]].promotePlus(groupdata[message['name']]))
                if (msg.index("promote") == len(msg)-3 and msg[len(msg)-2] in groupdata.keys()):
                    send(groupdata[msg[len(msg)-2]].promote(groupdata[message['name']], msg[len(msg)-1]))
                    #send(user.parsePromote(message['text'])        

#main
if __name__ == '__main__':

    botinfo() #fetch sensitive bot info
    request_params = {'token': uID}

    #if there is no recorded last run of time make the current time the last time read
    if(not os.path.exists("time.txt")):
        fileManage.writeFile('time.txt', str(0))
        
    groupdata = user.assign(botID,uID, groupID)
    print(groupdata)

    while True:
        response = requests.get('https://api.groupme.com/v3/groups/{}/messages'.format(groupID), params=request_params)

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
                if(message['created_at'] > last_time and message['created_at'] < most_recent_message_time):
                    splitMsg = message['text'].split()
                    if((splitMsg[0]).lower() == "all" or splitMsg[0] == localBotName):
                        splitMsg.pop(0)
                        newMsg = " ".join(splitMsg)
                        message['text'] = newMsg
                        valid_messages.append(message)

            if(last_time == 0):
                valid_messages = []

            if(most_recent_message_time != 0 and most_recent_message_time != last_time):
                fileManage.writeFile('time.txt', str(most_recent_message_time-1))

            parse_messages(valid_messages)

        first_run = False
        time.sleep(1)
