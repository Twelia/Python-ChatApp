import Token

class KeyExchange(Token):
    def __init__(self, receiver, key, sender):
        super(self).__init__()
        self.struct = {
            'message'   : 'DH Key Exchange',
            'receiver'  : receiver,
            'key'       : key,
            'sender'    : sender
        }
