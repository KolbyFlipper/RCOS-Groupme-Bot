import requests
import string
import time



global botName = "Thanos"

def botinfo():
    global botid
    global uid
    f = open("pass.txt", "r")
    lines = [line.rstrip('\n') for line in f]
    botid = lines[0]
    uid = lines[1]


def echo(toRepeate):
    print("CMD Call: Echo ")
    ret(toRepeate[toRepeate.find("echo"):])
    return;


#Controls the out flow message
def ret(msg):
    post_params = {'bot_id': botid, 'text': msg}
    requests.post('https://api.groupme.com/v3/bots/post', params=post_params)
    return;





#main


botinfo() #fetch sensitive bot info
request_params = {'token': uid}
ender = 0
fc = []

while True:
    response = requests.get('https://api.groupme.com/v3/groups/47728196/messages', params=request_params)

    # If there are new messages, check whether any of them are making queries to the bot
    if (response.status_code == 200):
        print("fffffffffff")
        response_messages = response.json()['response']['messages']

            # Iterate through each message, checking its text
        for message in response_messages:
            print(message['text'])

            if('echo' in message['text']):
                echo(message['text'][5:])

            # resume normal actions
            if (message['text'] == 'resume' and message['name'] != botName and message['id'] not in fc):
                fc.append(message['id'])
                ender = 0
                print('resume')

            # emergency stop
            if (message['text'] == 'pause' and message['name'] != botName and message['id'] not in fc):
                fc.append(message['id'])
                print('ended')
                #exit()


            if (('?' in message['text'] or 'should' in message['text']) and message['id'] not in fc and message['name'] != botName ):
                to_r = 'Nah man'
                fc.append(message['id'])
                post_params = {'bot_id': botid, 'text': to_r}
                requests.post('https://api.groupme.com/v3/bots/post', params=post_params)
                request_params['since_id'] = message['id']


time.sleep(5)
