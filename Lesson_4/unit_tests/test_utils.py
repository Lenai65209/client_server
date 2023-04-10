"""Unit-тесты утилит"""

import json
import unittest

from common.utils import accept_message, send_message
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, ACTION, \
    PRESENCE, ENCODING


class TestSocket:
    '''
    Тестовый класс для имитации работы функций
    '''

    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_message = None
        self.receved_message = None

    def send(self, message_to_send):
        json_test_message = json.dumps(self.test_dict)
        self.encoded_message = json_test_message.encode(ENCODING)
        self.receved_message = message_to_send

    def recv(self, max_len):
        json_test_message = json.dumps(self.test_dict)
        return json_test_message.encode(ENCODING)


class Tests(unittest.TestCase):
    error_dict = {RESPONSE: 400, ERROR: 'Bad Request'}
    ok_dict = {RESPONSE: 200}
    send_client_dict = {
        ACTION: PRESENCE,
        TIME: 111111.111111,
        USER: {
            ACCOUNT_NAME: 'test_test'
        }
    }

    def test_send_client_message(self):
        test_socket = TestSocket(self.send_client_dict)
        send_message(test_socket, self.send_client_dict)
        self.assertEqual(test_socket.encoded_message,
                         test_socket.receved_message)
        with self.assertRaises(Exception):
            send_message(test_socket)

    def test_send_server_ok_message(self):
        test_socket = TestSocket(self.ok_dict)
        send_message(test_socket, self.ok_dict)
        self.assertEqual(test_socket.encoded_message,
                         test_socket.receved_message)
        with self.assertRaises(Exception):
            send_message(test_socket)

    def test_send_server_err_message(self):
        test_socket = TestSocket(self.error_dict)
        send_message(test_socket, self.error_dict)
        self.assertEqual(test_socket.encoded_message,
                         test_socket.receved_message)
        with self.assertRaises(Exception):
            send_message(test_socket)

    def test_get_server_ok_message(self):
        test_sock_ok = TestSocket(self.ok_dict)
        self.assertEqual(accept_message(test_sock_ok), self.ok_dict)

    def test_get_server_err_message(self):
        test_sock_err = TestSocket(self.error_dict)
        self.assertEqual(accept_message(test_sock_err), self.error_dict)

    def test_get_client_message(self):
        test_sock_ok = TestSocket(self.send_client_dict)
        self.assertEqual(accept_message(test_sock_ok),
                         self.send_client_dict)


if __name__ == '__main__':
    unittest.main()
