"""Утилиты"""

import json
import os
import sys

from .variables import MAX_PACKAGE_LENGTH, ENCODING

sys.path.append(os.path.join(os.getcwd(), '..'))
def accept_message(client):
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(sock, message):
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
