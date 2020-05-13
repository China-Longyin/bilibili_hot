#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作者：龙.吟


import sys
import requests
import re
import time
import tkinter
from bs4 import BeautifulSoup
import webbrowser
import tkinter.messagebox
from tkinter import filedialog


def save():
    top_list = get_html()
    day = time.strftime("%Y.%m.%d", time.localtime())
    day = str(day)
    i = 1
    strs = '{}哔哩哔哩Top100：\n\n'.format(day)
    for top in top_list:
        taget = re.findall("\"https.*?\"", str(top))
        strs = strs + str(i) + '.' + top.text + '\n' + taget[0] + '\n' * 2
        i += 1
    s = strs
    flags = tkinter.messagebox.askokcancel('提示', '要执行此操作吗')
    if flags:
        try:

            with open(day + '哔哩哔哩Top100.txt', 'w', encoding='utf-8') as f:
                f.write(str(s))
            tkinter.messagebox.showinfo('提示', '保存成功！！')
        except:
            tkinter.messagebox.showinfo('提示', '保存失败！！')


def get_html():
    """获取所有标题、网址"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    }
    url = 'https://www.bilibili.com/ranking'
    Html = requests.get(url, headers=headers)
    Html.encoding = 'utf-8'
    soup = BeautifulSoup(Html.text, 'html.parser')
    top_list = soup.findAll('a', {'class': 'title'})
    return top_list


def save_data(top_list=None):
    """保存数据，返回一个元组的列表"""
    if top_list is None:
        top_list = get_html()
    data = []
    for top in top_list:
        taget = re.findall("(?<=\")https:.*?(?=\")", str(top))
        data.append((top.text, taget))
    return '今日哔哩哔哩Top100', data


def open_url(url1='https://www.bilibili.com/'):
    webbrowser.open(url1)


def ipt_data(file_name):
    with open(file_name, 'r', encoding='utf-8') as f:
        a_str = f.readlines()
    data = []
    for i in range(1, 301, 3):
        name = a_str[i + 1].strip('\n')
        net = [a_str[i + 2].strip('\n')]
        data.append((name, net))
    return a_str[0], data


def select_path():
    root = tkinter.Tk()

    root.withdraw()

    file_path = filedialog.askopenfilename()

    return file_path


def windows(data_txt=None):
    if data_txt is None:
        data_txt = save_data()
    name, txt = data_txt
    root = tkinter.Tk()
    root.title(name)
    # 设置窗口的居中显示
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    width = 700
    height = 630
    size = "%dx%d+%d+%d" % (width, height, (screenwidth - width) / 2, (screenheight - height) / 2)
    root.geometry(size)
    bu1 = tkinter.Button(root, text='保存到本地', command=save)
    bu2 = tkinter.Button(root, text='打开首页', command=open_url)
    bu3 = tkinter.Button(root, text='导入数据', command=lambda: windows(ipt_data(select_path())))

    bu1.grid(row=1, sticky="w", padx=200)
    bu2.grid(row=1, )
    bu3.grid(row=1, sticky="e", padx=200)
    i = 0
    for item in txt:
        i += 1
        names = locals()
        names['bu' + str(i)] = tkinter.Button(root, text='Top' + str(i) + '*-' * 3 + item[0], width=100, anchor='nw',
                                              command=lambda x=str(item[1][0]): open_url(x))
        names.get('bu' + str(i)).grid()
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    root.mainloop()


if __name__ == '__main__':
    windows()
