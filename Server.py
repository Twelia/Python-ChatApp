from Crypto import Random
from Crypto.Hash import SHA256
from random import randint
from socket import socket, gethostbyname
import json, sys, thread

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
        self.socket = socket()
        self.registry = ServerRegistry()
        self.conn = maxconnections # maximum client connections at a time

    # add methods accordingly to the commands above
    # check server.py for methods implementation

    def send(msg):
        key = connected_sockets[msg['receiver']]['private_key']
        cipher = AESCipher(key)
        msg = cipher.encrypt(json.dumps(msg))
        self.socket.send(msg)

    def set_username():
        return

    def connect():
        return

    def list_users():
        return

    def display_help():
        return

    def send_to():
        return

    def exit_client():
        return

    def on_new_client():
        return

    # method for key sharing and listening (async)
