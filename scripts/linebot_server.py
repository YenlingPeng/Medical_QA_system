import socketserver
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import API as api

class HandleRequests(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print("GET")
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        url = urllib.parse.unquote(self.path)
        print(url)
        self.wfile.write('<html><head><meta charset="UTF-8"></head>'.encode("utf-8"))
        self.wfile.write(f"<h1>{url}</h1></html>".encode("utf-8"))

        
    def do_POST(self):
        print("POST")
        self._set_headers()
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        msg = self.data_string.decode()
        print(msg)
        qa=api.qa_chatbot_api(msg)
        string = ''
        for ans in qa:
            if 'http' in ans:
                print(ans)
                string += '📚'+ans+'                                                              '
            else:
                string += ans+'                                                              '

        print(string)
        reply = '{"message":' + f'"{string}"' + '}' 
        self.wfile.write(reply.encode())

    def do_PUT(self):
        self.do_POST()

host = '0.0.0.0'
port = 8887
httpd = socketserver.TCPServer((host, port), HandleRequests)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    httpd.shutdown()
