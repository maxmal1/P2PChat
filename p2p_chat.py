import socket
import threading
import queue
import random
import sys
#import time

class P2P:
    # Set up server socket
    def __init__(self, SERVER_HOST, SERVER_PORT, CLIENT_HOST, CLIENT_PORT):
        self.SERVER_HOST = SERVER_HOST
        self.CLIENT_HOST = CLIENT_HOST
        self.SERVER_PORT = SERVER_PORT
        self.CLIENT_PORT = CLIENT_PORT
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



    def startServer(self):

        messages = queue.Queue()
        clients = []

        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind((self.SERVER_HOST, self.SERVER_PORT))
        
        #server.bind(("localhost", 9999))
 
        def receive():
            while True:
                try:
                    message,addr = server.recvfrom(1024)
                    messages.put((message,addr))
                except:
                    pass
        def broadcast():
            
            #server.sendto(f"SIGNUP_TAG:Server".encode(), ("localhost",9998))
            while True:
                """message = input("")
                if message == "!q":
                    exit()
                else:
                    server.sendto(f"Server: {message}".encode(), ("localhost",9998))"""
                while not messages.empty():
                    message, addr = messages.get()
                    #print(clients)
                    print(message.decode())
                    if addr not in clients:
                        clients.append(addr)
                    for client in clients[1:len(clients)]:
                        try:
                            if message.decode().startswith("SIGNUP_TAG:"):
                                name = message.decode()[message.decode().index(":")+1:]
                                server.sendto(f"{name} joined!".encode(),client)
                            else:
                                server.sendto(message,client)
                        except:
                            clients.remove(client)
                            
        def message():
            while True:
                message = input("")
                
                if message == "!q":
                    exit()
                else:
                    server.sendto(f"server: {message}".encode(), (self.SERVER_HOST,self.SERVER_PORT))
                    #server.sendto(f"server: {message}".encode(), ("localhost",9999))
                    #time.sleep(5)


            


        t1 = threading.Thread(target = receive)
        t2 = threading.Thread(target = broadcast)
        t3 = threading.Thread(target = message)

        t1.start()
        t2.start()
        t3.start()   
        
    def startClient(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        client.bind((self.CLIENT_HOST,self.CLIENT_PORT))
        #client.bind(("localhost",random.randint(8000, 9000)))
        name = input("nickanme: ")
        def receive():
            while True:
                try: 
                    message, _ = client.recvfrom(1024)
                    print(message.decode())
                    
                except:
                    pass
        t = threading.Thread(target = receive)
        t.start()

        client.sendto(f"SIGNUP_TAG:{name}".encode(), (self.SERVER_HOST,self.SERVER_PORT))
        #client.sendto(f"SIGNUP_TAG:{name}".encode(), ("localhost",9999))

        while True:
            message = input("")
            if message == "!q":
                print("quitting")
                sys.exit()
            else:
                client.sendto(f"{name}: {message}".encode(), (self.SERVER_HOST,self.SERVER_PORT))
                #client.sendto(f"{name}: {message}".encode(), ("localhost",9999))
                

if __name__ == '__main__':
    HOST = input('Please insert IP address to host/connect server: ')
    SERVER_PORT = int(input('Please insert Server Port Number: '))
    print(f'Your entered HOST IP address: {HOST}, your entered PORT number: {SERVER_PORT}')
    

    option = input("Would you like to connect to a server (c) or set up a server (s)?")
    if option == 's':
        p2p = P2P(HOST,SERVER_PORT,'0',0)
        p2p.startServer()
        """p2p = P2P(HOST,SERVER_PORT,0)
        p2p.startClient()"""

    elif option == 'c':
        CLIENT_HOST = int(input('Please insert Your IP Address: '))
        CLIENT_PORT = int(input('Please insert Your Port Number: '))
        p2p = P2P(HOST,SERVER_PORT,CLIENT_HOST,CLIENT_PORT)
        p2p.startClient()
        
    
    # Start the threads for receiving and sending messages
    """receive_thread = threading.Thread(target=p2p.receive_messages)
    send_thread = threading.Thread(target=p2p.send_message)
    receive_thread.start()
    send_thread.start()"""