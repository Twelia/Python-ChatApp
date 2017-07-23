import Token

class Command(Token):
    def __init__(self, sender, receiver, command, args):
        super(self).__init__()
        self.struct = {
            'sender'    : sender,
            'receiver'  : receiver,
            'command'   : command,
            'args'      : args
        }

    def __init__(self, sender, command, args):
        super(self).__init__()
        self.struct = {
            'sender'    : sender,
            'receiver'  : None,
            'command'   : command,
            'args'      : args
        }
