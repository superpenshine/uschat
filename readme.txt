How to run this?

To run a demo:

1. check your local network config (ifconfig for shell, ipconfig for command line) and update the ip addresses of both the server and the client using your loopback ip. If a socket port is occupied, change it to a valid one.

2. command "python server.py" to start up the server.

3. double click the bat file to run or "sudo chmod u+x 20 clients.sh" then "./20clients.sh" in shell.

3. both sides should be running without issue now.
    In windows,type any message in a client (client 1), and tap enter in another client2 (receives the new message from client1).
    In mac/linux system, type any message in a client (client 1), message should show up in client 2 directly.
   
    The threading library we used is not compatible with windows system, but it works in max. We are looking forward to replace it with other threading library.
    
Instruction set:
if you type anythin at the input line without the format specified below, it is treatd as send message by default.

/create [chatroom name you want]    create a chatroom
/delete [chatroom name you want]    delete a chatroom if you are the creator
/join [chatroom created]            join a chatroom
/change_alias [alias you want to use in current chatroom]     change your current alias to an unused alis you want.
/block [another user alias]         kick a user out if presents, the user is also banned from join this room.
/unblock [a blocked user alias]     undo the /block command.
