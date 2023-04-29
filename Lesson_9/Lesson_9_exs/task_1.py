"""
1. Написать функцию host_ping(), в которой с помощью утилиты ping
будет проверяться доступность сетевых узлов.
Аргументом функции является список, в котором каждый сетевой узел
должен быть представлен именем хоста или ip-адресом.
В функции необходимо перебирать ip-адреса и проверять
их доступность с выводом соответствующего сообщения
(«Узел доступен», «Узел недоступен»). При этом ip-адрес
сетевого узла должен создаваться с помощью функции ip_address().
"""

# воспользуемся пинг-командой со следуюшими параметрами:

'''
-w интервал

Определяет в миллисекундах время ожидания получения сообщения с эхо-ответом, 
которое соответствует сообщению с эхо-запросом. Если сообщение с эхо-ответом 
не получено в пределах заданного интервала, то выдается сообщение об ошибке 
"Request timed out". Интервал по умолчанию равен 4000 (4 секунды).

-n счетчик
Задает число отправляемых сообщений с эхо-запросом. По умолчанию - 4.
'''

from ipaddress import ip_address
from subprocess import Popen, PIPE


def host_ping(addresses_list, timeout=500, requests=4):
    results = {'Доступные узлы': "",
               'Недоступные узлы': ""}  # словарь с результатами
    for address in addresses_list:
        try:
            address = ip_address(address)
        # ValueError: 'yandex.ru' does not appear to be an IPv4 or IPv6 address
        except ValueError:
            pass
        proc = Popen(f"ping {address} -w {timeout} -n {requests}", shell=False,
                     stdout=PIPE)
        proc.wait()
        # проверяем код завершения подпроцесса
        if proc.returncode == 0:
            results['Доступные узлы'] += f' {str(address)}\n'
            res_string = f'{address} - Узел доступен'
        else:
            results['Недоступные узлы'] += f' {str(address)}\n'
            res_string = f'{address} - Узел недоступен'
        print('ping ', res_string)
    return results


if __name__ == '__main__':
    ip_addresses = ['yandex.ru', 'fe80::7d3d:b7fa:887a:e547%16',
                    '192.168.0.100', '127.0.0.1', 'google.com', '192.168.43.1']
    my_dic = host_ping(ip_addresses)
    for key, value in my_dic.items():
        print(key, ':\n', value)

"""
    Результат:
    ping  yandex.ru - Узел доступен
    ping  fe80::7d3d:b7fa:887a:e547%16 - Узел доступен
    ping  192.168.0.100 - Узел недоступен
    ping  127.0.0.1 - Узел доступен
    ping  google.com - Узел доступен
    ping  192.168.43.1 - Узел доступен
    Доступные узлы :
      yandex.ru
      fe80::7d3d:b7fa:887a:e547%16
     127.0.0.1
     google.com
     192.168.43.1
    
    Недоступные узлы :
      192.168.0.100
"""
