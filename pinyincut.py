#!/usr/bin/env python3
# coding: utf-8
# File: pinyin_cut.py
# Author: lhy<lhy_in_blcu@126.com,https://huangyong.github.io>
# Date: 18-4-24
import pickle

#定义trie字典树节点
class TrieNode:
    def __init__(self):
        self.value = None
        self.children = {}
#遍历树
class SearchIndex:
    def __init__(self, index, char=None, parent=None):
        self.index = index
        self.char = char
        self.parent = parent
        
#定义Trie字典树
class Trie:
    def __init__(self):
        self.root = TrieNode()
        self.trie_path = 'data/pinyin_trie.model'
        self.pinyin_path = 'data/pinyin.txt'
    #添加树节点
    def insert(self, key):
        node = self.root
        for char in key:
            if char not in node.children:
                child = TrieNode()
                node.children[char] = child
                node = child
            else:
                node = node.children[char]
        node.value = key
    #查找节点
    def search(self, key):
        node = self.root
        matches = []
        for char in key:
            if char not in node.children:
                break
            node = node.children[char]
            if node.value:
                matches.append(node.value)
        return matches

    def build_trie(self):
        trie = Trie()
        for line in open(self.pinyin_path):
            word = line.strip().lower()
            trie.insert(word)
        with open(self.trie_path, 'wb') as f:
            pickle.dump(trie, f)


class PinyinCut:
    def __init__(self):
        self.trie_path = 'data/pinyin_trie.model'
        self.trie = self.load_trie(self.trie_path)
        
    def load_trie(self, trie_path):
        with open(trie_path, 'rb') as f:
            return pickle.load(f)
    #音节切分
    def cut(self, sent):
        #获取总长度
        len_sent = len(sent)
        #存储切分序列
        chars = []
        #存储候选序列,SearchIndex(0)表示第一个字符
        candidate_index = [SearchIndex(0)]
        #当前单词的最后一个位置
        last_index = None
        while candidate_index:
            p = candidate_index.pop()
            #如果当前字符所在索引为句子长度，那么最后一个index为本身，即直接到句子末尾。
            if p.index == len_sent:
                last_index = p
                break
            matches = self.trie.search(sent[p.index:])
            for m in matches:
                new_index = SearchIndex(len(m) + p.index, m, p)
                candidate_index.append(new_index)
        index = last_index
        while index:
            if index.parent:
                chars.insert(0, index.char)
            index = index.parent

        return chars
#
# if __name__ == '__main__':
#     trie = Trie()
#     trie.build_trie()
#     cuter = PinyinCut()
#     while(1):
#         user_input = input('enter an string to transfer:')
#         cut_result = cuter.cut(user_input)
#         print(cut_result)