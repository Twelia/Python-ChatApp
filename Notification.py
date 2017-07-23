import Token

class Notification(Token):
    def __init__(self, msgtype, receiver, message):
        super(self).__init__("notification")
        self.struct.update({
            'msgtype' : msgtype,
            'receiver' : receiver,
            'message' : message
        })
