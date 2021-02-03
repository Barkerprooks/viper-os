import ssl, socket

DEFAULT_HEADERS = {"User-Agent": "Esp32"}

class URL:
    def __init__(self, url):
        parts = url.split(':') 
        if len(parts) >= 2:
            if parts[0] not in ["http", "https"]:
                print("protocol must be either http or https")
                return None
            self.host = parts[1][2:]
            self.port = 443 if parts[0] == "https" else 80
            self.ssl = True if parts[0] == "https" else False
            if len(parts) >= 3:
                self.port = int(parts[2].split('/')[0])
        else:
            print("improper url format")
            return None

class HTTPRequest:
    def __init__(self, url, headers, cookies, data):
        self.url = URL(url)


def get(url, headers=DEFAULT_HEADERS, cookies={}, data={}):

    request = HTTPRequest(url, headers, cookies, data)
    sockfd = socket.socket()

    if request.url.ssl:
        sockfd = ssl.wrap_socket(sockfd)

    sockfd.connect((request.url.host, request.url.port))
    sockfd.send(b"GET /%s HTTP/1.1\r\nHost: %s\r\n\r\n" % (b'', request.url.host.encode("utf-8")))
    headers = sockfd.recv(4068)
    response = sockfd.recv(4068)
    print(response.decode("utf-8"))

    sockfd.close()
