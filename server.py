from socket import socket, gethostbyname
from Crypto.Hash import SHA256
from Crypto import Random
from random import randint
import thread, sys, json

# from server_lib import *
from AESCipher import *

port = 12345
size = 2**16
username_max_size = 50

s = socket()
host = gethostbyname('0.0.0.0')


def send(msg, s):
    print msg
    key = connected_sockets[msg['response']['receiver']]['private_key']
    cipher = AESCipher(key)
    msg = json.dumps(msg)
    msg = cipher.encrypt(msg)
    print ""
    print msg
    print ""
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
            return {
                'messagecontent': 'You cannot connect to yourself, dumbass.',
                'messagetype'   : 'connect_fail'
            }
        else:
            Yconn = connected_sockets[args[0][0]]['public_key']
            Yuser = connected_sockets[args[0][1]]['public_key']
            msg = {
                'response': {
                    'messagetype'   : 'incoming_connect',
                    'sharedkey'     : Yuser,
                    'sender'        : args[0][0],
                }
            }
            send(msg, connected_sockets[args[0][0]]['socket'])
            return {
                'messagetype'   : 'success_connect',
                'sharedkey'     : Yconn,
                'sender'        : args[0][1],
                'receiver'      : args[0][0]
            }
    else:
        return {
            'messagecontent': 'User not available or not online at the moment',
            'messagetype'   : 'connect_fail'
        }


def send_to(*args):
    msg = {
        'response' : {
            'receiver'      : args[0][0],
            'sender'        : args[0][-1],
            'messagecontent': args[0][1],
            'messagetype'   : 'incoming_message',
        }
    }
    soc = connected_sockets[args[0][0]]['socket']
    print ""
    print ""
    print msg
    send(msg, soc)
    return {
        'receiver'      : args[0][-1],
        'messagetype'   : 'message_sent_success'
    }


def list_users(*args):
    return {
        'receiver'      : args[0][0],
        'messagecontent': 'Available Users:\n'+'--'+'\n--'.join(connected_sockets.keys())
    }


def display_help(*args):
    return {
    'receiver': args[0][0],
    'message' : '''
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
        'response': {
            'messagetype'   : 'success_exit',
            'receiver'      : args[0][0]
        }
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


def on_new_client(clientsocket, addr, user):
    while True: # this while is a listen loop to any client
        msg = clientsocket.recv(size)
        print msg
        # decrypt msg
        cipher = AESCipher(connected_sockets[user]['private_key'])
        msg = cipher.decrypt(msg)
        print addr,' >> ', msg
        msg = json.loads(msg)
        if msg['messagetype'] == 'command':
            msg['args'].append(msg['sender'])
            response = {
                'messagetype'   : 'response',
                'response'      : commands[msg['command']](msg['args'])
            }
            send(response, clientsocket)
            if msg['command'] == '/exit':
                exit()
        elif msg['messagetype'] == 'incoming_connect' or msg['messagetype'] == 'success_connect':
            response = msg
        elif msg['messagetype'] == 'message':
            if msg['receiver'] == '':
                response = {
                    'messagetype'   : 'send_failed',
                    'messagecontent': 'Could not send: no recipient found.'
                }
            else:
                response = {
                    'messagetype'   : 'received',
		    'sender'        : msg['sender']
                }
        send(response, clientsocket)

print 'Test_Server started, waiting for client connections.'
try:
    s.bind((host, port))
except __import__('socket').error as msg:
    print 'Bind failed. Error code: '+ str(msg[0])+ '. Message: '+ (msg[1])
    sys.exit()
print 'Socket bind successful.'
s.listen(10) # number of simultaneous TCP connections

shared_prime = 2**1536 - 2**1472 - 1 + 2**64 * ((2**1406) + 741804)
shared_base = 7
Xs = randint(30, 80)
Ys = (shared_base ** Xs) % shared_prime

connected_sockets = {} # initially empty
user = ""

while True:
    # start key exchange
    (c, addr) = s.accept()
    msg = c.recv(size)
    msg = json.loads(msg)
    Yc = long(msg['sharedkey'])
    c.send(json.dumps({
        'sharedkey': str(Ys)
    }))
    Ks = (Yc**Xs) % shared_prime
    print Yc
    print Ks
    h = SHA256.new()
    h.update(str(Ks))
    Ks = h.hexdigest()
    # register client
    user = msg['sender']
    connected_sockets[user] = {
		'address'       : addr,
		'socket'        : c,
		'private_key'   : Ks,
		'public_key'    : Yc
    }
    # end key exchange

    # give client a new space for itself
    thread.start_new_thread(on_new_client, (c, addr, user))
    user = ""
    # at this point, we can accept another client

