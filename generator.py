# -*- coding: utf-8 -*-

# 1. split into characters for and sentences
# 2. get the frequency of each character in the corpus
# 3. get the root sound of each character for keywords
# 4. calculate the percentile of each character for keywords
#   1) pass a list of words (one sentence)
#   2) get the frequency of all characters in a word that share the same sound
#   3) rank the characters by frequency in acending order
#   4) calculate the percentile of each character: (rank / total number of characters) * 100
# 5. Sum the percentile of the characters in a word, pick the highest

from pypinyin import lazy_pinyin
from itertools import product
import json
import pandas as pd
import jieba
import numpy as np


def convert2pinyin(df, col_name="source", punctuation=["，", "：", "。", "？", "！", "；", "、", "（", "）", "【", "】", "《", "》", "“", "”"]):
    all_pinyin = []
    for sent in df[col_name].values:
        words = sent.split("¥")
        pinyin_list = []
        for word in words:
            if word:
                tokens = list(jieba.cut(word))
                for token in tokens:
                    if token in punctuation:
                        tokens.remove(token)
                    pinyin_list.append(list(lazy_pinyin(token)))
        all_pinyin.append(pinyin_list)
    df["pinyin"] = all_pinyin
    return df


class HomophoneGenerator:
    def __init__(self, df, col_name="pinyin"):
        self.df = df
        self.col_name = col_name

    def generate(self, char_freq):
        '''char_freq is a dictionary with character as key and frequency as value'''
        all_homo_sent = []
        highest_homo_sent = []
        file_obj_all = open("generated_homo_candidates.out", "w")
        file_obj_high = open("highest_pscore_homo.out", "w")
        for words in self.df[self.col_name].values:
            if words:
                print("Start processing " + str(words))
                all_homo_word = []
                highest_homo_word = []
                for word in words:
                    if len(word) > 1: #no need to find homophones for word with one character
                        # get all homophones of a word by character
                        homophones = []
                        for char in word:
                            root_char = {}
                            for chara in char_freq.keys():
                                if char == lazy_pinyin(chara)[0]:
                                    if char_freq[chara] > 100:
                                        root_char[chara] = char_freq[chara]
                            homophones.append(root_char)
                            print("Root character obtained: " + str(root_char))

                        # get the percentile of each character in a word
                        print("Calculating scores...")
                        word_score = []
                        for homos in homophones:
                            sorted_homos = dict(sorted(homos.items(), key=lambda x: x[1]))
                            n = len(sorted_homos)
                            char_score = {}
                            for i in range(n):
                                char_score[list(sorted_homos.keys())[i]] = (i + 1) / n * 100
                            word_score.append(char_score)
                        
                        # Get all combinations of strings between different dictionaries
                        combinations = list(product(*[d.keys() for d in word_score]))

                        print("Sum scores of each character combination...")
                        # Calculate the sum of integers for each combination
                        homo_word = []
                        for combo in combinations:
                            combo_sum = sum([d[key] for d, key in zip(word_score, combo)])
                            homo_word.append(("".join(combo), combo_sum))
                        all_homo_word.append(homo_word)

                        # pick the word with the highest score
                        print("pick the highest scores")
                        if homo_word:
                            max_idx = np.argmax([word[1] for word in homo_word])
                            highest_homo_word.append(homo_word[max_idx])
                        else:
                            highest_homo_word.append("")

                    else:
                        all_homo_word.append((word, 0))
                        highest_homo_word.append(word)
                
                file_obj_all.write(str(all_homo_word) + "\n")
                file_obj_high.write(str(highest_homo_word) + "\n")
                all_homo_sent.append(all_homo_word)
                highest_homo_sent.append(highest_homo_word)
            
            else:
                file_obj_all.write("\n")
                file_obj_high.write("\n")
                all_homo_sent.append([])
                highest_homo_sent.append("")

        file_obj_all.close()
        file_obj_high.close()
        return all_homo_sent, highest_homo_sent         


if __name__ == "__main__":

    with open('weibo_char_freq.json') as f:
        char_freq = json.load(f)

    df = pd.read_excel("extracted_keywords.xlsx", sheet_name="Sheet1")
    df = convert2pinyin(df)


    homo_generator = HomophoneGenerator(df)
    all_homo, highest_homo = homo_generator.generate(char_freq)

