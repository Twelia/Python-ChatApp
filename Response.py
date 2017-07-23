import Token

class Response(Token):
    def __init__(self, receiver, message):
        super(self).__init__("response")
        self.struct.update({
            'receiver'  : sender,
            'message'   : message,
            'sender'    : 'server',
            'msg_info'  : 'response'
        })
