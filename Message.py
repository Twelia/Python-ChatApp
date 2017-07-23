import Token

class Message(Token):
    def __init__(self, receiver, sender, message):
        super(self).__init__()
        self.struct = {
            'receiver'  : receiver,
            'sender'    : sender,
            'message'   : message,
        }
