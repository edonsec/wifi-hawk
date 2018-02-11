import sqlite3

from Handler.LoggerPacketHandler import LoggerPacketHandler
from Handler.PrinterPacketHandler import PrinterPacketHandler
from scapy.all import *

from Packet.HandlerManager import HandlerManager


class Capture:
    def __init__(self, args):
        self.args = args

        db = sqlite3.connect(self.args.db)
        printer_handler = PrinterPacketHandler()
        logger_handler = LoggerPacketHandler(db)

        self.packet_handler_manager = HandlerManager()
        self.packet_handler_manager.add(printer_handler)
        self.packet_handler_manager.add(logger_handler)

    def is_accepted_packet(self, p):
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
