import urllib.parse
from datetime import datetime, timedelta
import requests  # Discordへの送信に使用
import os
import time
from discord_util import DiscordUtil
from arxiv import fetch_feed

discord_util = DiscordUtil()  

def run():
    # 現在のUTC時刻を取得
    now = datetime.utcnow()

    # 5時間前のUTC時刻を取得
    time_threshold = now - timedelta(hours=5)

    # 検索クエリを定義
    # Computer Scienceのカテゴリを指定
    query = 'cat:cs.SD'

    # ベースとなるAPIのURL
    base_url = 'http://export.arxiv.org/api/query?'

    # APIパラメータの設定
    params = {
        'search_query': query,
        'start': 0,                   # 取得開始位置
        'max_results': 100,           # 取得する結果の最大数（必要に応じて増やしてください）
        'sortBy': 'submittedDate',    # 提出日の新しい順にソート
        'sortOrder': 'descending',
    }

    # パラメータをURLエンコードしてクエリ文字列を作成
    query_string = urllib.parse.urlencode(params, safe=':')

    # 完全なAPIリクエストURLを構築
    url = base_url + query_string

    # フィードを取得
    feed = fetch_feed(url)

    def parse_date(date_str):
        try:
            return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        except ValueError as e:
            print(f"Error parsing date: {e}")
            return None

    # Discordに送信した論文の数をカウント
    paper_count = 0

    # 各論文について、5時間以内に公開されたものをフィルタリングして情報を表示
    for entry in feed.entries:
        # 'published' フィールドの日付を解析
        published_str = entry.published
        published = parse_date(published_str)

        if not published:
            continue
        
        # 'published' がtime_thresholdよりも新しい場合のみ処理を続行
        if published >= time_threshold:
            discord_util.send_message(entry)
            paper_count += 1
            
            time.sleep(5)  # 連続して送信しないように5秒待機

    # Discordに完了したことを通知
    discord_util.send_completion_message(paper_count)

if __name__ == '__main__':
    run()