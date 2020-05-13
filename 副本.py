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
import pandas


def save():
    data_list = save_data()
    day = time.strftime("%Y.%m.%d", time.localtime())
    day = str(day)
    name = ['排名', '标题', '网址', '播放数', '硬币数', '作者']
    pack = pandas.DataFrame(columns=name, data=data_list)
    flags = tkinter.messagebox.askokcancel('提示', '要执行此操作吗')
    if flags:
        try:
            pack.to_csv(day + '哔哩哔哩Top100.csv', encoding='utf_8_sig',index=False)
            tkinter.messagebox.showinfo('提示', '保存成功！！')
        except Exception as e:
            tkinter.messagebox.showinfo('提示', '保存失败！！\n' + str(e))


def get_html():
    """获取所有标题、网址"""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18362'
    }
    url = 'https://www.bilibili.com/ranking'
    Html = requests.get(url, headers=headers)
    Html.encoding = 'utf-8'
    soup = BeautifulSoup(Html.text, 'html.parser')
    top_list = soup.findAll('li', {'class': 'rank-item'})
    return top_list


def save_data(top_list=None):
    """保存数据，返回一个列表【排名，标题，网址，播放数，硬币数，作者】"""
    if top_list is None:
        top_list = get_html()
    data = []
    for top in top_list:
        img = top.find('div', {'class': 'img'})
        num = top.find('div', {'class': 'num'})
        box = top.findAll('span', {'class': 'data-box'})
        title = re.findall('''(?<=alt=").*?(?=")|(?<=alt=').*?(?=')''', str(img))
        ur = re.findall("(?<=\")https:.*?(?=\")", str(img))
        data.append([num.text, title[0], ur[0], box[0].text, box[1].text, box[2].text])

    return data


def open_url(url1='https://www.bilibili.com/'):
    webbrowser.open(url1)


def ipt_data(file_name):
    file = pandas.read_csv(file_name)
    data = file.values.tolist()

    return data


def select_path():
    root = tkinter.Tk()

    root.withdraw()

    file_path = filedialog.askopenfilename()

    return file_path


def next_page():
    pass


def previous_page():
    pass


def windows(data_txt=None):
    if data_txt is None:
        data_txt = save_data()
    txt = data_txt
    root = tkinter.Tk()
    root.title('今日哔哩哔哩排行榜前20')
    # 设置窗口的居中显示
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    width = 710
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
        names['bu' + str(i)] = tkinter.Button(root, text='Top' + str(i) + '*-' * 3 + item[1], width=100, anchor='nw',
                                              command=lambda x=str(item[2]): open_url(x))
        names.get('bu' + str(i)).grid()
    root.protocol("WM_DELETE_WINDOW", lambda: sys.exit(0))
    root.mainloop()


if __name__ == '__main__':
    windows()
