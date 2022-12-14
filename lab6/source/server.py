#!/usr/bin/env python3
from flask import Flask, request, Response
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


@app.post('/')
def zad6():
    str_stats = {}
    num_stats = {}
    data_xml = request.get_data()
    data = xmltodict.parse(data_xml)

    if 'root' in data:
        data_to_parse = data['root']
        if 'num1' in data_to_parse and 'num2' in data_to_parse:
            num_stats = dict(calculator(int(data_to_parse['num1']), int(data_to_parse['num2'])))

        if 'str' in data_to_parse:
            str_stats = dict(string_process(data_to_parse['str']))

    elif 'str' in data:
        str_stats = dict(string_process(data['str']))

    return_xml = dicttoxml.dicttoxml({**str_stats, **num_stats}, attr_type=False)
    return Response(parseString(return_xml).toprettyxml(), mimetype='application/xml')


# --- main ---

PORT = 4080

print(f'Starting: http://localhost:{PORT}')

app.run(port=4080, host='0.0.0.0')
