import select, network, os, sys, time
from src.vos import vsh
from src.net import vshd

wifi = network.WLAN(network.AP_IF)
wifi.active(True)
print(wifi.ifconfig())

shell = vshd.ViperShellServer(22)
shell.start()

services = [shell.sockfd]

r,_,_ = select.select(services, [], [])

while True:
    if shell.sockfd in r:
        shell.prompt()
