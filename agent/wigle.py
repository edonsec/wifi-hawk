import requests
from requests.auth import HTTPBasicAuth
from time import sleep

from Data.Entry import Entry
from Data.Location import Location


class WigleException(Exception):
    pass


class Wigle(object):
    API_ENDPOINT = "https://api.wigle.net/api/v2"

    def __init__(self, config, reporting, cache=None):
        self.auth = HTTPBasicAuth(config.name, config.token)
        self.reporting = reporting
        self.cache = cache

    def get_locations_by_ssid(self, ssid, max_results=5, sleep_offset=2, transformer=None):
        results = []
        locations = self.search(ssid, max_results)

        for location in locations:
            coords = Location(location['trilong'], location['trilat'])
            addr = location['addr'] if 'addr' in location else None
            entry = Entry(ssid, coords, addr)

            if 'cache' in location:
                entry.mark_cached()

            if transformer:
                entry = transformer(entry)

            results.append(entry)

            if not entry.is_cached() and sleep_offset:
                sleep(sleep_offset)

        return results

    def search(self, ssid, max_results=5):
        if self.cache:
            cache_result = self.cache.get(ssid)

            if cache_result:
                self.reporting.debug("Utilising cache for ssid: {}".format(ssid))
                self.reporting.debug("Cache result: {}".format(cache_result))

                return cache_result

        return self.search_api(ssid=ssid, resultsPerPage=max_results)

    def search_api(self, **kwargs):
        r = requests.get("{}/network/search".format(self.API_ENDPOINT), auth=self.auth, params=kwargs)
        r.raise_for_status()

        result = r.json()

        self.reporting.debug("Utilising API request for ssid: {}".format(kwargs.get("ssid")))
        self.reporting.debug(result)

        if not result["success"]:
            raise WigleException(result["message"])

        return result['results']
