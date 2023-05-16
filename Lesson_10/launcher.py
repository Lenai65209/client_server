# -*- coding: utf-8 -*-
"""Программа-лаунчер"""

import subprocess

PROCESSES = []

try:
    applications_number = int(input('Укажите максимальное число запускаемых '
                                    'клиентских приложений: '))
except Exception as e:
    print(e)

while True:
    ACTION = input('Выберите действие: q - выход, '
                   's - запустить сервер и клиенты, '
                   'x - закрыть все окна: ')

    if ACTION == 'q':
        break
    elif ACTION == 's':
        PROCESSES.append(subprocess.Popen('python server.py',
                                          creationflags=subprocess.CREATE_NEW_CONSOLE))
        for i in range(applications_number):
            PROCESSES.append(
                subprocess.Popen(f'python client.py -n test{i + 1}',
                                 creationflags=subprocess.CREATE_NEW_CONSOLE))

    elif ACTION == 'x':
        while PROCESSES:
            VICTIM = PROCESSES.pop()
            VICTIM.kill()
