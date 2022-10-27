#!/usr/bin/env python3
import http.server
import socketserver
import os
import time


# print('source code for "http.server":', http.server.__file__)

class web_server(http.server.SimpleHTTPRequestHandler):

    def prepare_headers(self):
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=UTF-8")
        self.end_headers()

    def do_GET(self):

        print("Request url: " + self.path)

        if self.path == '/':
            self.prepare_headers()
            self.wfile.write(b"Hello World!")
        elif self.path.startswith('/?cmd=time'):
            self.prepare_headers()
            named_tuple = time.localtime()
            time_string = time.strftime("%H:%M:%S", named_tuple)
            self.wfile.write(time_string.encode("utf-8"))
        elif self.path.startswith('/?cmd=rev'):
            self.prepare_headers()
            parameters = self.path.split("&str=")
            if len(parameters) == 1:
                self.wfile.write(b"Not found str parameter!")
            else:
                reversed_string = parameters[1][::-1]
                self.wfile.write(reversed_string.encode("utf-8"))
        else:
            super().do_GET()


# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("", PORT), web_server)
tcp_server.serve_forever()
