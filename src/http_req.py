import socket
import ssl
import gzip
from urllib.parse import urlparse

def get_parsed_url_contents(parsed_url):
    scheme = parsed_url.scheme
    path = parsed_url.path
    host = parsed_url.hostname
    port = parsed_url.port
    
            
    if scheme == "https":
        ctx = ssl.create_default_context()
        s = ctx.wrap_socket(s, server_hostname=host)
  
    if port == None:
        port = 80 
    return (scheme, path, host, port)

def handleFile(path):
    with open(path, "r") as file:
        file = open(path, "r")
        body = file.read()
        headers = ""
    return headers, body

    
def request(url):
    (scheme, path, host, port) = get_parsed_url_contents(urlparse(url))
    
    if scheme == 'file':
      return handleFile(path)
  
    s = socket.socket(
        family=socket.AF_INET,
        type=socket.SOCK_STREAM,
        proto=socket.IPPROTO_TCP,
    )
        
    s.connect((host, port))
    
    http_request = (
        b"GET " + bytes(path, 'utf-8') + b" HTTP/1.1\r\n" + 
        b"Host: " + bytes(host, 'utf-8') + b"\r\n" + 
        b"Connection: close\r\n" +
        b"User-Agent: Manyk\r\n" +
        b"Accept-Encoding: gzip\r\n" +
        b"\r\n"
    )
  
    s.send(http_request)
  
    response = s.makefile("rb", encoding="utf8", newline="\r\n")
    
    statusline = response.readline().decode()
    
    version, status, explanation = statusline.split(" ", 2)
    assert status == "200", "{}: {}".format(status, explanation)
  
    headers = {}
    while True:
        line = response.readline().decode()
        if line == "\r\n": break
        header, value = line.split(":", 1)
        headers[header.lower()] = value.strip()
  
    body = response.read()
    if 'content-encoding' in headers:
        assert "gzip" in headers.get('content-encoding')
        body = gzip.decompress(body).decode(encoding='utf-8')
    else: 
        body = body.decode(encoding='utf-8')
    s.close()
    return (headers, body)
  

def show(body):
    in_angle = False
    for c in body:
        if c == "<":
            in_angle = True
        elif c == ">":
            in_angle = False
        elif not in_angle:
            print(c, end="")

def load(url):
    headers, body = request(url)
    body = body.replace("&lt;", "<").replace("&gt;", ">")
    show(body)

if __name__ == "__main__":
    import sys
    load(sys.argv[1])


