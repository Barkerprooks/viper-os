#!/usr/bin/env python3

import time, ssl, socket, sys
import serial, random

ESP_IP = "192.168.4.1"
MAXBUF = 4069

class ViperShellClient:
    
    def __init__(self, port):
        self.port = port
        
    def get_ps1(self):
        
        try:
            self.sockfd = socket.socket()
            self.sockfd.connect((ESP_IP, self.port))
        except KeyboardInterrupt:
            exit(0)
        except:
            ind = random.randint(0, 2)
            dot = ''.join(['o' if i == ind else '.' for i in range(3)])
            msg = "connecting" + dot
            print("%s\033[%sD" % (msg, len(msg)), end='')
            sys.stdout.flush()
            time.sleep(2)
            self.get_ps1()

        return self.sockfd.recv(MAXBUF).decode("utf-8")

    def execute(self, cmd):
        
        self.sockfd.send(cmd.encode("utf-8"))
        sys.stdout.flush()
        
        while (out := self.sockfd.recv(MAXBUF)):
            print(out.decode("utf-8"), end='')
            sys.stdout.flush()

        self.sockfd.close()


if __name__ == "__main__":

    shell = ViperShellClient(22)
    connect = 1
    
    while connect:
        try:
            ps1 = shell.get_ps1()
            sys.stdout.flush()
            print(ps1, end='')
            sys.stdout.flush()
            cmd = input()
            if cmd:
                shell.execute(cmd)
            if cmd == "exit":
                connect = 0
        except KeyboardInterrupt:
            pass
        
