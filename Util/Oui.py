from netaddr import EUI


def get_manufacturer(mac):
    try:
        eui = EUI(mac)
        return eui.oui.registration()['org']
    except:
        return '<unknown>'
