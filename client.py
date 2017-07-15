from socket import socket, AF_INET, SOCK_DGRAM, SHUT_RDWR
from Crypto.Hash import SHA256
from random import randint
import thread, sys, json
from sys import argv

from AESCipher import *
# from client_lib import *

recipient = ''

if len(argv) != 2:
    username = raw_input('Kindly introduce yourself to the server: ')
else:
    username = argv[1]

shared_prime = 2**1536 - 2**1472 - 1 + 2**64 * ((2**1406) + 741804)
shared_base = 7
Xc = randint(30, 80)
Yc = (shared_base ** Xc) % shared_prime

IP   = 'localhost'
port = 12345
size = 2**16

# print ('Test client sending packets to IP {0}, via port {1}\n'.format(IP, port))

# start key exchange
s = socket()
s.connect((IP, port))

msg = json.dumps({'sharedkey': str(Yc), 'sender': username})
users_info = {}


def send(msg):
    msg = json.dumps(msg)
    cipher = AESCipher(Kc)
    msg = cipher.encrypt(msg)
    s.send(msg)

s.send(msg)
msg = s.recv(size)
msg = json.loads(msg)
Ys = long(msg['sharedkey'])
Kc = (Ys**Xc) % shared_prime
h = SHA256.new()
h.update(str(Kc))
Kc = h.hexdigest()
# end key exchange with server


def receive_loop():
    global recipient, Kc
    while 1:
        cipher = AESCipher(Kc)
        data = cipher.decrypt(s.recv(size))
	msg = json.loads(data)
        print msg
        if msg['response']['messagetype'] == 'success_exit':
            print 'Connection successfully closed.'
            s.shutdown(SHUT_RDWR)
            s.close()
            sys.exit(0)
        elif msg['response']['messagetype'] == 'success_connect':
            Kr = str((long(msg['response']['sharedkey'])**Xc) % shared_prime)
            h = SHA256.new()
            h.update(Kr)
            Kr = h.hexdigest()
            recipient = msg['response']['receiver']
            users_info[recipient] = {
                'public_key'    : msg['response']['sharedkey'],
                'private_key'   : Kr
            }
        elif msg['response']['messagetype'] == 'incoming_connect':
            Kr = str((long(msg['response']['sharedkey'])**Xc) % shared_prime)
            h = SHA256.new()
            h.update(Kc)
            Kc = h.hexdigest()
            users_info[msg['response']['sender']] = {
                'public_key'    : msg['response']['sharedkey'],
                'private_key'   : Kr
            }
        elif msg['response']['messagetype'] == 'incoming_message':
            receiver = msg['response']['receiver']
            sender = msg['response']['sender']
            cipher = AESCipher(users_info[receiver]['private_key'])
            message = cipher.decrypt(msg['response']['msg'])
            print user,'<',sender+':',message
        print msg['response']['messagecontent']

# start listening asynchronously
thread.start_new_thread(receive_loop, ())

while 1:
    user_input = raw_input(username+'> ')
    if user_input.startswith('/'):
        args = user_input.split(' ')
        if args[0] == '/send':
            args.insert(1, recipient)
            cipher = AESCipher(users_info[recipient]['private_key'])
            msg = cipher.encrypt(' '.join(args[2:]))
            del(args[2:])
            args.append(msg)
            send({
                'sender'        : username,
                'messagetype'   : 'command',
                'command'       : args[0],
                'args'          : args[1:]
            })
    else:
        if recipient == '':
            send({
                'messagetype'   : 'message',
                'messagecontent': user_input,
		'sender'        : username,
                'receiver'      : ''
            })
        else:
            cipher = AESCipher(users_info[recipient]['private_key'])
            message = user_input
            send({
                'messagetype'   : 'message',
                'messagecontent': cipher.encrypt(message),
                'receiver'      : recipient,
		'sender'        : username
            })
