#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 作者：龙.吟


from os import path

import wordcloud

import PIL.Image as image

import numpy as np

d = path.dirname(__file__)


# 分词


def trans_CN(text):
    # 接收分词的字符串

    word_list = jieba.cut(text)

    # 分词后在单独个体之间加上空格

    result = " ".join(word_list)

    return result


with open("G:\Python工程文件\qq文件解密\聊天记录.txt", "rb") as fp:
    text = fp.read()

    # print(text)

    # 将读取的中文文档进行分词

    text = trans_CN(text)

    mask = np.array(image.open("G:\Python工程文件\qq文件解密\dancer.png"))

    wordcloud = wordcloud.WordCloud(

        background_color="white",
        max_words=500,
        scale=3,
        width=1680,  #图幅宽度
        height=1050,
        # 添加遮罩层

        # mask=mask,

        # 生成中文字的字体,必须要加,不然看不到中文

        font_path="C:\Windows\Fonts\FZSTK.TTF"

    ).generate(text)

    image_produce = wordcloud.to_image()

    image_produce.show()

    wordcloud.to_file(path.join(d, "词云.png"))
