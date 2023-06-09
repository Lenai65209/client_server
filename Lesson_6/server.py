# -*- coding: utf-8 -*-
"""Программа-сервер"""
import socket
import sys
import argparse
import json
import logging
import logs.config_server_log
from errors import IncorrectDataRecivedError
from my_common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, DEFAULT_PORT, MAX_CONNECTIONS, ERROR, MAX_PACKAGE_LENGTH, ENCODING
from my_common.utils import accept_message, send_message
from decos import log


#Инициализация логирования сервера.
SERVER_LOGGER = logging.getLogger('server')


@log
def parse_client_message(message):
    SERVER_LOGGER.debug(f'Разбор сообщения от клиента : {message}')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message and message[USER][ACCOUNT_NAME] == 'Lena':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


@log
def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    return parser


@log
def main():
    # Определение порта
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    listen_address = namespace.a
    listen_port = namespace.p
    if not 1023 < listen_port < 65536:
        SERVER_LOGGER.critical(f'Попытка запуска сервера с указанием неподходящего порта '
                               f'{listen_port}. Допустимы адреса с 1024 до 65535.')
        sys.exit(1)
    SERVER_LOGGER.info(f'Запущен сервер, порт для подключений: {listen_port}, '
                       f'адрес с которого принимаются подключения: {listen_address}. '
                       f'Если адрес не указан, принимаются соединения с любых адресов.')

    # Включение сокета
    transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    transport.bind((listen_address, listen_port))

    # Слушаем порт
    transport.listen(MAX_CONNECTIONS)

    while True:
        client, client_address = transport.accept()
        SERVER_LOGGER.info(f'Установлено соедение с ПК {client_address}')
        try:
            message_from_client = accept_message(client)
            SERVER_LOGGER.debug(f'Получено сообщение {message_from_client}')
            print(message_from_client)
            response = parse_client_message(message_from_client)
            SERVER_LOGGER.info(f'Cформирован ответ клиенту {response}')
            send_message(client, response)
            SERVER_LOGGER.debug(
                f'Соединение с клиентом {client_address} закрывается.')
            client.close()
            break  # выключаемся после ответа клиенту
        except json.JSONDecodeError:
            SERVER_LOGGER.error(
                f'Не удалось декодировать JSON строку, полученную от '
                f'клиента {client_address}. Соединение закрывается.')
            client.close()
        except IncorrectDataRecivedError:
            SERVER_LOGGER.error(
                f'От клиента {client_address} приняты некорректные данные. '
                f'Соединение закрывается.')
            client.close()


if __name__ == '__main__':
    main()

    # try:
    #     main()
    # except Exception as e:
    #     print(e)
