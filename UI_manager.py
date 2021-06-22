import socket
import threading
import sys
from tkinter import *
from tkinter import messagebox


class chatGUI:
    def __init__(self, root):
        self.currentLine = 0
        self.master = root
        self.master.title("Peer to Peer Messenger")


        self.Nickname = Entry(self.master, width=18)  # Nickname entry box
        self.Nickname.grid(row=0, column=2)
        self.INLabel = Label(self.master, text="Please enter Nickname")
        self.INLabel.grid(row=0, column=1)
        self.INButton = Button(self.master, text="Set",command=self.sendName)  # sets nickname
        self.INButton.grid(row=0, column=3, padx=5, pady=5)

        self.IPentry = Entry(self.master, width=18)  # ip entry box
        self.IPentry.grid(row=1, column=2)
        self.IPLabel = Label(self.master, text="Enter Peer's Public IP:")
        self.IPLabel.grid(row=1, column=1)
        self.IPButton = Button(self.master, text="Connect",command=self.sendIP)  # connect button
        self.IPButton.grid(row=1, column=3, padx=5, pady=5)

        self.logLabel = Label(self.master, text="Chat Log")  # log text
        self.logLabel.grid(row=2, column=1)
        self.logBox = Text(self.master, height=15, width=50,state=DISABLED)  # log box
        self.logBox.grid(row=3, column=1, padx=20, columnspan=2)

        self.inputLabel = Label(self.master, text="Input Message:")  # entry text
        self.inputLabel.grid(row=4, column=1)
        self.inputBox = Text(self.master, height=5, width=50)  # entry box
        self.inputBox.grid(row=5, column=1, padx=20, columnspan=2)

        self.nextButton = Button(self.master, text="Send", command=self.sendMessageClick)  # send text button
        self.nextButton.grid(row=5, column=3, pady=5)

        self.quitButton = Button(self.master, text="Quit", command=self.master.destroy)  # quit button
        self.quitButton.grid(row=6, column=1, padx=5, pady=5)


    def printMessage(self,message):
        self.logBox.configure(state=NORMAL)
        self.logBox.insert(END, message)
        #self.logBox.insert(END, "\n")
        self.logBox.configure(state=DISABLED)

    def sendMessageClick(self):
        #print("send message click called")
        message = self.inputBox.get("1.0", "end")
        message = Nickname + ": " + message
        self.printMessage(message)#this dupes the message if you're connected to yourself but thats okay
        sendMessage(message)
        self.inputBox.delete("1.0", "end")

    def sendName(self):
        global Nickname
        Nickname = self.Nickname.get()

    def sendIP(self):
        IP = self.IPentry.get()
        startClientThread(IP)



def processMessages(conn, addr):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                conn.close()
            print(data.decode("utf-8"))
            mainGUI.printMessage(data.decode("utf-8"))
            conn.sendall(bytes('Message received!', 'utf-8'))
        except:
            conn.close()
            print("Connection closed by", addr)
            sys.exit()# Quit the thread.

def startServer():
    while True:
        # Wait for connections
        print('Waiting for Connection')
        conn, addr = s.accept()
        print('Got connection from ', addr[0], '(', addr[1], ')')
        # Listen for messages on this connection
        processMessages(conn,addr)

def startClientThread(IP):
    client = threading.Thread(target=startClient, args=[IP])
    client.start()

def startClient(pubIP):
    host = str(pubIP)  # Get local machine name '66.75.235.111','72.220.9.29'
    port = 12000  # Reserve a port for your service.
    global clientConn
    clientConn = socket.socket()  # Create a socket object

    clientConn.connect((host, port))

    clientConn.sendall(b'Connected. Wait for data...\n')

    while 1:
        intosend = input("message to send: ")
        #intosend = mainGUI.sendMessage()
        clientConn.sendall(intosend.encode('utf-8'))
        # data received back from sever
        data = clientConn.recv(1024)
        print("Data: ", data.decode('utf-8'))
    clientConn.close()  # Close the socket when done

    print(data.decode("utf-8"))

def sendMessage(message):
    try:
        clientConn.sendall((message.encode('utf-8')))
    except:
        print("Socket not connected yet")

if __name__ == '__main__':
    s = socket.socket()  # Create a socket object
    host = ('192.168.1.31')  # Get local machine name

    port = 12000  # Reserve a port for your service.

    s = socket.socket()
    s.bind((host, port))  # Bind to the port

    s.listen(5)  # Now wait for client connection.

    server = threading.Thread(target=startServer)
    server.start()

    #client = threading.Thread(target=startClient)
    #client.start()

    mainRoot = Tk() #tk
    global mainGUI
    mainGUI = chatGUI(mainRoot) #tk
    mainRoot.mainloop() #tk





