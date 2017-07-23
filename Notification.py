import Token

class Notification(Token):
    def __init__(self, msgtype, receiver, message):
        super(self).__init__()
        self.struct = {
            'msgtype' : msgtype,
            'receiver' : receiver,
            'message' : message
        }
