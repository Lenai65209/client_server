# -*- coding: utf-8 -*-
"""Программа-сервер"""
import json
import socket
import sys


def accept_message(client):
    encoded_response = client.recv(1024)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode('utf-8')
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def parse_client_message(message):
    if 'action' in message and message[
        'action'] == 'presence' and 'time' in message \
            and 'user' in message and message['user']['account_name'] == 'Lena':
        return {'response': 200}
    return {
        'response': 400,
        'error': 'Bad Request'
    }


def send_message(sock, message):
    json_message = json.dumps(message)
    encoded_message = json_message.encode('utf-8')
    sock.send(encoded_message)


def main():
    # Определение порта
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = 7777
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' указывается номер порта.')
        sys.exit(1)
    except ValueError:
        print(
            'Порт - это число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Определение адреса
    try:
        if '-a' in sys.argv:
            listen_address = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_address = '127.0.0.1'
    except IndexError:
        print(
            'После параметра \'a\'- адрес, который будет слушать сервер.')
        sys.exit(1)

    # Включение сокета
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт
    transport.listen(5)

    while True:
        client, client_address = transport.accept()
        try:
            message_from_client = accept_message(client)
            print(message_from_client)
            response = parse_client_message(message_from_client)
            send_message(client, response)
            client.close()
            break  # выключаемся после ответа клиенту
        except (ValueError, json.JSONDecodeError):
            print('Некорретное сообщение от клиента.')
            client.close()
            break  # выключаемся


if __name__ == '__main__':
    main()

    # try:
    #     main()
    # except Exception as e:
    #     print(e)
