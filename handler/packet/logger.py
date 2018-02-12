import string
from datetime import datetime
from scapy.all import Dot11ProbeReq, Dot11ProbeResp, Dot11Beacon

from util import oui


class Logger(object):
    def __init__(self, db):
        self.db = db
        self.cursor = db.cursor()

        self.cursor.execute(
            'CREATE TABLE IF NOT EXISTS ssid_log (ssid TEXT PRIMARY KEY, '
            'client TEXT, manufacturer TEXT, '
            'entry_date DATETIME, '
            'proximity INT)')

    def process(self, pkt):
        try:
            if pkt.haslayer(Dot11ProbeReq):
                self.add_entry(pkt)

            if pkt.haslayer(Dot11Beacon) or pkt.haslayer(Dot11ProbeResp):
                self.mark_proximity(pkt)

        except Exception, e:
            print str(e)

    def no_entry(self, ssid, client):
        q = self.cursor.execute('SELECT * FROM ssid_log WHERE ssid = ? and client = ?',
                                (ssid, client))
        fetch = q.fetchall()

        return len(fetch) == 0

    def add_entry(self, pkt):
        (ssid, client) = (pkt.sprintf('%Dot11ProbeReq.info%').strip(), pkt.addr2)

        ssid = str(ssid)
        client = str(client)

        if self.no_entry(ssid, client) and self.is_valid(ssid):
            self.cursor.executemany('REPLACE INTO ssid_log VALUES (?, ?, ?, ?, ?)',
                                    [(ssid, client, oui.get_manufacturer(ssid), datetime.now(), 0)])
            self.db.commit()

    def mark_proximity(self, pkt):
        typename = 'Dot11Beacon' if pkt.haslayer(Dot11Beacon) else 'Dot11ProbeResp'

        self.cursor.execute('UPDATE ssid_log SET proximity = ? WHERE ssid = ?',
                            (1, str(pkt.sprintf('%' + typename + '.info%'))))
        self.db.commit()

    @staticmethod
    def is_valid(ssid):
        return all(c in string.printable for c in ssid)
