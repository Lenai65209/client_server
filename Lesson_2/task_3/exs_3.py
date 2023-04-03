#!/usr/bin/env python
# -*- coding: utf-8 -*-
import yaml

DATA_DICT = {'first_key': ['computer', 'printer', 'scanner'],
             'second_key': 7,
             'third_key': {'computer': '500€', 'printer': '250€',
                           'scanner': '100€'}
             }

with open('file.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(DATA_DICT, f, default_flow_style=False, allow_unicode=True,
              sort_keys=False
              )

with open("file.yaml", 'r', encoding='utf-8') as f:
    DATA_DICT_FROM_FILE = yaml.load(f, Loader=yaml.SafeLoader)
    print(DATA_DICT == DATA_DICT_FROM_FILE)
    print(DATA_DICT_FROM_FILE)
