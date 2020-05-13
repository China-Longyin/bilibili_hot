#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作者：龙.吟
import re



def ipt_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        a_str = f.readlines()
    data = []
    for i in range(1, 301, 3):
        name = a_str[i+1].strip('\n')
        net = [a_str[i + 2].strip('\n')]
        data.append((name, net))
    return data


print(ipt_data('2020-04-16哔哩哔哩Top100.txt'))