import os
import json
import urllib

from jinja2 import Environment, FileSystemLoader


class GoogleException(Exception):
    pass


class GoogleMap(object):
    def __init__(self, config, reporting, template_dir=None, template_name="geo.html.j2", jinja=None):
        self.config = config
        self.reporting = reporting
        self.template_name = template_name
        self.template_dir = template_dir if template_dir else os.path.dirname(os.path.abspath(__file__)) + '/template'
        self.jinja = jinja if jinja else Environment(loader=FileSystemLoader(self.template_dir), trim_blocks=True)
        self.locations = []

    def make_map(self, map_path):

        geosrc = self.jinja.get_template(self.template_name).render(
            google_key=self.config.javascript_api_key,
            access_points=json.dumps(self.locations),
        )

        with open(map_path, 'w') as mf:
            mf.write(geosrc)

    def add_addr_to_entry(self, x):
        x.addr = self.get_address(x.location.lat, x.location.lng)

        return x

    def get_address(self, lat, lng):
        url = "https://maps.googleapis.com/maps/api/geocode/json" \
              "?latlng={},{}&sensor=true&key={}".format(str(lat),
                                                        str(lng),
                                                        self.config.geocode_api_key)

        response = urllib.urlopen(url)
        data = json.loads(response.read())

        if 'error_message' in data:
            raise GoogleException(data['error_message'])

        try:
            return data['results'][0]['formatted_address']
        except Exception, e:
            raise GoogleException(str(e))

    def add_location(self, entry):
        self.locations.append(entry.to_serializable())
