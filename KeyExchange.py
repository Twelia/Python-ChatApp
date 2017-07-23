import Token

class KeyExchange(Token):
    def __init__(self, receiver, key, sender):
        super(self).__init__("diffie_hellman")
        self.struct.update({
            'message'   : 'DH Key Exchange',
            'receiver'  : receiver,
            'key'       : key,
            'sender'    : sender
        })
