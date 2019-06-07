

#CHANGE UID to user id
import requests
import string
import time

request_params = {'token': 'BOTIDHERE'}
ender = 0
target = 'Aidan'
fc = []

while True:
    response = requests.get('https://api.groupme.com/v3/groups/UID/messages', params=request_params)

    # If there are new messages, check whether any of them are making queries to the bot
    if (response.status_code == 200):
        response_messages = response.json()['response']['messages']

        # Iterate through each message, checking its text
    for message in response_messages:
        print(message['text'])

        # resume normal actions
        if (message['text'] == 'resume' and message['name'] == 'Aidan' and message['id'] not in fc):
            fc.append(message['id'])
            ender = 0
            print('resume')

        # emergency stop
        if (message['text'] == 'pause' and message['name'] == 'Aidan' and message['id'] not in fc):
            fc.append(message['id'])
            print('Program Stopping')
            exit()

        if (('?' in message['text'] or 'should' in message['text']) and message['id'] not in fc):
            to_r = 'Nah man'
            fc.append(message['id'])
            post_params = {'bot_id': 'BOTIDHERE', 'text': to_r}
            requests.post('https://api.groupme.com/v3/bots/post', params=post_params)
            request_params['since_id'] = message['id']

        time.sleep(5)

        # if 'mono' in message['']
        #    if(target in message['name']):
        #        copycat = message['text']
        #    post_params = { 'bot_id' : 'BOTIDHERE', 'text': copycat}
        #      requests.post('https://api.groupme.com/v3/bots/post', params = post_params)
        #    request_params['since_id'] = message['id']
        #  time.sleep(1)
        '''
            if ("something" in message['text']):
                # Construct a response to send to the group
                to_send = 'THIS IS THE END\N{FACE SCREAMING IN FEAR}'

                # Send the response to the group
                for pls in range(0,1):
                    post_params = { 'bot_id' : 'BOTIDHERE', 'text': to_send }
                    requests.post('https://api.groupme.com/v3/bots/post', params = post_params)
                    request_params['since_id'] = message['id']
                break
        '''
