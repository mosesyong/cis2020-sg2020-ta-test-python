import json
import logging

from flask import request, Response

from codeitsuisse import app

logger = logging.getLogger(__name__)


@app.route('/encryption', methods=['POST'])
def evaluate_secret_message():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = [encoder(test["n"], test["text"]) for test in data]
    logging.info("My result :{}".format(result))
    return Response(json.dumps(result), mimetype='application/json')


def encoder(n, text):
    if n <= 0:
        return "invalid"

    # index   start   end
    # 0       0       7
    # 1       7       13
    # 2       13      19

    text = text.replace(' ', '')
    text = text.upper()
    ch_list = [ch for ch in text if ch.isalpha()]

    # method creates the split strings
    start = 0
    str_list = []
    for i in range(n):
        length = len(ch_list) // n
        remainder = len(ch_list) % n

        if remainder > 0 and i < remainder:
            length += 1

        s = ch_list[start: start + length]
        start += length

        str_list.append(s)

    result = ""
    for i in range(len(ch_list)):
        result += str_list[i % n].pop(0)

    return result


@app.route('/secret-message-encode', methods=['POST'])
def decode_secret_message():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = [decoder(test["n"], test["text"]) for test in data]
    logging.info("My result :{}".format(result))
    return Response(json.dumps(result), mimetype='application/json')


def decoder(n, text):
    text = text.replace(' ', '')
    text = text.upper()
    li = []
    for i in range(n):
        sub_list = []
        for j in range(i, len(text), n):
            sub_list.append(text[j])
        li.append(sub_list)
    return "".join(["".join(l) for l in li])

# Thisisasamplemessage -> 20 characters, split string will have length of 7, 7 and 6
# Thisisa
# samplem
# essage


# TSE
# HAS
# IMS
# SPA
# ILG
# SEE
# AM

#
# {
#     "n": 3,
#     "text": "This is a sample message."
# },
# {
#     "n": 10,
#     "text": "Too short"
# }

# [
#     "TSEHASIMSSPAILGSEEAM",
#     "TOOSHORT"
# ]
