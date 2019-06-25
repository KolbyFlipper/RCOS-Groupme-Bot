import requests
import shlex
import string

class User(object):
    def __init__(self, name, ID):
        self.ID = ID
        self.name = name
        self.rank = "User"
        
def addu(info, botID):
    print("CMD Call: Add-User {}".format(info))
    shparam = shlex.split(info)
    add_param = dict()
    add_param['nickname'] = shparam[0]
    add_param['bot_id'] = botID
    add_param['guid'] = "fff"
    add_param['token'] = "" #private userID
    if "@" in shparam[1]:
        add_param['email'] = shparam[1]
    elif shparam[1][0] == "+":
        add_param['phone_number'] = shparam[1]
    else:
        add_param['user_id'] = shparam[1]
    try:
        print(requests.post("https://api.groupme.com/v3/groups/47728196/members/add", params=add_param).json())
    except:
        print("add error placeholder")
    #else:
        #users.append(User(add_param["nickname"], ("x")))
    return "Adding user {}".format(shparam[0])