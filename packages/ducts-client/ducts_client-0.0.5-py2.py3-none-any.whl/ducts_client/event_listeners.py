class DuctEventListener:
    def __init__(self):
        self.funcs = {}
    async def on(self, names, func):
        if not isinstance(names, list):  names = [names]
        for name in names:
            if name not in self.funcs:
                raise Exception(f"[{name}]")
            self.funcs[name] = func

class ConnectionEventListener(DuctEventListener):
    async def onopen(self, event):
        pass

    async def onclose(self, event):
        pass

    async def onerror(self, event):
        pass

    async def onmessage(self, event):
        pass

