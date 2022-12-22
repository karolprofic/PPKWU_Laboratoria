#!/usr/bin/env python3
import json
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


def string_process(string):
    return {
        "lowercase": count_lowercase(string),
        "uppercase": count_uppercase(string),
        "digits": count_digit(string),
        "special": count_special(string),
    }


def send_error_msg():
    pass


def calculator(number_1, number_2):
    try:
        number_1 = int(number_1)
        number_2 = int(number_2)
    except ValueError:
        send_error_msg()
        return
    if number_2 == 0:
        send_error_msg()
        return

    return {
        "sum": number_1 + number_2,
        "sub": number_1 - number_2,
        "mul": number_1 * number_2,
        "div": int(number_1 / number_2),
        "mod": number_1 % number_2
    }


parameter_names_nums = ["sum", "sub", "mul", "div", "mod"]
parameter_names_str = ["lowercase", "uppercase", "digits", "special"]


@app.post('/')
def zad6():
    response_str = {}
    response_nums = {}
    data_xml = request.get_data()
    data = xmltodict.parse(data_xml)

    if 'root' in data:
        data_to_parse = data['root']
        print(data["str"])

        if 'str' in data_to_parse:
            response_str = dict(string_process(data["str"]))

        if 'num1' in data_to_parse and 'num2' in data_to_parse:
            response_nums = dict(calculator(int(data_to_parse['num1']), int(data_to_parse['num2'])))
    if 'str' in data:
        response_str = dict(string_process(data['str']))

    print(response_str)
    print(response_nums)

    return_xml = dicttoxml.dicttoxml({**response_str, **response_nums}, attr_type=False)
    return Response(parseString(return_xml).toprettyxml(), mimetype='application/xml')


# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

app.run(port=4080, host='0.0.0.0')
