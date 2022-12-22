#!/usr/bin/env python3
import http.server
import json
import socketserver
from flask import Flask, request, jsonify, Response
import xmltodict
import dicttoxml
from xml.dom.minidom import parseString

app = Flask(__name__)

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


def send_error_msg(self):
    self.prepare_headers()
    self.wfile.write("Error occurred".encode())

def calculator(self, params):
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

@app.post('/')
def zad6():
    data_xml = request.get_data()
    data = xmltodict.parse(data_xml)

    if 'str' in data:
        data_to_parse = data['root']
        if 'str' in data_to_parse:
            print("str")

        if 'num1' in data_to_parse and 'num2' in data_to_parse:
            print("str i int")

    if 'root' in data:
        print("int")




    # def do_POST(self):
    #     print("POST Request")
    #     self.prepare_headers()
    #     data_len = self.rfile.read(int(self.headers['Content-Length']))
    #     x = self.rfile.read()
    #     # input_json = json.loads(data_len)
    #     # self.wfile.write(json.dumps(input_json).encode())
    #     # tree = ET.parse('movies.xml')
    #     #
    #
    #     print(data_len)
    #     print(x)



        # if 'str' in input_json and 'num1' in input_json and 'num2' in input_json:
        #     print("1")
        #     self.prepare_headers()
        #     calculate = json.loads(self.calculator(input_json))
        #     self.wfile.write(json.dumps({
        #         "lowercase": count_lowercase(input_json['str']),
        #         "uppercase": count_uppercase(input_json['str']),
        #         "digits": count_digit(input_json['str']),
        #         "special": count_special(input_json['str']),
        #         "sum": calculate['sum'],
        #         "sub": calculate['sub'],
        #         "mul": calculate['mul'],
        #         "div": calculate['div'],
        #         "mod": calculate['mod']
        #     }).encode())
        #     return
        # if 'num1' in input_json and 'num2' in input_json:
        #     print("2")
        #     self.prepare_headers()
        #     self.wfile.write(self.calculator(input_json).encode())
        #     return
        # if 'str' in input_json:
        #     print("3")
        #     self.prepare_headers()
        #     self.wfile.write(json.dumps({
        #         "lowercase": count_lowercase(input_json['str']),
        #         "uppercase": count_uppercase(input_json['str']),
        #         "digits": count_digit(input_json['str']),
        #         "special": count_special(input_json['str'])
        #     }).encode())
        #     return


# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

app.run(port=4080, host='0.0.0.0')
