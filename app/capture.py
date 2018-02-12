import sqlite3

from scapy.all import *

from handler.manager import Manager
from handler.packet.logger import Logger
from handler.packet.printer import Printer


class Capture(object):
    def __init__(self, args):
        self.args = args

        db = sqlite3.connect(self.args.db)
        printer_handler = Printer()
        logger_handler = Logger(db)

        self.packet_handler_manager = Manager()
        self.packet_handler_manager.add(printer_handler)
        self.packet_handler_manager.add(logger_handler)

    @staticmethod
    def is_accepted_packet(p):
        return (p.haslayer(Dot11Beacon) or
                ((p.haslayer(Dot11ProbeReq) and p.getlayer(Dot11ProbeReq).info))
                or p.haslayer(Dot11ProbeResp))

    def handle_packet(self, pkt):
        return self.packet_handler_manager.apply(pkt)

    def run(self):

        sniffkw = {
            "prn": self.handle_packet,
            "lfilter": self.is_accepted_packet
        }

        if self.args.pcap:
            sniffkw["offline"] = self.args.pcap
        elif self.args.interface:
            sniffkw["iface"] = self.args.interface

        sniff(**sniffkw)
