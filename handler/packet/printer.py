from scapy.all import Dot11ProbeReq, Dot11ProbeResp, Dot11Beacon

from chardet import detect
from util import oui


class Printer:
    def __init__(self):
        self.probe_req = []
        self.probe_res = []
        self.beacon = []

    def process(self, pkt):
        if pkt.haslayer(Dot11ProbeReq):
            self.add_probe_req(pkt)
        elif pkt.haslayer(Dot11ProbeResp):
            self.add_probe_resp(pkt)
        elif pkt.haslayer(Dot11Beacon):
            self.add_beacon(pkt)

    def add_probe_req(self, pkt):
        probe_req = pkt.sprintf('%Dot11ProbeReq.info%')

        if probe_req not in self.probe_req:
            print "[Probe Req] Device: {} ({}); SSID: {}".format(pkt.addr2, oui.get_manufacturer(pkt.addr2),
                                                                 self.normalize(probe_req))
            self.probe_req.append(probe_req)

    def add_probe_resp(self, pkt):
        probe_res = pkt.sprintf('%Dot11ProbeResp.info%')

        if probe_res not in self.probe_res:
            print "[Probe Resp] Device: {} ({}); SSID: {}".format(pkt.addr2, oui.get_manufacturer(pkt.addr2),
                                                                  self.normalize(probe_res))
            self.probe_res.append(probe_res)

    def add_beacon(self, pkt):
        beacon = pkt.sprintf('%Dot11Beacon.info%')

        if beacon not in self.beacon:
            print "[Beacon] Device: {} ({}); SSID: {}".format(pkt.addr2, oui.get_manufacturer(pkt.addr2),
                                                              self.normalize(beacon))
            self.beacon.append(beacon)

    @staticmethod
    def normalize(ssid):
        enc = detect(ssid)

        if enc['encoding'] is not None:
            return ssid.decode(enc['encoding'])
        else:
            return '<unknown encoding>'
