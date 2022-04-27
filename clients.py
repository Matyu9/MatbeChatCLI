# let's create the client part of a chat with socket programming

# we will use sockets to connect to the server
# we will use the same server as in the previous exercise
# we will use the same port and ip as in the previous exercise
# we will use the same protocol as in the previous exercise

# we will use threads for the client because I want to send and receive messages at the same time

import socket
import threading


# create the class for the client thread
class ClientThread(threading.Thread):
    def __init__(self, client_socket, client_address):
        threading.Thread.__init__(self)
        self.client_socket = client_socket
        self.client_address = client_address

    def run(self):
        # while loop to receive messages from the server
        while True:
            # receive the message from the server
            messages = self.client_socket.recv(1024).decode()
            # if the message is empty, the client has disconnected
            if messages == '':
                break

            # print the message
            print(messages)


# create a socket object 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# create a tuple with the ip and port
server_address = ('127.0.0.1', 1217)


# create a try-except block to catch errors
try:
    # connect to the server
    s.connect(server_address)

    # create a thread for the client
    client_thread = ClientThread(s, server_address)
    client_thread.start()

    # while loop to send messages to the server
    while True:
        # get the message from the user
        message = input(">> ")
        # send the message to the server
        s.send(message.encode())

except Exception as e:
    # if an error occurs, print the error
    print("An error has occurred: {}".format(e))
    # close the socket
    s.close()
