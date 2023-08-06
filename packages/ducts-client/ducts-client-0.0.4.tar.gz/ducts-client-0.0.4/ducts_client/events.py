class DuctEvent:
    pass

class DuctConnectionEvent(DuctEvent):
    def __init__(self, state, source):
        super().__init__()
        self.state = state
        self.source = source

class DuctMessageEvent(DuctEvent):
    def __init__(self, rid, eid, data):
        super().__init__()
        self.rid = rid
        self.eid = eid
        self.data = data
