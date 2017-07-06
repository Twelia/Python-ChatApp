from socket import socket, AF_INET, SOCK_DGRAM, SHUT_RDWR
from sys import argv
import thread, sys, json, OpenSSL, hashlib, base64

# import importlib
# importlib.import_module(AESCipher)
from AESCipher import *

port = 12345
size = 2**16

def send(msg, s):
    key = connected_sockets[msg['response']['username']]['private_key']
    cipher = AESCipher(key)
    msg = json.dumps(msg)
    msg = cipher.encrypt(msg)
    s.send(msg)

def set_username(*args):
    connected_sockets[args[0][0]] = connected_sockets[args[0][1]]
    del connected_sockets[args[0][1]]
    return {
        'message': 'Username successfully changed from '+args[0][1]+' to '+args[0][0]
    }

def connect(*args):
    if connected_sockets.has_key(args[0][0]):
        if args[0][0] == args[0][1]:
            return 'You cannot connect to yourself, dumbass.'
        else:
            Yconn = connected_sockets[args[0][0]]['public_key']
            Yuser = connected_sockets[args[0][1]]['public_key']
            msg = {
                'response': {
                    'message'   : 'incoming_connect',
                    'key'       : Yuser,
                    'username'  : args[0][0],
                    'type'      : 'DH Key Exchange'
                }
            }
            send(msg, connected_sockets[args[0][0]]['socket'])
            return {
                'message'   : 'success_connect',
                'key'       : Yconn,
                'type'      : 'DH Key Exchange',
                'username'  : args[0][1],
                'recipient' : args[0][0]
            }
    else:
        return {
            'message': 'User not available or not online at the moment'
        }

def send_to(*args):
    # A sends message to B
    msg = {
        'response' : {
            'username'  : args[0][0],
            'sender'    : args[0][-1],
            'msg'       : args[0][1],
            'message'   : 'incoming_message',
        }
    }
    soc = connected_sockets[args[0][0]]['socket']
    send(msg, soc)
    return {
        'username' : args[0][-1],
        'message' : 'message_sent_success'
    }

def list_users(*args):
    return {
        'username' : args[0][0],
        'message': 'Available Users:\n'+'--'+'\n--'.join(connected_sockets.keys())
    }

def display_help(*args):
    return {
    'username' : args[0][0],
    'message': '''
    -----------
     HELP MENU
    -----------
    /help            open help menu
    /list            list of connected users
    /connect         connect to a certain user
    /setname         set your username
    /send            send to current recipient (use connect)
    /exit            exit client
    more options etc'''
    }

def exit_client(*args):
    del connected_sockets[args[0][0]]
    return {
        'message'   : 'success_exit',
        'username'  : args[0][0]
    }

commands = {
    '/setname'      : set_username,
    '/connect'      : connect,
    '/list'         : list_users,
    '/help'         : display_help,
    '/send'         : send_to,
    '/exit'         : exit_client
    # more methods later
}

def on_new_client(clientsocket, addr):
    while True: # this while is a listen loop to any client
        msg = clientsocket.recv(size)
        # decrypt msg
        print addr,' >> ', msg
        msg = json.loads(msg)
        if msg['type'] == 'command':
            msg['args'].append(msg['username'])
            response = {
                'type': 'response',
                'response': commands[msg['command']](msg['args'])
            }
            send(response, clientsocket)
            if msg['command'] == '/exit':
                exit()
        elif msg['type'] == 'DH Key Exchange':
            response = msg
        else:
            response = {
                'type': 'response',
                'response': {
                    'message': 'received'
                }
            }
            send(response, clientsocket)
