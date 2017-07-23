class Token(Object):
    def __init__(self):
        self.struct = {}

    def __repr__(self):
        return json.dumps(self.struct)
