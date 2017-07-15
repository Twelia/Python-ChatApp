class ClientRegistry:
    def __init__(self):
        self.cRegistry = {}

    def addConnection(username, Y, K):
        self.cRegistry[username] = {
            'public_key'    : Y,
            'private_key'   : K
        }
