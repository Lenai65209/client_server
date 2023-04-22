# -*- coding: utf-8 -*-
"""Программа-клиент"""
import argparse
import json
import logging
import socket
import sys
import time

from decos import log
# import logs.config_client_log
from errors import ReqFieldMissingError, ServerError
from my_common.utils import accept_message, send_message
from my_common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, \
    RESPONSE, DEFAULT_PORT, ERROR, DEFAULT_IP_ADDRESS, SENDER, MESSAGE, \
    MESSAGE_TEXT

# Инициализация клиентского логера
CLIENT_LOGGER = logging.getLogger('client')


@log
def message_from_server(message):
    """Функция - обработчик сообщений других пользователей, поступающих с
    сервера """
    if ACTION in message and message[ACTION] == MESSAGE and \
            SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение от пользователя '
              f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
        CLIENT_LOGGER.info(f'Получено сообщение от пользователя '
                           f'{message[SENDER]}:\n{message[MESSAGE_TEXT]}')
    else:
        CLIENT_LOGGER.error(
            f'Получено некорректное сообщение с сервера: {message}')


@log
def create_message(sock, account_name='Lena'):
    """Функция запрашивает текст сообщения и возвращает его.
    Так же завершает работу при вводе подобной комманды
    """
    message = input(
        'Введите сообщение для отправки или \'!!!\' для завершения работы: ')
    if message == '!!!':
        sock.close()
        CLIENT_LOGGER.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    CLIENT_LOGGER.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
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


@log
def process_ans(message):
    CLIENT_LOGGER.debug(f'Разбор сообщения от сервера: {message}')
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            CLIENT_LOGGER.debug(
                f"Прмшло сообщение '200 : OK', пришло: {message[RESPONSE]} ")
            return '200 : OK'
        elif message[RESPONSE] == 400:
            CLIENT_LOGGER.debug(
                f"Прмшло сообщение '400 : OK', пришло: {message[ERROR]}")
            raise ServerError(f'400 : {message[ERROR]}')
    raise ReqFieldMissingError(RESPONSE)


@log
def create_arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', '--mode', default='listen', nargs='?')
    return parser


@log
def main():
    parser = create_arg_parser()
    namespace = parser.parse_args(sys.argv[1:])
    server_address = namespace.addr
    server_port = namespace.port
    client_mode = namespace.mode
    # Определение адреса и порта
    try:
        if server_port < 1024 or server_port > 65535:
            CLIENT_LOGGER.critical(
                f' Попытка запуска клиента с неподходящим номером порта: '
                f'{server_port}. Допустимы адреса с 1024 до 65535. Клиент '
                f'завершается.')
            raise ValueError
    except IndexError:
        server_address = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        CLIENT_LOGGER.info(f'Параметры клиента выбраны по умолчнию.')
    except ValueError:
        print(
            'Порт - это число в диапазоне от 1024 до 65535.')
        sys.exit(1)

    # Проверим допустим ли выбранный режим работы клиента
    if client_mode not in ('listen', 'send'):
        CLIENT_LOGGER.critical(
            f'Указан недопустимый режим работы {client_mode}, '
            f'допустимые режимы: listen , send')
        sys.exit(1)

    CLIENT_LOGGER.info(
        f'Запущен клиент с парамертами: адрес сервера: {server_address}, '
        f'порт: {server_port}, режим работы: {client_mode}')
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
        # print(f'Принят ответ от сервера: {answer}')
    except json.JSONDecodeError:
        CLIENT_LOGGER.error('Не удалось декодировать полученную Json строку.')
        sys.exit(1)
    except ServerError as error:
        CLIENT_LOGGER.error(
            f'При установке соединения сервер вернул ошибку: {error.text}')
        sys.exit(1)
    except ReqFieldMissingError as missing_error:
        CLIENT_LOGGER.error(f'В ответе сервера отсутствует необходимое поле '
                            f'{missing_error.missing_field}')
    except ConnectionRefusedError:
        CLIENT_LOGGER.critical(
            f'Не удалось подключиться к серверу {server_address} : '
            f'{server_port}, '
            f'конечный компьютер отверг запрос на подключение.')
        sys.exit(1)
    else:
        # Если соединение с сервером установлено корректно,
        # начинаем обмен с ним, согласно требуемому режиму.
        # основной цикл прогрммы:
        if client_mode == 'send':
            print('Режим работы клиета - отправка сообщений.')
            print(f'Принят ответ от сервера: {answer}')
        else:
            print('Режим работы клиента - приём сообщений.')
            print(f'Принят ответ от сервера: {answer}')
        while True:
            # режим работы - отправка сообщений
            if client_mode == 'send':
                try:
                    send_message(transport, create_message(transport))
                except (
                        ConnectionResetError, ConnectionError,
                        ConnectionAbortedError):
                    CLIENT_LOGGER.error(
                        f'Соединение с сервером '
                        f'{server_address} было потеряно.')
                    sys.exit(1)

            # Режим работы приём:
            if client_mode == 'listen':
                try:
                    message_from_server(accept_message(transport))
                except (
                        ConnectionResetError, ConnectionError,
                        ConnectionAbortedError):
                    CLIENT_LOGGER.error(
                        f'Соединение с сервером '
                        f'{server_address} было потеряно.')
                    sys.exit(1)


if __name__ == '__main__':
    main()
    # try:
    #     main()
    # except Exception as e:
    #     print(e)
