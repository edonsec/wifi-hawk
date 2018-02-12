class GoogleConfig(object):
    def __init__(self, geocode_api_key=None, javascript_api_key=None):
        self.geocode_api_key = geocode_api_key
        self.javascript_api_key = javascript_api_key


class WigleConfig:
    def __init__(self, name=None, token=None):
        self.name = name
        self.token = token


class Config:
    def __init__(self, wigle=None, google=None):
        self.wigle = wigle if wigle else WigleConfig()
        self.google = google if google else GoogleConfig()
