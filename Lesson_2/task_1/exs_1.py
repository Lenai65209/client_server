"""
1. Задание на закрепление знаний по модулю CSV. Написать скрипт,
осуществляющий выборку определенных данных из файлов info_1.txt, info_2.txt,
info_3.txt и формирующий новый «отчетный» файл в формате CSV.

Для этого:

Создать функцию get_data(), в которой в цикле осуществляется перебор файлов
с данными, их открытие и считывание данных. В этой функции из считанных данных
необходимо с помощью регулярных выражений извлечь значения параметров
«Изготовитель системы», «Название ОС», «Код продукта», «Тип системы».
Значения каждого параметра поместить в соответствующий список. Должно
получиться четыре списка — например, os_prod_list, os_name_list,
os_code_list, os_type_list. В этой же функции создать главный список
для хранения данных отчета — например, main_data — и поместить в него
названия столбцов отчета в виде списка: «Изготовитель системы»,
«Название ОС», «Код продукта», «Тип системы». Значения для этих
столбцов также оформить в виде списка и поместить в файл main_data
(также для каждого файла);

Создать функцию write_to_csv(), в которую передавать ссылку на CSV-файл.
В этой функции реализовать получение данных через вызов функции get_data(),
а также сохранение подготовленных данных в соответствующий CSV-файл;

Пример того, что должно получиться:

Изготовитель системы,Название ОС,Код продукта,Тип системы

1,LENOVO,Windows 7,00971-OEM-1982661-00231,x64-based

2,ACER,Windows 10,00971-OEM-1982661-00231,x64-based

3,DELL,Windows 8.1,00971-OEM-1982661-00231,x86-based

Обязательно проверьте, что у вас получается примерно то же самое.

ПРОШУ ВАС НЕ УДАЛЯТЬ СЛУЖЕБНЫЕ ФАЙЛЫ TXT И ИТОГОВЫЙ ФАЙЛ CSV!!!
"""

import csv
import re


def get_data():
    """Считываеие данных из файлов txt"""
    os_prod_list = []
    os_prod_el = re.compile(r'(Изготовитель ОС: .+?)\n')
    os_name_list = []
    os_name_el = re.compile(r'(Название ОС: .+?)\n')
    os_code_list = []
    os_code_el = re.compile(r'(Код продукта: .+?)\n')
    os_type_list = []
    os_type_el = re.compile(r'(Тип системы: .+?)\n')
    main_data = []
    headers = ['Изготовитель системы', 'Название ОС', 'Код продукта',
               'Тип системы']
    main_data.append(headers)
    for i in range(1, 4):
        with open(f'info_{i}.txt') as f:
            data = f.read()
            os_prod_lst = os_prod_el.findall(data)[0].split()
            del os_prod_lst[0:2]
            os_prod_str = ' '.join(os_prod_lst)
            os_prod_list.append(os_prod_str)
            os_name_lst = os_name_el.findall(data)[0].split()
            del os_name_lst[0:2]
            os_name_str = ' '.join(os_name_lst)
            os_name_list.append(os_name_str)
            os_code_lst = os_code_el.findall(data)[0].split()
            del os_code_lst[0:2]
            os_code_str = ' '.join(os_code_lst)
            os_code_list.append(os_code_str)
            os_type_lst = os_type_el.findall(data)[0].split()
            del os_type_lst[0:2]
            os_type_str = ' '.join(os_type_lst)
            os_type_list.append(os_type_str)

        # print('os_prod_list', os_prod_list)
        # print('os_name_list', os_name_list)
        # print('os_code_list', os_code_list)
        # print('os_type_list', os_type_list)
        row_data = []
        for i in range(0, len(os_prod_list)):
            row_data = [os_prod_list[i], os_name_list[i], os_code_list[i],
                        os_type_list[i]]
        main_data.append(row_data)
    return main_data


def write_to_csv(file_name):
    """Запись данных в ффйл csv"""

    main_data = get_data()
    with open(file_name, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
        for row in main_data:
            writer.writerow(row)


write_to_csv('data_report.csv')
