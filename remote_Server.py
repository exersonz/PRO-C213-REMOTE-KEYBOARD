import socket
from  threading import Thread
from pynput.mouse import Button, Controller
from screeninfo import get_monitors
from pynput.keyboard import Key, Controller

SERVER = None
IP_ADDRESS = "192.168.68.105"
PORT = 8000
screen_width = None
screen_height = None

keyboard = Controller()

def recvMessage(client_socket):
    global keyboard
    while True:
        try:
            message = client_socket.recv(2046).decode()
            if(message):
                keyboard.press(message)
                keyboard.release(message)
                print(message)
        except Exception as error:
            pass

def getDeviceSize():
    global screen_height
    global screen_width
    
    for m in get_monitors():
        print(m)
        screen_height = int(str(m).split(",")[3].strip().split('height=')[1])
        screen_width = int(str(m).split(",")[2].strip().split('width=')[1])

def acceptConnections():
    global SERVER
    while True:
        client_socket, addr = SERVER.accept()
        print(f"Connection established with {client_socket} : {addr}")
        
        # handling multiple client requests simultaneously
        thread1 = Thread(target=recvMessage, args=(client_socket,))
        thread1.start()

def setup():
    print("\n\t\t\t\t\t\tWelcome to remote keyboard!\n")
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))
    SERVER.listen(100)
    print("\n\t\t\t\t\t\tServer is waiting for incoming connections...\n")
    acceptConnections()
    getDeviceSize()

setup()