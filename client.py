from socket import socket, AF_INET, SOCK_DGRAM, SHUT_RDWR
from Crypto.Hash import SHA256
from random import randint
import thread, sys, json
from sys import argv

from AESCipher import *
# from client_lib import *

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s: s[0:-ord(s[-1])]

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

msg = json.dumps({'key': str(Yc), 'username': username})
users_info = {}


def send(msg):
    msg = json.dumps(msg)
    cipher = AESCipher(Kc)
    msg = cipher.encrypt(msg)
    s.send(msg)

s.send(msg)
msg = s.recv(size)
msg = json.loads(msg)
Ys = long(msg['key'])
Kc = (Ys**Xc) % shared_prime
h = SHA256.new()
h.update(str(Kc))
Kc = h.hexdigest()
# print Yc, ' is my public key'
# print Kc, ' is my private key with the server'
# end key exchange with server


def receive_loop():
    global recipient, Kc
    while 1:
        cipher = AESCipher(Kc)
        data = cipher.decrypt(s.recv(size))
	print "--->"+data+"<---"
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
            'username'  : username,
            'type'      : 'command',
            'command'   : args[0],
            'args'      : args[1:]
        })
    else:
        if recipient == '':
            send({
                'type'      : 'message',
                'message'   : user_input,
		'username'  : username
            })
        else:
            cipher = AESCipher(users_info[recipient]['private_key'])
            send({
                'type'      : 'message',
                'message'   : user_input,
                'recipient' : recipient,
		'username'  : username
            })
