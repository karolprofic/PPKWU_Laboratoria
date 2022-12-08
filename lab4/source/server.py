#!/usr/bin/env python3
import http.server
import json
import socketserver
import os
import time
from urllib.parse import urlparse
from urllib.parse import parse_qs

# print('source code for "http.server":', http.server.__file__)

class web_server(http.server.SimpleHTTPRequestHandler):

    def prepare_headers(self):
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=UTF-8")
        self.end_headers()

    def send_error_msg(self):
        self.prepare_headers()
        self.wfile.write("Error occurred".encode())

    def do_GET(self):

        print("Request url: " + self.path)

        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        print(params)

        if len(params) != 2:
            self.send_error_msg()
            return
        if 'num1' not in params.keys():
            self.send_error_msg()
            return
        if 'num2' not in params.keys():
            self.send_error_msg()
            return
        try:
            number_1 = int(params['num1'][0])
            number_2 = int(params['num2'][0])
        except ValueError:
            self.send_error_msg()
            return
        if number_2 == 0:
            self.send_error_msg()
            return
        
        self.prepare_headers()
        self.wfile.write("Ok".encode())


# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("", PORT), web_server)
tcp_server.serve_forever()
