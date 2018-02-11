class HandlerManager:
    def __init__(self):
        self.handlers = []

    def add(self, packet_handler):
        self.handlers.append(packet_handler)

    def apply(self, pkt):
        for h in self.handlers:
            h.process(pkt)
