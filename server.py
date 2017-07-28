#server code
"""
This is the server code, which is for SENG299 project.
Author: Zelan Xiang
Editor: Haotian Shen
"""
import socket
import select
import time

class Chatroom(object):
    """This is the chatroom class, which include 5 attributes:
     room name, room number, room creator, block list, roommate list;
     4 methods: joinroom, quitroom, add_block, remove_block."""
    def __init__(self, name, owner, number):
        """
        This the initialize method for chatroom.
        """
        self.roomname = name
        self.roomnum = number
        self.creator = owner
        self.roommate = []
        self.block = []

    def joinroom(self, user_address):
        """
        The joinroom method is the join method we design in milestone 2.
        We cnanged the name, because we do not want to mix this method with
        join method in server class.
        This method will add user's address to roommate list.
        """
        self.roommate.append(user_address)

    def quitroom(self, user_address):
        """
        The quitroom method is the quit method we discribed in milestone 2.
        This method will delete the user's address from roommate list.
        """
        try:
            self.roommate.remove(user_address)
        except Exception:
            print "%s is not in list" %(str(user_address))

    def add_block(self, user_address):
        """
        This method will add the user's address to block list.
        """
        self.block.append(user_address)

    def remove_block(self, user_address):
        """
        This method will remove the user's address from block list.
        """
        try:
            self.block.remove(user_address)
        except Exception:
            print "%s is not in list" %(str(user_address))

def sendmeg(currtime, room_name, username, meg):
    """
    The sendmeg method is the send method we design in milestone 2.
    We change the method name, because we do not want to mix with .send() method in socket library.
    This method will broadcast the message to all clients in given chatroom.
    """
    sender_socket = S
    client_socket = S
    if username == 'admin':
        message1 = meg + '\n'
    else:
        message1 = "[%s][%s][%s]: [%s]\n\n" %(room_name, currtime, username, meg)
    for room in ROOM_LIST:
        if room_name == room.roomname:
            broadcast_list = room.roommate
            break

    for tempclient in CLIENT_LIST:
        if username == tempclient['name']:
            sender_socket = tempclient['socket']
            break

    for client1 in broadcast_list:
        for tempclient1 in CLIENT_LIST:
            if client1 == tempclient1['address']:
                client_socket = tempclient1['socket']
                break
        if client_socket != S and client_socket != sender_socket:
            try:
                client_socket.send(message1)
            except Exception:
                client_socket.close()

def create(room_name, user1):
    """
    This method will create a new chatroom. If the room name is used,
    return the error message to requester.
    """
    global ROOM_LIST, CLIENT_LIST
    for room in ROOM_LIST:
        if room_name == room.roomname:
            return "\n[Error, the room name already used.]\n\n"
    room_index = len(ROOM_LIST)
    temp_room = Chatroom(room_name, user1['address'], room_index)
    ROOM_LIST.append(temp_room)
    for temp3 in CLIENT_LIST:
        if user1 == temp3:
            ROOM_LIST[temp3['room']].quitroom(temp3['address'])
            ROOM_LIST[room_index].joinroom(temp3['address'])
            temp3['room'] = ROOM_LIST[room_index].roomnum
            break
    message2 = "\n[Room %s has been created.]\n" %(room_name)
    sendmeg(time.strftime('%m-%d %H:%M:%S', time.localtime()), 'global', 'admin', message2)
    return "\n[room create success]\n\n"

def delete(room_name, user6):
    """
    This method will delete a chatroom if the user is room owner.
    And move all roommate to global room
    ROOM_LIST will still has this room with no room information
    """
    global ROOM_LIST, CLIENT_LIST
    for room in ROOM_LIST:
        if room_name == room.roomname:
            times = 1
            if room.creator != user6['address']:
                return "\n[Error, you are not able to delete this room.]\n\n"
            room.creator = ADDRESS
            while room.roommate:
                for temp13 in CLIENT_LIST:
                    if room.roommate[0] == temp13['address']:
                        print "delete: " + str(times)
                        room.quitroom(temp13['address'])
                        ROOM_LIST[0].joinroom(temp13['address'])
                        temp13['room'] = 0
                        message7 = "\n[You are moved from room %s to global room.]\n\n" % room_name
                        temp13['socket'].send(message7)
                        times = times + 1
                        break
            room.roomname = ''
            room.roomnum = 0
            print "after delete the room mate is: "
            print room.roommate
            return "\n[You delete room %s successfully.]\n\n" % room_name
    return "\n[Error, the given room is not exsit.]\n\n"

def join(room_name, user2):
    """
    This method will detect whether the user could join a chatroom or could not.
    """
    global ROOM_LIST, CLIENT_LIST
    for room in ROOM_LIST:
        if room_name == room.roomname:
            for anyone in room.block:
                if user2['address'] == anyone:
                    return "\n[Error, the room do not want you.]\n\n"
            for temp4 in CLIENT_LIST:
                if user2 == temp4:
                    ROOM_LIST[temp4['room']].quitroom(temp4['address'])
                    room.joinroom(temp4['address'])
                    temp4['room'] = room.roomnum
                    message3 = "\n[new user %s entered %s.]\n" %(temp4['name'], room_name)
                    sendmeg(tm, ROOM_LIST[temp4['room']].roomname, 'admin', message3)
                    return "\n[you join room %s successfully.]\n\n" % room_name
    return "\n[Error, the given room is not exsit.]\n\n"

def block(block_name, user3):
    """
    This method will detect whether the user could block other user or could not.
    If user has ability to block, then block
    """
    global ROOM_LIST, CLIENT_LIST
    room_num = user3['room']
    nothasclient = True
    for temp5 in CLIENT_LIST:
        if block_name == temp5['name']:
            blocked_user = temp5
            nothasclient = False
            break
    if nothasclient:
        return "\n[Error, he/she is not connected.]\n\n"
    for room in ROOM_LIST:
        if room_num == room.roomnum:
            if user3['address'] != room.creator or block_name == user3['name']:
                return "\n[Error, you are not able to block this person.]\n\n"
            for client1 in room.roommate:
                if client1 == blocked_user['address']:
                    room.add_block(blocked_user['address'])
                    for temp1 in CLIENT_LIST:
                        if blocked_user == temp1:
                            room.quitroom(temp1['address'])
                            ROOM_LIST[0].joinroom(temp1['address'])
                            temp1['room'] = ROOM_LIST[0].roomnum
                            temp1['socket'].send("\n[You have been remove from room.]\n\n")
                            return "\n[block user success]\n\n"
            room.add_block(blocked_user['address'])
            return "\n[He/she is not in room. He/She would not be able to join this room.]\n\n"
    return "\n[Error, there is no such room.]\n\n"

def unblock(unblock_name, user4):
    """
    This method will detect whether the user could unblock other user or could not.
    If user has ability to unblock, then unblock.
    """
    global ROOM_LIST
    room_num = user4['room']
    nothasclient2 = True
    for temp11 in CLIENT_LIST:
        if unblock_name == temp11['name']:
            blocked_user = temp11
            nothasclient2 = False
            break
    if nothasclient2:
        return "\n[Error, he/she is not connected.]\n\n"
    for room in ROOM_LIST:
        if room_num == room.roomnum:
            if user4['address'] == room.creator:
                room.remove_block(blocked_user['address'])
                return "\n[unblock user success]\n\n"
            return "\n[Error, you are not able to unblock anyone.]\n\n"
    return "\n[Error, there is no such room.]\n\n"

def change_alias(new_name, user5):
    """
    This method will change the alias.
    """
    global CLIENT_LIST
    if new_name == 'admin':
        return "\n[Error, you can not use this name.]\n\n"
    for temp9 in CLIENT_LIST:
        if new_name == temp9['name']:
            return "\n[Error, the name is used by other client.]\n\n"
    for temp6 in CLIENT_LIST:
        if user5 == temp6:
            old_name = temp6['name']
            temp6['name'] = new_name
            message4 = "\n[User %s change his/her alias to %s]\n\n" %(old_name, new_name)
            sendmeg(tm, ROOM_LIST[temp6['room']].roomname, 'admin', message4)
            return "\n[change alias success]\n"

def find_who(user_address):
    """
    this is to use a address and return a name
    """
    for client1 in CLIENT_LIST:
        if user_address == client1['address']:
            return client1['name']

S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = socket.gethostname()
PORT = 10000
ADDRESS = (HOST, PORT)

USER = {'address':(0, 0), 'name':'admin', 'room':0, 'socket':''}
CLIENT_LIST = []
ROOM_LIST = []

GLOBAL = Chatroom('global', ADDRESS, 0)
ROOM_LIST.append(GLOBAL)

print "server start..."
print "start on PORT %s" %PORT
print "name: %s, number: %s, owner: %s." %(GLOBAL.roomname, GLOBAL.roomnum, GLOBAL.creator)

INDEX = 1
CONNECT_LIST = []
S.bind(ADDRESS)
S.listen(5)
CONNECT_LIST.append(S)

while True:
    READ, WRITE, ERROR = select.select(CONNECT_LIST, [], [])
    for connect in READ:
        tm = time.strftime('%m-%d %H:%M:%S', time.localtime())
        if connect == S:
            client, addr = S.accept()
            CONNECT_LIST.append(client)
            USER['address'] = addr
            USER['name'] = 'User_Name'+ str(INDEX)
            USER['room'] = 0
            USER['socket'] = client
            CLIENT_LIST.append(USER)
            ROOM_LIST[USER['room']].joinroom(USER['address'])

            temproom = ROOM_LIST[CLIENT_LIST[-1]['room']].roomname
            tempname = CLIENT_LIST[-1]['name']

            sendmeg(tm, temproom, 'admin', "\n[new user %s entered %s]\n" %(tempname, temproom))
            USER = {'address':(0, 0), 'name':'User_Name', 'room':0, 'socket':''}
            INDEX = INDEX + 1
        else:
            for temp7 in CLIENT_LIST:
                if connect == temp7['socket']:
                    tempuser = temp7
                    break
            try:
                pack = connect.recv(1024)
                if pack == '':
                    continue
#send
                if pack[:2] == '00':
                    connect.send("\n")
                    sendmeg(tm, ROOM_LIST[tempuser['room']].roomname, tempuser['name'], pack[2:-1])
                    print ROOM_LIST[tempuser['room']].roommate
                    print "finish send message\n"
#create
                elif pack[:2] == '01':
                    result = create(pack[2:][3:-5], tempuser)
                    connect.send(result)
                    print "finish create\n"
                    print ROOM_LIST
                    print CLIENT_LIST
#delete
                elif pack[:2] == '02':
                    result = delete(pack[2:][3:-5], tempuser)
                    connect.send(result)
                    print "finish delete\n"
                    print ROOM_LIST
                    print ROOM_LIST[-1].roommate
                    print ROOM_LIST[-1].roomnum
                    print ROOM_LIST[-1].creator
                    print CLIENT_LIST
#join
                elif pack[:2] == '03':
                    result = join(pack[2:][3:-5], tempuser)
                    connect.send(result)
                    print "finish join\n"
                    print CLIENT_LIST
                    print ROOM_LIST[tempuser['room']].roommate
#block
                elif pack[:2] == '04':
                    result = block(pack[2:][3:-5], tempuser)
                    connect.send(result)
                    print "finish block\n"
                    print CLIENT_LIST
                    print ROOM_LIST[tempuser['room']].block
#unblock
                elif pack[:2] == '05':
                    result = unblock(pack[2:][3:-5], tempuser)
                    connect.send(result)
                    print "finish unblock\n"
                    print CLIENT_LIST
                    print ROOM_LIST[tempuser['room']].block
#changename
                elif pack[:2] == '06':
                    result = change_alias(pack[2:][3:-5], tempuser)
                    connect.send(result)
                    print "finish change alias\n"
                    print CLIENT_LIST
            except Exception:
                print 'in exception'
                message5 = "\n[User %s is offline.]\n" %tempuser['name']
                sendmeg(tm, ROOM_LIST[tempuser['room']].roomname, 'admin', message5)
                message6 = "\n[The new user %s i not the same person.]\n\n" %tempuser['name']
                sendmeg(tm, ROOM_LIST[tempuser['room']].roomname, 'admin', message6)
                for temp8 in CLIENT_LIST:
                    if connect == temp8['socket']:
                        ROOM_LIST[temp8['room']].quitroom(temp8['address'])
                        CLIENT_LIST.remove(temp8)
                        break
                connect.close()
                CONNECT_LIST.remove(connect)
                continue
