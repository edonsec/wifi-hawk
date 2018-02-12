import ConfigParser

import os
import sqlite3

from agent.google_map import GoogleMap
from agent.ssid import Ssid
from agent.wigle import WigleException, Wigle
from cache.location import Location
from util import sqlite_factory
from util.pattern import Pattern
from util.stdout_reporting import StdoutReporting
from config.config import Config, GoogleConfig, WigleConfig
from defaults import *


class Plot:
    db = None
    cache = None
    google_agent = None
    wigle_agent = None

    def __init__(self, args):
        self.args = args
        self.reporting = StdoutReporting(verbose=self.args.verbose, debug=self.args.debug)
        self.app_config = Config()
        self.whitelist = Pattern([])
        self.blacklist = Pattern([])

    def setup(self):
        self.ensure_db_exists()

        self.db = sqlite3.connect(self.args.db)
        self.db.row_factory = sqlite_factory.dict_factory
        self.cache = Location(self.db)

        self.setup_config()

        self.wigle_agent = Wigle(self.app_config.wigle, self.reporting, cache=self.cache)
        self.google_agent = GoogleMap(self.app_config.google, self.reporting, template_dir="resources/template")

        if self.args.whitelist_file:
            self.whitelist.load_with_file(self.args.whitelist_file)

        if self.args.blacklist_file:
            self.blacklist.load_with_file(self.args.blacklist_file)

        return self

    def run(self):
        if self.args.flush_cache:
            self.reporting.verbose("Cache now flushed.")
            self.cache.flush()

        ssid_agent = Ssid(self.db)
        entries = []
        last_printed = None

        for client in ssid_agent.get_clients(self.args.mac_addr):
            for ssid in client['ssid']:
                if self.whitelist.not_empty() and not self.whitelist.matches(ssid):
                    self.reporting.debug("Skipping {} - does not match supplied patterns".format(ssid))
                    continue

                if self.blacklist.matches(ssid):
                    self.reporting.debug("Skipping {} - Matches {} rule for blacklist".format(
                        ssid, self.blacklist.get_last_match()))
                    continue

                if last_printed != client['client']:
                    self.reporting.verbose("{surround}\nClient: {mac}\n{surround}\n".format(
                        mac=client['client'],
                        surround="=" * (len(client['client']) + 8)
                    ))

                    last_printed = client['client']

                self.reporting.verbose('SSID: {}'.format(ssid))

                if not self.args.dry:
                    try:
                        entries = self.wigle_agent.get_locations_by_ssid(ssid,
                                                                         sleep_offset=self.args.sleep,
                                                                         transformer=self.google_agent.add_addr_to_entry)
                    except WigleException, e:
                        self.reporting.error("Wigle Error: {}".format(str(e)))

                    for entry in entries:
                        if not entry.is_cached():
                            self.cache.store(entry.ssid, entry.location.lng, entry.location.lat,
                                             entry.addr)

                        self.reporting.verbose(
                            '  > Lng: {}; Lat: {} ({})'.format(entry.location.lng, entry.location.lat, entry.addr))

                        self.google_agent.add_location(entry)
                else:
                    self.reporting.debug("Skipping Wigle calls")

        if not self.args.dry and entries and self.args.plot_map:
            try:
                self.google_agent.make_map(self.args.plot_map)
            except GoogleException, e:
                self.reporting.error("Google Map Error: {}".format(str(e)))
        else:
            self.reporting.debug("Skipping Google calls")

    def setup_config(self):
        config = ConfigParser.ConfigParser()
        user_config_path = os.path.expanduser("~/{}".format(DEFAULT_CONFIG_NAME))

        if os.path.exists(user_config_path) or os.path.exists(self.args.config):
            config.read([user_config_path, self.args.config])

            google_config = GoogleConfig(geocode_api_key=config.get("google", "geocode_api_key"),
                                         javascript_api_key=config.get("google", "javascript_api_key"))
            wigle_config = WigleConfig(
                name=config.get("wigle", "name"),
                token=config.get("wigle", "token")
            )

            self.app_config.google = google_config
            self.app_config.wigle = wigle_config
        else:
            self.reporting.error("Please provide a configuration - either via -c/--config argument or create "
                                 "~/.".format(DEFAULT_CONFIG_NAME))

    def ensure_db_exists(self):
        if not os.path.exists(self.args.db):
            self.reporting.error("{} does not exist".format(self.args.db))
