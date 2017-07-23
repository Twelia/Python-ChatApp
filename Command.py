import Token

class Command(Token):
    def __init__(self, sender, receiver, command, args):
        super(self).__init__("command")
        self.struct.update({
            'sender'    : sender,
            'receiver'  : receiver,
            'command'   : command,
            'args'      : args
        })

