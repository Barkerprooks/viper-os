from src.vos import vsh
import os, socket

class ViperShellServer(vsh.ViperShell):

    def __init__(self, port):
        self.port = port
        self.sockfd = socket.socket()
        super().__init__()

    def start(self):
        print("starting shell server on port %s" % self.port)
        self.sockfd.bind(('', self.port))
        self.sockfd.listen(5)
        self.prompt()

    def prompt(self):
        client, ip = self.sockfd.accept()
        print("%s connected" % ip[0])

        ps1 = str(self.ps1 % os.getcwd()).encode("utf-8")
        client.send(ps1)
        cmd = client.recv(4069).decode("utf-8")
        args = self.parse_args(cmd)

        if args:
            self.execute(args, client)
            client.close()
            return True
        
        client.close()
        return False

