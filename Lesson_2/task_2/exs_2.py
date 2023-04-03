#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json


def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    with open('orders.json', 'w', encoding='utf-8') as f:
        order_list = data['orders']
        new_order = {'item': item, 'quantity': quantity, ' price': price,
                     'buyer': buyer, 'date': date}
        order_list.append(new_order)
        json.dump(data, f, indent=4, ensure_ascii=False)


write_order_to_json('printer', '1', '16000', 'Ivanov I.I.', '01.04.2024')
write_order_to_json('scanner', '5', '10000', 'Petrov P.P.', '02.04.2024')
write_order_to_json('Принтер', '5', '20000', 'Иванов И.И.', '04.04.2024')
write_order_to_json('Сканер', '1', '8000', 'Петров П.П.', '05.04.2024')
