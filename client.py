#client code
"""
client clode
Author: Haotian Shen
Editor: Zelan Xiang
"""
import socket
import sys
import select


def send(actions, msgs):
    """
    this is the method to send data to server
    """
    message = actions + msgs
    S.send(message)
    return


#HOST = '134.87.190.80'
#HOST = '192.168.56.1'
#HOST = '10.255.255.174'
HOST = '142.104.185.164'
PORT = 10000
ADDRESS = (HOST, PORT)
MSG = ''
S = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
S.connect(ADDRESS)
print "Client starts now"
print "================="

while True:
    #receive()
    READ_LIST = [sys.stdin, S]
    READ, WRITE, ERROR = select.select(READ_LIST, [], [])
    for sock in READ:
        if sock == S:
            data = sock.recv(1024)
            if not data:
                print '\n disconncted from server.'
                sys.exit()
            else:
                sys.stdout.write(data)
                #sys.stdout.write('\n[You]: ')
                sys.stdout.flush()
        else:

            userinput = sys.stdin.readline()
            input_split = userinput.split(" ")
            if len(input_split) > 1:
                MSG = str(input_split[1:])

            #aprint ("ok" + userinput)

            if input_split[0] == "/quit":
                S.close()
                quit()
            elif input_split[0] == "/create":
                action = '01'
            elif input_split[0] == "/delete":
                action = '02'
            elif input_split[0] == "/join":
                action = '03'
            elif input_split[0] == "/block":
                action = '04'
            elif input_split[0] == "/unblock":
                action = '05'
            elif input_split[0] == "/set_alias":
                action = '06'
            else:
                action = '00'
                MSG = input_split[0:]
                MSG = reduce((lambda x, y: x+' '+y), MSG)
            send(action, MSG)
            #sys.stdout.write(userinput)
            sys.stdout.flush()
            #print "finish"
