#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作者：龙.吟


import json
import wordcloud
import requests
from bs4 import BeautifulSoup
from os import path
import multidict as multidict


def get_oid(av_num):  # 获取cid，输入视频bv号
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    }
    url = 'https://api.bilibili.com/x/player/pagelist?bvid={}&jsonp=jsonp'.format(av_num)  # 获取cid的api
    Html = requests.get(url, headers=headers).content.decode('utf8')
    js_format = json.loads(Html)  # 转换为json格式
    return js_format['data'][0]['cid']  # 返回





def get_dm(oid):  # 获取弹幕，输入cid
    url = 'https://api.bilibili.com/x/v1/dm/list.so?oid={}'.format(oid)  # 弹幕api
    dm = requests.get(url).content.decode('utf8')  # 编码，防止中文乱码
    soup = BeautifulSoup(dm, "html.parser")  # 美化下输出格式
    dmlist = [x.text for x in soup.find_all('d')]  # 只返回d标签，即弹幕
    return dmlist


def getFrequencyDictForText(sentence):
    fullTermsDict = multidict.MultiDict()
    tmpDict = {}
    for text in sentence.split(" "):
        val = tmpDict.get(text, 0)
        tmpDict[text.lower()] = val + 1
        for key in tmpDict:
            fullTermsDict.add(key, tmpDict[key])
            return fullTermsDict


def main():
    av_num = input('请输入视频的BV号:')
    cid = get_oid(av_num)
    dm_list = get_dm(cid)
    makecloud(av_num, dm_list)


def makecloud(av_num, dm_list):
    dm = " ".join(str(i) for i in dm_list)
    cloud = wordcloud.WordCloud(

        background_color="white",
        max_words=1000,
        scale=3,
        width=1680,  # 图幅宽度
        height=1050,
        prefer_horizontal=1,
        relative_scaling=0.2,
        # 添加遮罩层

        # mask=mask,

        # 生成中文字的字体,必须要加,不然看不到中文

        font_path=r"C:\Windows\Fonts\FZSTK.TTF"

    ).generate(dm)
    image_produce = cloud.to_image()
    image_produce.show()
    d = path.dirname(__file__)
    cloud.to_file(path.join(d, "{}词云.png".format(av_num)))


if __name__ == '__main__':
    main()
# BV1VT4y137iY
