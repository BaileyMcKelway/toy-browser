import socket
import ssl
import gzip
from urllib.parse import urlparse

class Request:
    def __init__(self, url):
        self.url = url

    def get_parsed_url_contents(self, parsed_url):
        scheme = parsed_url.scheme
        path = parsed_url.path
        host = parsed_url.hostname
        port = parsed_url.port
      
        if port == None:
            port = 80 if scheme == "http" else 443
        return (scheme, path, host, port)

    def build_headers(self, response):
        headers = {}
        while True:
            line = response.readline()
            if line == "\r\n": break
            header, value = line.split(":", 1)
            headers[header.lower()] = value.strip()
        return headers
    
    def build_body(self, response, headers):
        body = response.read()
        body.replace("&lt;", "<").replace("&gt;", ">")
        return body
        
    def get_response(self, s):
      response = s.makefile("r", encoding="utf8", newline="\r\n")
      statusline = response.readline()
      version, status, explanation = statusline.split(" ", 2)
      return (response, status, explanation)
      
    def handle_file(self, path):
        with open(path, "r") as file:
            file = open(path, "r")
            body = file.read()
            headers = ""
        return headers, body
        
    def request(self):
        (scheme, path, host, port) = self.get_parsed_url_contents(urlparse(self.url))
        
        if scheme == 'file':
          return self.handle_file(path)
      
        s = socket.socket(
            family=socket.AF_INET,
            type=socket.SOCK_STREAM,
            proto=socket.IPPROTO_TCP,
        )
        if scheme == "https":
            ctx = ssl.create_default_context()
            s = ctx.wrap_socket(s, server_hostname=host)
            
        s.connect((host, port))
        http_request = ("GET {} HTTP/1.0\r\n".format(path) + "Host: {}\r\n\r\n".format(host)).encode("utf8")
        s.send(http_request)
      
        response, status, explanation = self.get_response(s)
        assert status == "200", "{}: {}".format(status, explanation)
      
        headers = self.build_headers(response)
        body = self.build_body(response, headers)
        
        s.close()
        return (headers, body)





