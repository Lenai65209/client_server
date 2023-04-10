"""Unit-тесты клиента"""
import json
import unittest

from client import create_server_request, process_ans
from common.variables import RESPONSE, ERROR, USER, ACCOUNT_NAME, TIME, \
    ACTION, PRESENCE, ENCODING


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


class TestClass(unittest.TestCase):

    def test_def_create_server_request(self):
        test = create_server_request()
        test[
            TIME] = 1.1  # время необходимо приравнять принудительно
        self.assertEqual(test, {ACTION: PRESENCE, TIME: 1.1,
                                USER: {ACCOUNT_NAME: 'Lena'}})

    def test_def_process_ans_200(self):
        self.assertEqual(process_ans({RESPONSE: 200}), '200 : OK')

    def test_def_process_ans_400(self):
        self.assertEqual(process_ans({RESPONSE: 400, ERROR: 'Bad Request'}),
                         '400 : Bad Request')

    def test_no_response(self):
        self.assertRaises(ValueError, process_ans, {ERROR: 'Bad Request'})
        with self.assertRaises(ValueError):
            process_ans({ERROR: 'Bad Request'})


if __name__ == '__main__':
    unittest.main()
