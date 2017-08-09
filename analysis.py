# -*- coding: utf-8 -*-

from natto import MeCab
import csv
from collections import OrderedDict


def process(option, input_filename, output_filename):
    # 入力ファイルを開く
    with open(input_filename, 'r') as input_file:
        reader = csv.reader(input_file)
        # MeCab オブジェクトを作成
        with MeCab(option) as nm:
            # ツイートを処理する
            words_count = {}    # 名詞ごとの出現回数を保持する辞書
            for row in reader:
                # 本文を形態素解析する
                for n in nm.parse(row[1], as_nodes=True):
                    node = n.feature.split(',')
                    if len(node) != 3:
                        continue
                    if node[1] == '名詞':     # 名詞だったとき
                        # 出現回数を加算
                        if node[0] in words_count:
                            words_count[node[0]] += 1
                        else:
                            words_count[node[0]] = 1
            # 出現回数順にソートする
            words_count = OrderedDict(sorted(words_count.items(), key=lambda x:x[1], reverse=True))
            # 結果を CSV ファイルに出力
            with open(output_filename, 'w') as output_file:
                writer = csv.writer(output_file, lineterminator='\n') # 改行コードを指定
                for w in words_count.items():
                    writer.writerow(list(w))
            # 出力
            return words_count


if __name__ == '__main__':
    # CSVファイル名を入力
    print('CSVファイル名>', end='')
    filename = input()

    # MeCab 標準の辞書を用いて処理
    process('-F%m,%f[0],%h', filename, 'out_ipadic_' + filename)
    # mecab-ipadic-NEologd を用いて処理
    word_count = process('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd -F%m,%f[0],%h', filename, 'out_neologd_' + filename)