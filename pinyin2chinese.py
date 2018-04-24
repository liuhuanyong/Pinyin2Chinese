#!/usr/bin/env python3
# coding: utf-8
# File: pinyin2chinese.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-4-23
import math
from pinyincut import *

class PinyinWordTrans:
    def __init__(self):
        self.bigram_path = 'data/bigram.model'
        self.pinyin2word_path = 'data/pinyin2word.model'
        self.wordfreq_path = 'data/wordfreq.model'
        self.bigram_dict = self.load_model(self.bigram_path)
        self.pinyin2word_dict = self.load_model(self.pinyin2word_path)
        self.wordfreq_dict = self.load_model(self.wordfreq_path)
        self.pinyincuter = PinyinCut()
        self.min_trans = 1e-10
        self.min_emit = 1e-10

    def load_model(self, model_path):
        f = open(model_path, 'r')
        a = f.read()
        word_dict = eval(a)
        f.close()
        return word_dict

    def trans(self, sent):
        pinyin_list = self.pinyincuter.cut(sent)
        route_dict = {len(pinyin_list):{'E':1.0}}
        for index, pinyin in enumerate(pinyin_list):
            route_dict[index] = {}
            if index == 0:
                for word, p_word in self.pinyin2word_dict[pinyin].items():
                    p0 = p_word * self.bigram_dict['B'].get(word, self.min_emit)
                    if p0 >0 :
                        route_dict[index][word] = p0
            else:
                for word, p_word in self.pinyin2word_dict[pinyin].items():
                    route_dict[index][word] = p_word

        print(route_dict)
        for key,value in route_dict.items():
            print(key,value)

        result = self.viterbi(route_dict)
        return result

    '''verterbi算法求解'''
    def viterbi(self, route_dict):  # 维特比算法（一种动态规划算法）
        V = [{}]
        result = list()
        for state in route_dict[0]:
            V[0][state] = route_dict[0][state]

        for t in range(1, len(route_dict)):
            V.append({})
            for word, word_prob in route_dict[t].items():
                tmp = []
                for pre_state in V[t - 1].keys():
                    last_p = V[t - 1][pre_state]
                    current_p = word_prob
                    if pre_state not in self.bigram_dict:
                        trans_p = 0
                    else:
                        trans_p = self.bigram_dict[pre_state].get(word, self.min_trans)
                    score = last_p * current_p * trans_p
                    tmp.append(score)
                print(tmp)
                max_prob = max(tmp)
                V[t][word] = max_prob

        for vector in V:
            max_state = sorted(vector.items(), key=lambda asd: asd[1], reverse=True)[0][0]
            result.append(max_state)

        return result[:-1]

