from socket import socket, AF_INET, SOCK_DGRAM, SHUT_RDWR
from Crypto.Hash import SHA256
from random import randint
from sys import argv
import json, sys, thread

from AESCipher import *
from ClientRegistry import *


class Client:
    shared_prime = 2**1536 - 2**1472 - 1 + 2**64 * ((2**1406) + 741804)
    shared_base = 7

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
        while 1:
            cipher = AESCipher(self.K)
            data = cipher.decrypt(self.socket.recv(self.size))
            msg = json.loads(data)
            print msg
        # more stuff


    def input_loop():

        return
