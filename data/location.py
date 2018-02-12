class Location(object):
    def __init__(self, lng, lat):
        self.lng = lng
        self.lat = lat

    def to_serializable(self):
        me = self

        return me.__dict__
