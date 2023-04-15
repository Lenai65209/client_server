# -*- coding: utf-8 -*-
"""Программа-клиент"""
import argparse
import json
import logging
import socket
import sys
import time
import logs.config_client_log
from errors import ReqFieldMissingError
from my_common.utils import accept_message, send_message
from my_common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, DEFAULT_PORT, ERROR, DEFAULT_IP_ADDRESS

# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')


def create_server_request(account_name='Lena'):
    out = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    CLIENT_LOGGER.debug(
        f'Сформировано "{PRESENCE}" сообщение для пользователя {account_name}')
    return out


def process_ans(message):
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return '200 : OK'
        CLIENT_LOGGER.debug(
            f"НЕ прмшло сообщение '200 : OK', пришло: {message[ERROR]} ")
        return f'400 : {message[ERROR]}'
    CLIENT_LOGGER.debug(
        f"Отсутствует обязательное поле, пришло: {message[ERROR]} ")
    raise ReqFieldMissingError(RESPONSE)


def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    return parser


def main():
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    # Определение адреса и порта
    try:
        if server_port < 1024 or server_port > 65535:
            CLIENT_LOGGER.critical(
                f' Попытка запуска клиента с неподходящим номером порта: {server_port}.'
                f' Допустимы адреса с 1024 до 65535. Клиент завершается.')
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        CLIENT_LOGGER.info(f'Параметры клиента выбраны по умолчнию.')
    except ValueError:
        print(
            'Порт - это число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    CLIENT_LOGGER.info(f'Запущен клиент с парамертами: '
                       f'адрес сервера: {server_address}, порт: {server_port}')
    try:
        #  Включение сокета
        transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        transport.connect((server_address, server_port))

        #  Отправляем сообщение серверу
        message_to_server = create_server_request()
        send_message(transport, message_to_server)

        #  Получаем ответ
        answer = process_ans(accept_message(transport))
        CLIENT_LOGGER.info(f'Принят ответ от сервера {answer}')
        print(answer)
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(
            f'Не удалось подключиться к серверу {server_address} : {server_port}, '
            f'конечный компьютер отверг запрос на подключение.')


if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except Exception as e:
    #     print(e)
