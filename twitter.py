# -*- coding: utf-8 -*-

import urllib
from requests_oauthlib import OAuth1Session
import json
import twitter_config as config
import csv


def get_json(twitter, url):
     # 結果を取得
    res = twitter.get(url)
    # JSON に変換
    data = json.loads(res.text)

    return data


def process_tweet(tweet, writer):
    # ツイートの内容を表示
    print(tweet['text'])
    print('-' * 20)
    # CSV に書き出し
    writer.writerow([
        '@' + tweet['user']['screen_name'],     # ユーザー名
        tweet['text'],                          # 内容
        tweet['created_at']                     # ツイート日時
    ])


if __name__ == '__main__':
    SEARCH_API_URL = 'https://api.twitter.com/1.1/search/tweets.json'

    # 検索する単語を入力する
    print('検索する単語>', end='')
    word = input()

    # OAuth
    twitter = OAuth1Session(
        config.CONSUMER_KEY,
        client_secret=config.CONSUMER_SECRET,
        resource_owner_key=config.ACCESS_TOKEN,
        resource_owner_secret=config.ACCESS_TOKEN_SECRET
    )

    # CSV ファイルを開く
    with open('tweets_' + word + '.csv', 'w') as f:
        # 改行コードを指定
        writer = csv.writer(f, lineterminator='\n')

        count = 0   # 処理したツイート数
        # クエリパラメータを作成
        query = {
            'q': word + " exclude:retweets",
            'count': 100
        }
        # URL を作成
        url = SEARCH_API_URL + '?' + urllib.parse.urlencode(query)
        # 結果を取得
        data = get_json(twitter, url)
        # ツイートを処理
        for t in data['statuses']:
            process_tweet(t, writer)
            count += 1
        print('=' * 30 + ('\n読み込んだツイート数: %d\n' % count) + '=' * 30)
        # next_results に次の検索クエリが存在する限り、ツイートを取得する
        while 'next_results' in data['search_metadata'] and len(data['search_metadata']['next_results']) > 0 and count <= 1200:
            # URL を作成
            url = SEARCH_API_URL + data['search_metadata']['next_results']
            # 結果を取得
            data = get_json(twitter, url)
            # ツイートを処理
            for t in data['statuses']:
                process_tweet(t, writer)
                count += 1
            print('=' * 30 + ('\n読み込んだツイート数: %d\n' % count) + '=' * 30)