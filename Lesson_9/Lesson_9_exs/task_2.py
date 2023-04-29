"""
2. Написать функцию host_range_ping() для перебора ip-адресов из заданного диапазона.
Меняться должен только последний октет каждого адреса.
По результатам проверки должно выводиться соответствующее сообщение.
"""

from ipaddress import ip_address

from task_1 import host_ping


def host_range_ping():
    while True:
        # запрос первоначального адреса
        start_ip = input('Введите первоначальный адрес: ')
        try:
            # смотрим чему равен последний октет
            last_octet = int(start_ip.split('.')[3])
            break
        except Exception as e:
            print(e)
    while True:
        # запрос на количество проверяемых адресов
        addresses_number = input('Сколько адресов проверить?: ')
        if not addresses_number.isnumeric():
            print('Необходимо ввести число: ')
        else:
            # по условию меняется только последний октет
            if (last_octet + int(addresses_number)) > 254:
                print(f"Можем менять только последний октет. "
                      f"Максимальное число хостов для проверки: "
                      f"{254 - last_octet}")
            else:
                break

    host_list = []
    # формируем список ip адресов
    [host_list.append(str(ip_address(start_ip) + i)) \
        for i in range(int(addresses_number))]
    # передаем список в функцию из задания 1 для проверки доступности
    return host_ping(host_list)


if __name__ == "__main__":
    host_range_ping()

"""
Результат:

Введите первоначальный адрес: 192.168.99.1
Сколько адресов проверить?: 5
ping  192.168.99.1 - Узел доступен
ping  192.168.99.2 - Узел доступен
ping  192.168.99.3 - Узел недоступен
ping  192.168.99.4 - Узел недоступен
ping  192.168.99.5 - Узел недоступен

"""
