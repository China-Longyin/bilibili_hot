# !/usr/bin/env python

# -*- coding: utf-8 -*-

import requests
import re
from bs4 import BeautifulSoup
import time
import tkinter.messagebox

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
}
url = 'https://www.bilibili.com/ranking'


def save():
    s = get_html()
    flags = tkinter.messagebox.askokcancel('提示', '要执行此操作吗')
    if flags:
        try:
            day = time.strftime("%Y-%m-%d", time.localtime())
            day = str(day)
            with open(day + '哔哩哔哩Top100.txt', 'w', encoding='utf-8') as f:
                f.write(s)
            tkinter.messagebox.showinfo('提示', '保存成功！！')
        except:
            tkinter.messagebox.showinfo('提示', '保存失败！！')


def get_html():
    Html = requests.get(url, headers=headers)
    Html.encoding = 'utf-8'
    soup = BeautifulSoup(Html.text, 'html.parser')
    top_list = soup.findAll('a', {'class': 'title'})
    i = 1
    strs = '以下是今日热榜：\n\n'
    for top in top_list:
        taget = re.findall("\"https.*?\"", str(top))
        strs = strs + str(i) + '.' + top.text + '\n' + taget[0] + '\n' * 2
        i += 1
    return strs


if __name__ == '__main__':
    txt = get_html()
    root = tkinter.Tk()
    te = tkinter.Text(root,font='等线',background='pink')
    bu = tkinter.Button(root, text='保存到本地', command=save)
    sb = tkinter.Scrollbar(root)
    sb.pack(side='right', fill='y')
    te.insert('end', txt)
    bu.pack()
    te.pack()
    sb.config(command=te.yview)
    root.mainloop()
