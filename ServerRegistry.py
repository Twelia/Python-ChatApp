class ServerRegistry:
    def __init__(self):
        self.sRegistry = {}

    def addConnection(username, socket, Y, K):
        self.sRegistry[username] = {
            'socket'        : socket,
            'public_key'    : Y,
            'private_key'   : K
        }

    def deleteConnection(username):
        del connected_sockets[username]