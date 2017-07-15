class Server:
    def __init__(self):
        self.port = 12345
        self.size = 2**16
        self.username_max_size = 50
        self.host = gethostbyname('0.0.0.0')
        self.commands = {
            '/setname'  : set_username,
            '/connect'  : connect,
            '/list'     : list_users,
            '/help'     : display_help,
            '/send'     : send_to,
            '/exit'     : exit_client
        }

    # add methods accordingly to the commands above
    # check server.py for methods implementation

    def send():
        return

    def set_username():
        return

    def connect():
        return

    def list_users():
        return

    def display_help():
        return

    def send_to():
        return

    def exit_client():
        return

    def on_new_client():
        return

    # method for key sharing and listening (async)
