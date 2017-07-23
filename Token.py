class Token(Object):
    def __init__(self, type):
        self.struct = {
            "type": type
        }

    def __repr__(self):
        return json.dumps(self.struct)
