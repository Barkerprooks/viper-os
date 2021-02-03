import os, sys

class ViperShell:

    def __init__(self):
        self.ps1 = "esp32:%s> "
        self.sid = 1
        self.pswd = ""
        self.path = "/bin/"

    def parse_args(self, cmd):
        arg = ''
        args = []
        in_quote = False
        
        for token in cmd.split():
            if token[0] == '"':
                in_quote = True
                token = token[1:]
            if token[-1] == '"':
                in_quote = False
                arg += token[:-1]
            if in_quote:
                arg += token + ' '
            else:
                if arg:
                    args.append(arg)
                    arg = ''
                else:
                    args.append(token)

        if args[0] in ["exit", "quit"]:
            return False
        
        args[0] = self.path + args[0]

        return args

    def execute(self, args, stream):
       
        if stream != sys.stdout:
            print("command sent: %s" % args)
            os.dupterm(stream)
            
        try:
            with open(args[0]) as handle:
                try:
                    exec(handle.read(), {"args": args})
                except:
                    stream.write(b"failed to execute: %s\n" % args[0])
        except:
            stream.write(b"command not found: %s\n" % args[0])

    def prompt(self):
        if self.session_id: 
            cmd = input(self.ps1 % os.getcwd())
            args = self.parse_args(cmd)
            
            if args[0] == self.path + "exit":
                return False
            
            try:
                self.execute(args, sys.stdout)
            except:
                pass
            return True
        


def spawn():
    shell = ViperShell()
    while shell.prompt(): pass
