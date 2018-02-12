class Entry(object):
    def __init__(self, ssid, location, addr, cache=False):
        self.ssid = ssid
        self.location = location
        self.addr = addr
        self.cache = cache

    def mark_cached(self):
        self.cache = True

    def is_cached(self):
        return self.cache

    def to_serializable(self):
        serializable = self.__dict__
        serializable['location'] = serializable['location'].to_serializable()

        return serializable
