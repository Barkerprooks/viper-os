import network

IF = network.WLAN(network.STA_IF)
CONFIG = "/etc/wifi.conf"

def scan():
    IF.active(True)
    ap_list = ["[%s] ssid: %s - signal: %s" % (i, ap[0].decode(), ap[3]) for i, ap in enumerate(IF.scan())]
    IF.active(False)
    return ap_list

def start(ssid='', pswd=''):
    
    if not ssid:
        with open(CONFIG) as stream:
            lines = [l.strip() for l in stream.readlines()]
            ssid = lines[0]
            pswd = lines[1]

    IF.active(True)
    IF.connect(ssid, pswd)

    print("connecting to %s" % ssid)
    while not IF.isconnected() and attempts > 0:
        print('.', end='')
        pass
    
    if not IF.isconnected():
        print("\nfailed to connect")

