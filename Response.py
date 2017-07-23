import Token

class Response(Token):

    def __init__(self, receiver, message):
        super(self).__init__()
        self.struct = {
            'receiver'  : sender,
            'message'   : message,
            'sender'    : 'server',
            'msg_info'  : 'response'
        }
