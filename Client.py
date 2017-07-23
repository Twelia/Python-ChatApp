from socket import socket, AF_INET, SOCK_DGRAM, SHUT_RDWR
from Crypto.Hash import SHA256
from random import randint
from sys import argv
import json, sys, thread

from AESCipher import *
from ClientRegistry import *


class Client:
    def __init__(self, name):
        self.port = 12345
        self.size = 2**16
        self.IP = 'localhost'
        self.recipient = ''
        self.username = name
        self.X = randint(30, 80)
        self.Y = (shared_base ** X) % shared_prime
        self.K = ''
        self.socket = socket()
        self.socket.connect((IP, port))
        self.registry = ClientRegistry()


    # methods

    def connect_server():
        msg = json.dumps({'sharedkey': str(Y), 'sender': username})
        self.socket.send(msg)
        msg = json.loads(self.socket.recv(self.size))
        Ys = long(msg['sharedkey'])
        self.K = (Ys**X) % shared_prime
        h = SHA256.new()
        h.update(str(self.K))
        self.K = h.hexdigest()

    def send(msg):
        msg = json.dumps(msg)
        cipher = AESCipher(K)
        msg = cipher.encrypt(msg)
        s.send(msg)

    def receive_loop():
        connect_server()
        while 1:
            cipher = AESCipher(self.K)
            data = cipher.decrypt(self.socket.recv(self.size))
            msg = json.loads(data)
            print msg
        # more stuff


    def input_loop():
        user_input = raw_input(self.username+'> ')
        if user_input.startswith('/'):
            args = user_input.split(' ')
            if args[0] == '/send_to':
                receiver = args[1]
                Kreceiv = self.clientRegistry['receiver']['private_key']
                cipher = AESCipher(Kreceiv)
                message = args[2:]
                message = cipher.encrypt(message)
                # send(Message(receiver, self.username, message))
                send(Command(self.username, receiver, '/send_to', message))
            else:
                send(Command(self.username, '/send_to', message))
        else:
            print "Please issue a command."
        # idem
    def start_client():
        thread.start_new_thread(receive_loop, ())
        input_loop()
