# -*- coding: utf-8 -*-
"""Программа-клиент"""

import json
import socket
import sys
import time


def accept_message(client):
    encoded_response = client.recv(1024)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode('utf-8')
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def create_server_request(account_name='Lena'):
    out = {
        'action': 'presence',
        'time': time.time(),
        'user': {
            'account_name': account_name
        }
    }
    return out


def send_message(sock, message):
    json_message = json.dumps(message)
    encoded_message = json_message.encode('utf-8')
    sock.send(encoded_message)


def process_ans(message):
    if 'response' in message:
        if message['response'] == 200:
            return '200 : OK'
        return f'400 : {message["error"]}'
    raise ValueError


def main():
    # Определение адреса и порта
    try:
        server_address = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 or server_port > 65535:
            raise ValueError
    except IndexError:
        server_address = '127.0.0.1'
        server_port = 7777
    except ValueError:
        print(
            'Порт - это число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    #  Включение сокета
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.connect((server_address, server_port))

    #  Отправляем сообщение серверу
    message_to_server = create_server_request()
    send_message(transport, message_to_server)

    #  Получаем ответ
    try:
        answer = process_ans(accept_message(transport))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера.')


if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except Exception as e:
    #     print(e)
