import select, network, os, sys, time
from machine import Pin, sleep

from src.vos import vsh
from src.net import vshd

wifi = network.WLAN(network.AP_IF)
wifi.active(True)
print(wifi.ifconfig())

led = Pin(2, Pin.OUT)

vsh_srv = vshd.ViperShellServer(22)
vsh_srv.start()

rd_socks = [
    vsh_srv.sockfd
]

wr_socks = [
    sys.stdout
]

rd,wr,_ = select.select(rd_socks, wr_socks, [])

while 1:
    led.off()
    if vsh_srv.client in rd:
        vsh_srv.prompt()
        led.on()
