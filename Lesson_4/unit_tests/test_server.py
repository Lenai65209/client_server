"""Unit-тесты сервера"""
import json
import unittest

from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, \
    ACTION, PRESENCE, ENCODING
from server import parse_client_message


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


class TestServer(unittest.TestCase):
    error_dict = {RESPONSE: 400, ERROR: 'Bad Request'}
    ok_dict = {RESPONSE: 200}

    def test_ok(self):
        self.assertEqual(parse_client_message(
            {ACTION: PRESENCE, TIME: 1.1,
             USER: {ACCOUNT_NAME: 'Lena'}}),
            self.ok_dict)

    def test_no_action(self):
        self.assertEqual(parse_client_message(
            {TIME: 1.1,
             USER: {ACCOUNT_NAME: 'Lena'}}),
            self.error_dict)

    def test_wrong_action(self):
        self.assertEqual(parse_client_message(
            {ACTION: 'close', TIME: 1.1, USER: {ACCOUNT_NAME: 'Lena'}}),
            self.error_dict)

    def test_no_time(self):
        self.assertEqual(parse_client_message(
            {ACTION: PRESENCE, USER: {ACCOUNT_NAME: 'Lena'}}),
            {RESPONSE: 400, ERROR: 'Bad Request'})

    def test_no_user(self):
        self.assertEqual(parse_client_message(
            {ACTION: PRESENCE, TIME: '1.1'}),
            {RESPONSE: 400, ERROR: 'Bad Request'})

    def test_unknown_user(self):
        self.assertEqual(parse_client_message(
            {ACTION: PRESENCE, TIME: 1.1,
             USER: {ACCOUNT_NAME: 'Nik'}}),
            {RESPONSE: 400, ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
