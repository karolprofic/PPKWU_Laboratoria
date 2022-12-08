#!/usr/bin/env python3
import http.server
import json
import socketserver
import os
import time
from urllib.parse import urlparse
from urllib.parse import parse_qs

# print('source code for "http.server":', http.server.__file__)

def count_lowercase(string):
    return sum(1 for c in string if c.islower())

def count_uppercase(string):
    return sum(1 for c in string if c.isupper())

def count_digit(string):
    return sum(1 for c in string if c.isdigit())

def count_special(string):
    special = "!\"£$%&/()='?^+*[]{}#@-_.:,;"
    count = 0
    for character in string:
        if character in special:
            count += 1
    return count

class web_server(http.server.SimpleHTTPRequestHandler):

    def prepare_headers(self):
        self.protocol_version = 'HTTP/1.1'
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=UTF-8")
        self.end_headers()

    def send_error_msg(self):
        self.prepare_headers()
        self.wfile.write("Error occurred".encode())

    def calculator(self, params):
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
            number_1 = int(params['num1'])
            number_2 = int(params['num2'])
        except ValueError:
            self.send_error_msg()
            return
        if number_2 == 0:
            self.send_error_msg()
            return

        return json.dumps({
            "sum": number_1 + number_2,
            "sub": number_1 - number_2,
            "mul": number_1 * number_2,
            "div": int(number_1 / number_2),
            "mod": number_1 % number_2
        })

    def do_POST(self):
        self.prepare_headers()
        data_len = self.rfile.read(int(self.headers['Content-Length']))
        input_json = json.loads(data_len)
        self.wfile.write(json.dumps(input_json).encode())
        print(input_json)
        if 'str' in input_json and 'num1' in input_json and 'num2' in input_json:
            print("1")

            return
        if 'num1' in input_json and 'num2' in input_json:
            print("2")
            self.prepare_headers()
            self.wfile.write(self.calculator(input_json).encode())
            return
        if 'str' in input_json:
            print("3")
            self.prepare_headers()
            self.wfile.write(json.dumps({
                "lowercase": count_lowercase(input_json['str']),
                "uppercase": count_uppercase(input_json['str']),
                "digits": count_digit(input_json['str']),
                "special": count_special(input_json['str'])
            }).encode())
            return

    # def do_GET(self):
    #
    #     print("Request url: " + self.path)
    #
    #     parsed = urlparse(self.path)
    #     params = parse_qs(parsed.query)
    #
    #     print(params)
    #
    #     if len(params) != 2:
    #         self.send_error_msg()
    #         return
    #     if 'num1' not in params.keys():
    #         self.send_error_msg()
    #         return
    #     if 'num2' not in params.keys():
    #         self.send_error_msg()
    #         return
    #     try:
    #         number_1 = int(params['num1'][0])
    #         number_2 = int(params['num2'][0])
    #     except ValueError:
    #         self.send_error_msg()
    #         return
    #     if number_2 == 0:
    #         self.send_error_msg()
    #         return
    #
    #     self.prepare_headers()
    #     self.wfile.write(json.dumps(
    #         {"sum": number_1 + number_2,
    #          "sub": number_1 - number_2,
    #          "mul": number_1 * number_2,
    #          "div": int(number_1 / number_2),
    #          "mod": number_1 % number_2
    #          }
    #     ).encode())


# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

tcp_server = socketserver.TCPServer(("", PORT), web_server)
tcp_server.serve_forever()
