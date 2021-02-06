#!/usr/bin/env python3

import time, ssl, socket, sys
import serial, random

ESP_IP = "192.168.4.1"
MAXBUF = 4069

class ViperShellClient:
    
    def __init__(self, port):
        self.port = port
        
    def get_ps1(self, retry=5):
        tries = retry
        while tries:
            try:
                self.sockfd = socket.socket()
                self.sockfd.settimeout(5)
                self.sockfd.connect((ESP_IP, self.port))
                if tries < retry:
                    print()
                return self.sockfd.recv(MAXBUF).decode("utf-8")
            except KeyboardInterrupt:
                exit(0)
            except:
                dots = ['*' if (i+1) == tries else '.' for i in range(retry)]
                dots.reverse()
                tries -= 1
                data = ">>> connecting." + ''.join(dots) + '.'
                print(data + "\033[%dD" % len(data), end='')
                sys.stdout.flush()
                time.sleep(1)
        print("\n>>> failed to connect")
        return None


    def execute(self, cmd):
        self.sockfd.send(cmd.encode("utf-8"))
        while (out := self.sockfd.recv(MAXBUF)):
            print(out.decode("utf-8"), end='')
            sys.stdout.flush()
        self.sockfd.close()


if __name__ == "__main__":

    shell = ViperShellClient(22)
    
    while 1:
        try:
            ps1 = shell.get_ps1()
            if not ps1:
                exit(0)
            print(ps1, end='')
            sys.stdout.flush()
            cmd = input()
            if not cmd:
                shell.sockfd.close()
                continue
            shell.execute(cmd)
            if cmd == "exit":
                exit(0)
        except KeyboardInterrupt:
            shell.sockfd.close()
            pass
