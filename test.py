#!/usr/bin/env python3
# coding: utf-8
# File: test.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-4-24
from pinyin2chinese import *

transer = PinyinWordTrans()
while(1):
    pinyin_list = input('enter an sent to transfer:')
    result = transer.trans(pinyin_list)
    print(result)
