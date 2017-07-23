from socket import socket, AF_INET, SOCK_DGRAM, SHUT_RDWR
from Crypto.Hash import SHA256
from random import randint
from sys import argv
import json, sys, thread

import AESCipher, ClientRegistry, Message, KeyExchange, Notification, Command, Response, Token


class Client:
    shared_prime = 2**1536 - 2**1472 - 1 + 2**64 * ((2**1406) + 741804)
    shared_base = 7

    def __init__(self, name):
        self.port = 12345
        self.size = 2**16
        self.IP = 'localhost'
        self.recipient = ''
        self.username = name
        self.Xc = randint(30, 80)
        self.Yc = (shared_base ** X) % shared_prime
        self.serverSharedKey = ''
        self.clientSocket = socket()
        self.socket.connect((IP, port))
        self.clientRegistry = ClientRegistry()


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

    def send(token):
        cipher = AESCipher(self.serverSharedKey)
        msg = cipher.encrypt(repr(token))
        self.socket.send(msg)

    def receive_loop():
        connect_server()
        while 1:
            cipher = AESCipher(self.serverSharedKey)
            data = cipher.decrypt(self.clientSocket.recv(self.size))
            msg = json.loads(data)
            if msg.struct['message'] == 'Exit Success':
                print 'Connection successfully closed.'
                self.socket.shudown(SHUT_RDWR)
                self.socket.close()
                sys.exit(0)
            elif msg.struct['message'] == 'DH Key Exchange':
                K = str((long(msg.struct['key'])**self.Xc) % shared_prime)
                h = SHA256.new()
                h.update(K)
                K = h.hexdigest()
                sender = msg.struct['sender']
                self.clientRegistry[sender] = {
                    'public_key'    : msg.struct['key'],
                    'private_key'   : K
                }
            else:
                sender = msg.struct['sender']
                key = self.clientRegistry[sender]['private_key']
                cipher = AESCipher(key)
                message = cipher.decrypt(msg.struct['message'])
                print message

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

    def start_client():
        thread.start_new_thread(receive_loop, ())
        input_loop()
