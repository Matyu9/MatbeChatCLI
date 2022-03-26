# Let's create an interface for our client.
# This will be used to receive the data from the server and send a response.

# We will be using the socket library to create a socket.
# We will use Tkinter to create a GUI.
# We will use the threading library to create a thread for receive data from the server.

import socket
import tkinter as t
import threading

# Create a class thread for receiving data from the server.
class ReceiveData(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.sock = sock

    def run(self):
        while True:
            try:
                data = self.sock.recv(1024)
                if data:
                    print(data.decode())
                    # display the data on the GUI from ClientInterface.
                    ClientInterface.display_data(data.decode())

            except Exception as e:
                print("Error receiving data: " + str(e))
                break

# Our GUI component will be an Input field and a Button for sending data and a Label for displaying the data.
class ClientInterface(t.Frame):
    def __init__(self, master=None, sock=None):
        t.Frame.__init__(self, master)
        self.master = master
        self.pack()
        self.createWidgets()
        self.sock = sock

    def createWidgets(self):
        self.input = t.Entry(self)  # Create an input field.
        self.input.pack(side="left")  # Pack the input field.
        self.input.focus_set()  # Set the focus to the input field.
        self.input.bind("<Return>", self.sendData)  # Bind the Enter key to the sendData function.
        self.sendButton = t.Button(self, text="Send", command=self.sendData)  # Create a button for sending data.
        self.sendButton.pack(side="left")  # Pack the button.
        self.label = t.Label(self, text="")  # Create a label for displaying the data.
        self.label.pack(side="left")  # Pack the label.

    def sendData(self, event=None, sock=None):
        data = self.input.get()
        self.input.delete(0, t.END)
        self.label["text"] = data
        # Send the data to the server.
        self.sock.send(data.encode())

    def display_data(self, data):
        self.label["text"] = data


# Create the socket.
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# The host is '127.0.0.1' and the port is 1217.
(host, port) = ("127.0.0.1", 1217)

# Connect to the server.
sock.connect((host, port))

# Create a thread for receiving data from the server.
receiveData = ReceiveData(sock)
receiveData.start()

# Display the GUI.
root = t.Tk()
root.title("Client")
root.geometry("300x100")
app = ClientInterface(master=root, sock=sock)
app.mainloop()
