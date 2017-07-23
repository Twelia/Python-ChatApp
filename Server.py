from Crypto import Random
from Crypto.Hash import SHA256
from random import randint
from socket import socket, gethostbyname
import json, sys, thread

import AESCipher, ServerRegistry, Message, KeyExchange, Notification, Command, Response, Token

class Server:
    shared_prime = 2**1536 - 2**1472 - 1 + 2**64 * ((2**1406) + 741804)
    shared_base = 7

    def __init__(self, maxconnections):
        self.port = 12345
        self.size = 2**16
        self.username_max_size = 50
        self.host = gethostbyname('0.0.0.0')
        self.commands = {
            '/setname'  : set_username,
            '/connect'  : connect,
            '/list'     : list_users,
            '/help'     : display_help,
            '/send'     : send_to,
            '/exit'     : exit_client
        }
        self.X = randint(30, 80)
        self.Y = (shared_base ** X) % shared_prime
        self.serverSocket = socket()
        self.serverRegistry = ServerRegistry()
        self.conn = maxconnections # maximum client connections at a time

    # add methods accordingly to the commands above
    # check server.py for methods implementation

    def send(token):
        username = token.struct['receiver']
        key = self.serverRegistry.sRegistry[username]['private_key']
        socket = self.serverRegistry.sRegistry[username]['socket']
        cipher = AESCipher(key)
        msg = cipher.encrypt(repr(token))
        self.serverSocket.sendto(msg, socket)

    def connect(command):
        receiver = command.struct['sender']
        receiver = command.struct['args'][0]
        if self.serverRegistry.sRegistry.has_key(receiver):
            if sender == receiver:
                send(Response(sender, 'Connect Fail: cannot connect to self'))
            else:
                Ysender = self.serverRegistry.sRegistry['sender']['public_key']
                Yreceiv = self.serverRegistry.sRegistry['receiver']['public_key']
                send(KeyExchange(receiver, Ysender, sender))
                send(KeyExchange(sender, Yreceiv, receiver))
        else:
            send(Response(sender, 'Connect Fail: user unavailable at the moment'))


    def list_users(command):
        message = 'Available Users:\n'+'--'+'\n--'.join(self.serverRegistry.sRegistry.keys())
        username = command.struct['receiver']
        send(Response(username, message))

    def display_help(command):
        messsage = '''
        -----------
         HELP MENU
        -----------
        /help           open help menu
        /list           list of connected users
        /connect        connect to user
        /send           send message to user
        /exit           exit client
        '''
        username = command.struct['sender']
        send(Response(username, message))

    def send_to(command):
        send(Message(command.struct['receiver'], command.struct['message'], command.struct['sender']))
        send(Response(command.struct['sender'], 'Message Sent Success'))

    def exit_client(command):
        self.serverRegistry.deleteConnection(command.struct['sender'])
        send(Response(command.struct['sender'], 'Exit Success'))

    def on_new_client(socket, addr, username):
        while 1:
            msg = socket.recv(size)
            cipher = AESCipher(self.serverRegistry.sRegistry[username]['private_key'])
            msg = cipher.decrypt(msg)
            # print addr,' >> ', msg
            msg = json.loads(msg)
            # stuff
        return

    # method for key sharing and listening (async)
