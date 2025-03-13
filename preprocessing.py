# -*- coding: utf-8 -*-

import jieba
import pandas as pd
from collections import defaultdict, Counter
import json


def tokenize_zh(df, col_name="source", save_file=False):
    word_freq = defaultdict(int)
    for sent in df[col_name]:
        for word in jieba.cut(sent):
            word_freq[word] += 1
    if save_file:
        json_data = json.dumps(word_freq, indent=4, ensure_ascii=False)
        with open("weibo_word_freq.json", "w", encoding="utf-8") as f:
            f.write(json_data)
    return word_freq


class FrequencyCounter(object):
    def __init__(self, df, col_name="source"):
        self.df = df
        self.col_name = col_name

    def _process_extracted_words(self):
        whole_dict = {}
        for num, item in enumerate(self.df[self.col_name].values):
            if item.strip():
                word_list = []
                for word in item.strip().split("¥"):
                    if word:
                        word_list.append(word)
                whole_dict[num] = word_list
            else:
                whole_dict[num] = ""
        return whole_dict

    def _tokenize_keywords(self):
        toks = []
        keyword_dict = self._process_extracted_words()
        for keyword in [i for v in keyword_dict.values() for i in v]:
            if len(keyword) > 4:
                for tok in jieba.cut(keyword):
                    toks.append(tok)
            else:
                toks.append(keyword)
        return toks
    
    def _split_by_char(self):
        toks = []
        for sent in self.df[self.col_name]:
            for tok in sent:
                if tok != " ":  # remove space
                    toks.append(tok)
        return toks

    def count_freq(self, save_file=False, by_char=False):
        if by_char:
            toks = self._split_by_char()
        else:
            toks = self._tokenize_keywords()

        if save_file:
            json_data = json.dumps(dict(Counter(toks).most_common()), indent=4, ensure_ascii=False)
            with open("weibo_char_freq.json", "w", encoding="utf-8") as f:
                f.write(json_data)
        return Counter(toks).most_common()



if __name__ == "__main__":

    df_train = pd.read_csv("./SMP2020/train.tsv", sep="\t")
    df_dev = pd.read_csv("./SMP2020/dev.tsv", sep="\t")
    df_test = pd.read_csv("./SMP2020/test.tsv", sep="\t")
    df = pd.concat([df_train, df_dev, df_test], axis=0)
    fc = FrequencyCounter(df, col_name="text_a")
    _ = fc.count_freq(save_file=True, by_char=True)
