import requests
import shlex
import string

class User(object):
    
    ranks = ["user", "trusted", "moderator", "admin","owner"]
    cmds = {"user":[], "trusted":["add-user"], "moderator":["add-user"], "admin":["add-user","promote","pycall"],"owner":["add-user","promote","pycall"]}
    
    def __init__(self, name, ID):
        self.ID = ID
        self.name = name
        self.rank = "User"
        
    def promote():
        if (self.ranks.index(self.rank) != 5):
            self.rank = self.ranks.index(self.rank.lower())+1
        else:
            return "User already max level"
    
    def promote(nuRank):
        if (nuRank.lower() in self.ranks):
            self.rank = nuRank
        else:
            return "Invalid user level"
        
##################################################################
###################  Nonmember functions  ########################
##################################################################
        
def addu(info, botID, uID):
    print("CMD Call: Add-User {}".format(info))
    shparam = shlex.split(info)
    add_param = dict()
    add_param['members'] = []
    add_param['members'].append(dict())
    add_param['members'][0]['nickname'] = shparam[0]
    add_param['members'][0]['bot_id'] = botID
    add_param['members'][0]['guid'] = "fff"
    if "@" in shparam[1]:
        add_param['members'][0]['email'] = shparam[1]
    elif shparam[1][0] == "+":
        add_param['members'][0]['phone_number'] = shparam[1]
    else:
        add_param['members'][0]['user_id'] = shparam[1]
    try:
        print(requests.post("https://api.groupme.com/v3/groups?token=2FbBv60XqZzn6kFuxQ4gL0OfxmrwRREosahZcUry/47728196/members/add", params=add_param).json())
    except:
        print("add error placeholder")
    #else:
        #users.append(User(add_param["nickname"], ("x")))
    return "Adding user {}".format(shparam[0])

def assign(botID,uID):
    groupdata = dict()
    try:
        open("ranks.txt", "r")
        x=False
    except:
        open("ranks.txt", "x")
        x=True
    
    if (x):
        f = open("ranks.txt","w")
        members = requests.get("https://api.groupme.com/v3/groups?token={}".format(uID)).json()['response'][0]['members']
        for dude in members:
            groupdata[dude['nickname']] = {"user_id":dude["user_id"], "role":dude["roles"][0]}
            f.write("{}:user_id={},role={}\n".format(dude['nickname'], dude['user_id'],dude['roles'][0]))
        f.close()
    else:
        f = open("ranks.txt","r")
        for line in f:
            line = line.split(":")
            line[1] = line[1].strip("\n").split(",")
            groupdata[line[0]] = {"user_id":line[1][0][8:], "role":line[1][1][5:]}
        f.close()
    return groupdata
