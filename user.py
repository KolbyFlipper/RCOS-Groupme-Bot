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
        
    def promote(sender):
        if (ranks.index(sender.rank) <= ranks.index(self.rank)):
            return "Users can't promote beyond their rank"
        if (ranks.index(self.rank) != self.ranks.len()-1):
            self.rank = self.ranks.index(self.rank.lower())+1
        else:
            return "User already at max level"
    
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

# scans the data and either creates or updates the local user database
def assign(botID, uID, groupID):
    groupdata = dict()
    exists = os.path.isfile("users.db")
    conn = sqlite3.connect("users.db")
    curs = conn.cursor()
    if not exists: # First run or users.db not existing, this creates the users table
        curs.execute('''CREATE TABLE users (nick, id, role)''')
    members = requests.get("https://api.groupme.com/v3/groups?token={}".format(uID)).json()['response']
    for group in members:
        if group['group_id'] == groupID:
            members = group['members']
            break
    for dude in members: #reads through all the group members, adds them to groupdata and edits/adds to db
        nick = dude['nickname']
        if ("owner" in dude['roles']):
            role = 'owner'
        elif ("admin" in dude["roles"]):
            role = "admin"
        else:
            role = "user"
        if not curs.execute("SELECT id FROM users WHERE nick=?", (dude["nickname"],)).fetchone(): # if first run or user has been added in between runs of the program
            groupdata[nick] = User(nick, dude['user_id'], role)
            curs.execute("INSERT INTO users VALUES ('{}','{}', '{}')".format(nick, dude['user_id'], role))
        else: # checks new info with old database and updates where necessary
            curs.execute("SELECT role FROM users WHERE nick = '{}'".format(dude['nickname']))
            db_role = curs.fetchone()[0]
            if role == "owner" or role == "admin":
                curs.execute("UPDATE users SET role = '{}' WHERE nick = '{}'".format(role, dude['nickname']))
                groupdata[nick] = User(nick, dude['user_id'], role)
            if role == "user":
                if db_role == "admin" or db_role == "owner":
                    curs.execute("UPDATE users SET role = 'trusted' WHERE nick = '{}'".format(dude['nickname']))
                    groupdata[nick] = User(nick, dude['user_id'], "trusted")
                if db_role == ("trusted" or "moderator" or "user"):
                    groupdata[nick] = User(nick, dude['user_id'], db_role)
    conn.commit()
    conn.close()

def allowed(cmd, usr):
    if cmd in cmds[usr.rank]:
        #print(cmds[usr.rank])
        return True
    print("user {} doesn't have access to command: {}".format(usr.name,cmd))
    return False