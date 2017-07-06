from socket import socket, AF_INET, SOCK_DGRAM, SHUT_RDWR
from sys import argv
import thread, sys, json, OpenSSL, hashlib, base64

# import importlib
# importlib.import_module(AESCipher)
from AESCipher import *


def receive_loop():
    while 1:
        cipher = AESCipher(Kc)
        data = cipher.decrypt(s.recv(size))
        msg = json.loads(data)
        if msg['response']['message'] == 'success_exit':
            print 'Connection successfully closed.'
            s.shutdown(SHUT_RDWR)
            s.close()
            sys.exit(0)
        elif msg['response']['message'] == 'success_connect':
            Kr = str((long(msg['response']['key'])**Xc) % shared_prime)
            h = SHA256.new()
            h.update(Kr)
            Kr = h.hexdigest()
            recipient = msg['response']['recipient']
            users_info[recipient] = {
                'public_key'    : msg['response']['key'],
                'private_key'   : Kr
            }
        elif msg['response']['message'] == 'incoming_connect':
            Kr = str((long(msg['response']['key'])**Xc) % shared_prime)
            h = SHA256.new()
            h.update(Kc)
            Kc = h.hexdigest()
            users_info[msg['response']['username']] = {
                'public_key'    : msg['response']['key'],
                'private_key'   : Kr
            }
        elif msg['response']['message'] == 'incoming_message':
            user = msg['response']['username']
            sender = msg['response']['sender']
            cipher = AESCipher(users_info[user]['private_key'])
            message = cipher.decrypt(msg['response']['msg'])
            print user,'<',sender+':',message
        print msg['response']['message']
