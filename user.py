import requests
import shlex
import string
import sqlite3
import os

ranks = ["user", "trusted", "moderator", "admin","owner"]
cmds = {"user":["echo", "lmgtfy", "weather"], "trusted":["add-user","echo", "lmgtfy", "weather"], "moderator":["add-user","echo", "lmgtfy", "weather"], "admin":["add-user","promote","pycall","echo", "lmgtfy", "weather", "whois"],"owner":["add-user","promote","pycall","echo", "lmgtfy", "exit", "weather","whois"]}

class User(object):
    
    def __init__(self, name, ID, rank):
        self.ID = ID
        self.name = name
        self.rank = rank
        
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
        print(requests.post("https://api.groupme.com/v3/groups?token={}/PLACEHOLDER/members/add".format(uID), params=add_param).json())
    except:
        print("add error placeholder")
    #else:
        #users.append(User(add_param["nickname"], ("x")))
    return "Adding user {}".format(shparam[0])

'''
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
            nick = dude['nickname']
            if ("owner" in dude['roles']):
                role = 'owner'
            else if ("admin" in dude["roles"]):
                role = "admin"
            else:
                role = "user"
            groupdata[nick] = User(nick, dude['user_id'], role) 
            f.write("{}:user_id={},role={}\n".format(dude['nickname'], dude['user_id'],role))
        f.close()
    else:
        f = open("ranks.txt","r")
        for line in f:
            line = line.split(":")
            line[1] = line[1].strip("\n").split(",")
            groupdata[line[0]] = User(line[0], line[1][0][8:], line[1][1][5:])
        f.close()
    return groupdata
'''

def assign(botID, uID):
    groupdata = dict()
    if (os.path.isfile("users.db")):
        print("fuck")
    else:
        conn = sqlite3.connect("users.db")
        curs = conn.cursor()
        curs.execute('''CREATE TABLE users (nick, id, role)''')
        members = requests.get("https://api.groupme.com/v3/groups?token={}".format(uID)).json()['response'][0]['members']
        for dude in members:
            nick = dude['nickname']
            if ("owner" in dude['roles']):
                role = 'owner'
            elif ("admin" in dude["roles"]):
                role = "admin"
            else:
                role = "user"
            groupdata[nick] = User(nick, dude['user_id'], role)
            curs.execute("INSERT INTO users VALUES ('{}','{}', '{}')".format(nick, dude['user_id'], role))
        conn.commit()
    conn.close()

def allowed(cmd, usr):
    if cmd in cmds[usr.rank]:
        #print(cmds[usr.rank])
        return True
    print("user {} doesn't have access to command: {}".format(usr.name,cmd))
    return False