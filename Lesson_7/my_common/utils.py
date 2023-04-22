# -*- coding: utf-8 -*-
"""Утилиты"""

import json
import logging
import os
import sys

sys.path.append('../')
from .variables import MAX_PACKAGE_LENGTH, ENCODING
from errors import NonDictInputError, NonBytesInputError
from decos import log

sys.path.append(os.path.join(os.getcwd(), '..'))

CLIENT_LOGGER = logging.getLogger('client')
SERVER_LOGGER = logging.getLogger('server')


@log
def accept_message(client):
    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        SERVER_LOGGER.critical(f'Сообщение {response} не является словарем!')
        CLIENT_LOGGER.critical(f'Сообщение {response} не является словарем!')
        raise NonDictInputError
    SERVER_LOGGER.critical(f'Сообщение {encoded_response} не байты!')
    CLIENT_LOGGER.critical(f'Сообщение {encoded_response} не байты!')
    raise NonBytesInputError


@log
def send_message(sock, message):
    SERVER_LOGGER.info('Отправка сообщения')
    CLIENT_LOGGER.info('Отправка сообщения')
    js_message = json.dumps(message)
    encoded_message = js_message.encode(ENCODING)
    sock.send(encoded_message)
