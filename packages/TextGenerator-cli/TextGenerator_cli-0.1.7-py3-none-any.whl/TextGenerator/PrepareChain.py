# -*- coding: utf-8 -*-

'''
与えられた文書からマルコフ連鎖のためのチェーン（連鎖）を作成して、DBに保存するファイル
'''

import os
import re
import sqlite3
import subprocess
from collections import defaultdict
from shutil import which

import MeCab


class PrepareChain(object):
    '''
    チェーンを作成してDBに保存するクラス
    '''

    BEGIN = '__BEGIN_SENTENCE__'
    END = '__END_SENTENCE__'

    def __init__(self, text, DB_PATH='chain.db'):
        '''
        初期化メソッド
        @param text チェーンを生成するための文章
        '''
        self.text = text
        self.DB_PATH = DB_PATH

        # 形態素解析用タガー
        asdf = MeCab.Tagger('-Ochasen -r' + self.search_mecabrc())
        asdf.parse('')
        self.tagger = asdf

    def search_mecabrc(self):
        '''
        mecabrcの探索
        @return mecabrcのパス
        '''
        if which('mecab-config'):
            cmd = ['mecab-config', '--sysconfdir']
            exe = subprocess.check_output(cmd, shell=False)
            return os.path.join(exe.decode().rstrip(), 'mecabrc')
        else:
            return self._search_mecabrc()

    def _search_mecabrc(self):
        '''
        mecabrcの探索ヘルパ
        @return mecabrcのパス
        '''
        if os.name == 'nt':
            mecabrc = ('C:\\Program Files(x86)\\Mecab\\etc\\mecabrc',)
        else:
            mecabrc = ('/usr/local/etc/mecabrc', '/etc/mecabrc')

        mecabrc = list(filter(os.path.isfile, mecabrc))
        if len(mecabrc) == 1:
            return mecabrc[0]
        else:
            return ('NUL' if os.name == 'nt' else '/dev/null')

    def make_triplet_freqs(self):
        '''
        形態素解析から3つ組の出現回数まで
        @return 3つ組とその出現回数の辞書 key: 3つ組（タプル） val: 出現回数
        '''
        # 長い文章をセンテンス毎に分割
        sentences = self._divide(self.text)

        # 3つ組の出現回数
        triplet_freqs = defaultdict(int)

        # センテンス毎に3つ組にする
        for sentence in sentences:
            # 形態素解析
            morphemes = self._morphological_analysis(sentence)
            # 3つ組をつくる
            triplets = self._make_triplet(morphemes)
            # 出現回数を加算
            for (triplet, n) in list(triplets.items()):
                triplet_freqs[triplet] += n

        return triplet_freqs

    def _divide(self, text):
        '''
        「。」や改行などで区切られた長い文章を一文ずつに分ける
        @param text 分割前の文章
        @return 一文ずつの配列
        '''

        # 全ての分割文字を改行文字に置換（splitしたときに「。」などの情報を無くさないため）
        text = re.sub(r'(。|\.|．)', r'\1\n', text)

        # 改行文字で分割
        sentences = text.splitlines()

        # 前後の空白文字を削除
        sentences = [sentence.strip() for sentence in sentences]

        return sentences

    def _morphological_analysis(self, sentence):
        '''
        一文を形態素解析する
        @param sentence 一文
        @return 形態素で分割された配列
        '''
        morphemes = []
        node = self.tagger.parseToNode(sentence)
        while node:
            if node.posid != 0:
                morpheme = node.surface
                morphemes.append(morpheme)
            node = node.next
        return morphemes

    def _make_triplet(self, morphemes):
        '''
        形態素解析で分割された配列を、形態素毎に3つ組にしてその出現回数を数える
        @param morphemes 形態素配列
        @return 3つ組とその出現回数の辞書 key: 3つ組（タプル） val: 出現回数
        '''
        # 3つ組をつくれない場合は終える
        if len(morphemes) < 3:
            return {}

        # 出現回数の辞書
        triplet_freqs = defaultdict(int)

        # 繰り返し
        for i in range(len(morphemes)-2):
            triplet = tuple(morphemes[i:i+3])
            triplet_freqs[triplet] += 1

        # beginを追加
        triplet = (self.BEGIN, morphemes[0], morphemes[1])
        triplet_freqs[triplet] = 1

        # endを追加
        triplet = (morphemes[-2], morphemes[-1], self.END)
        triplet_freqs[triplet] = 1

        return triplet_freqs

    def save(self, triplet_freqs, init=False):
        '''
        3つ組毎に出現回数をDBに保存
        @param triplet_freqs 3つ組とその出現回数の辞書 key: 3つ組（タプル） val: 出現回数
        '''
        # DBオープン
        con = sqlite3.connect(self.DB_PATH)

        # 初期化から始める場合
        if init:
            # DBの初期化
            schema = 'drop table if exists chain_freqs;'\
                     'create table chain_freqs ('\
                     'id integer primary key autoincrement not null,'\
                     'prefix1 text not null,'\
                     'prefix2 text not null,'\
                     'suffix text not null,'\
                     'freq integer not null);'
            con.executescript(schema)

            # データ整形
            datas = [(triplet[0], triplet[1], triplet[2], freq)
                     for (triplet, freq) in list(triplet_freqs.items())]

            # データ挿入
            p_statement = 'insert into chain_freqs'\
                ' (prefix1, prefix2, suffix, freq) values (?, ?, ?, ?)'
            con.executemany(p_statement, datas)

        # コミットしてクローズ
        con.commit()
        con.close()

    def show(self, triplet_freqs):
        '''
        3つ組毎の出現回数を出力する
        @param triplet_freqs 3つ組とその出現回数の辞書 key: 3つ組（タプル） val: 出現回数
        '''
        for triplet in triplet_freqs:
            print('|'.join(triplet), '\t', triplet_freqs[triplet])


def main(file=0):
    text = open(file, encoding='utf-8_sig').read()
    chain = PrepareChain(text)
    triplet_freqs = chain.make_triplet_freqs()
    chain.save(triplet_freqs, True)


if __name__ == '__main__':
    main()
