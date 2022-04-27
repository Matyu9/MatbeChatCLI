# let's create the server part of a chat with socket programming
# we will use the socket library
# we will use the threading library
# we will use the time library
# we will use the random library
# we will use the sqlite3 library for storing the messages
# we will use hashlib library for the chat encryption in SHA256

import socket
import threading
import time
import random
import sqlite3

# create a socket object
# AF_INET is the address family
# SOCK_STREAM is the socket type
# we will use TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# we will create a database, is named chat.db
# we will use the sqlite3 library
conn = sqlite3.connect('chat.db', check_same_thread=False)
# we will create a cursor
c = conn.cursor()

# we will create a table named log_chat
# we will use the sqlite3 library
c.execute('''CREATE TABLE IF NOT EXISTS log_chat (timestamp text, username text, message text)''')

user = []  # list of users


# create a function 'broadcast' to send messages to all connected clients, the argument name is a
def broadcast(message, name):
    # iterate over the list of clients
    for client in user:
        # if client is the sender, skip it
        if client != s:
            # send the username, message and the time to the client like this: time: username: message
            to_send = time.strftime("%H:%M:%S") + ": " + str(name) + ": " + message
            client.send(to_send.encode('utf-8'))

            # print the message to the server console
            print(message.decode("utf-8"))
        else:
            continue


# we will create a class for clients that will use threads
class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print("New connection added: ", clientAddress)
        # add the client adress to the list of clients
        user.append(self.csocket)

    # function for the thread
    def run(self):
        # create a random name for the client
        name = random.randrange(0, 1000)
        # send the name to the client
        self.csocket.send(str(name).encode())

        # loop forever who will receive messages and broadcast them
        while True:
            # receive the message
            message = self.csocket.recv(2048)
            # if the message is empty, close the connection
            if not message:
                end_message = "Client %s is offline" % str(name)
                print(end_message)
                broadcast(end_message.encode(), name)
                # remove the client from the list of clients
                user.remove(self.csocket)
                # close the connection with the client
                self.csocket.close()
                break
            # if the message is not empty, broadcast it
            else:
                # if message starts 'quit', close the connection and broadcast end message
                if message.decode() == 'quit':
                    end_message = "Client %s is offline" % str(name)
                    print(end_message)
                    broadcast(end_message.encode(), name)
                    # remove the client from the list of clients
                    user.remove(self.csocket)
                    # close the connection with the client
                    csocket.close()
                    break
                # insert the message to the database
                c.execute("INSERT INTO log_chat VALUES (?,?,?)", (time.strftime("%d/%m/%Y"), str(name), message.decode()))
                # commit the changes
                conn.commit()
                # send the message to all clients
                broadcast(message, name)
                # print the username, the message and the time
                print(time.strftime("%d/%m/%Y"), ":", str(name), ":", message.decode())


# we will use the IP address of the server
# we will use the port number
# we will bind the socket to the address

(host, port) = ("127.0.0.1", 1217)
s.bind((host, port))

# we will listen for 5 connections
s.listen(5)

# print 'Server Started on ' + host + ':' + str(port)
print('Server Started on ' + host + ':' + str(port))

# we will create a loop to accept connections
while True:
    # accept connections
    csocket, cAddress = s.accept()
    # create a new thread for the client
    # we will pass the client address and the client socket
    # we will start the thread
    ClientThread(cAddress, csocket).start()
