import requests
import shlex
import string
import sqlite3
import os

ranks = ["user", "trusted", "moderator", "admin","owner"]
cmds = {"user":["echo", "lmgtfy", "users", "weather"], "trusted":["add-user","echo", "lmgtfy", "users", "weather"], "moderator":["add-user","echo", "lmgtfy", "users", "weather"], "admin":["add-user","promote","pycall","echo", "lmgtfy", "users", "weather", "whois"],"owner":["add-user","promote","pycall","echo", "lmgtfy", "exit", "users", "weather","whois"]}

class User(object):
    
    def __init__(self, name, ID, rank):
        self.ID = ID
        self.name = name
        self.rank = rank
        
    def promotePlus(self, sender):
        if (ranks.index(sender.rank) <= ranks.index(self.rank)):
            return "Users can't promote beyond their rank"
        if (ranks.index(self.rank) < len(ranks)):
            return self.promote(sender, ranks[ranks.index(self.rank)+1])
        return "User already at max level"
    
    def promote(self, sender, nuRank):
        if nuRank not in ranks:
            return "Invalid user level. Valid User levels: user, trusted, moderator, admin, and owner"
        if ranks.index(sender.rank) < ranks.index(nuRank):
            return "Users can't promote beyond their rank"
        if self.rank == nuRank:
            return "{} is already {}".format(self.name, nuRank)
        conn = sqlite3.connect("users.db")
        curs = conn.cursor()
        curs.execute("UPDATE users SET role = '{}' WHERE nick = '{}'".format(nuRank, self.name)) 
        conn.commit()
        conn.close()
        return "{} is now {}".format(self.name, nuRank)
        
        
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
                else:
                    groupdata[nick] = User(nick, dude['user_id'], db_role)
    conn.commit()
    conn.close()
    return groupdata

def allowed(cmd, usr):
    if cmd in cmds[usr.rank]:
        #print(cmds[usr.rank])
        return True
    post_params = {'bot_id': botID, 'text': "User {} does not have access to command: {}".format(usr.name, cmd)}
    requests.post('https://api.groupme.com/v3/bots/post', params=post_params)   
    return False