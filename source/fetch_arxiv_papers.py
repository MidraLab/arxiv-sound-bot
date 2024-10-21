import urllib.parse
from datetime import datetime
import requests  
import time
import os
import json
from discord_util import DiscordUtil
from arxiv import fetch_feed

discord_util = DiscordUtil()  
JSON_FILE_DIR = "opt"
JSON_FILE_PATH = os.path.join(JSON_FILE_DIR, "contents_info.json")

def save_latest_entry(latest_entry):
    """最新のエントリ（IDや公開日など）を保存する"""
    if not os.path.exists(JSON_FILE_DIR):
        os.makedirs(JSON_FILE_DIR)
    with open(JSON_FILE_PATH, 'w') as f:
        json.dump(latest_entry, f)

def load_latest_entry():
    """最新のエントリ（IDや公開日など）を読み込む"""
    if os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'r') as f:
            data = json.load(f)
            return data
    else:
        if not os.path.exists(JSON_FILE_DIR):
            os.makedirs(JSON_FILE_DIR)
        with open(JSON_FILE_PATH, 'w') as f:
            json.dump({}, f)
    return {}

def parse_date(date_str):
    """日付を解析する"""
    try:
        return datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return None

def run():
    # 検索クエリを定義
    query = 'cat:cs.SD'

    # ベースとなるAPIのURL
    base_url = 'http://export.arxiv.org/api/query?'

    # APIパラメータの設定
    params = {
        'search_query': query,
        'start': 0,                   
        'max_results': 100,           
        'sortBy': 'submittedDate',    
        'sortOrder': 'descending',
    }

    # パラメータをURLエンコードしてクエリ文字列を作成
    query_string = urllib.parse.urlencode(params, safe=':')

    # 完全なAPIリクエストURLを構築
    url = base_url + query_string

    # フィードを取得
    feed = fetch_feed(url)

    # 最新のエントリ情報を読み込む
    latest_entry = load_latest_entry()
    latest_id = latest_entry.get("latest_id", None)

    # Discordに送信した論文の数をカウント
    paper_count = 0

    # 各論文について、最新のIDと比較して新しいものを処理する
    for entry in feed.entries:
        current_id = entry.id.split('/')[-1]
        current_date = entry.published

        # 最新のIDが存在しないか、現在のIDが最新のIDよりも新しい場合に処理を続行
        if latest_id is not None and current_id == latest_id:
            print("最新のコンテンツまで到達しました。")
            break
        
        discord_util.send_message(entry)
        paper_count += 1

        # 最初のエントリのデータを保存
        if paper_count == 1:
            save_latest_entry({
                "latest_id": current_id,
                "published_date": current_date
            })

        time.sleep(5)  # 連続して送信しないように5秒待機
    
    # Discordに完了したことを通知
    discord_util.send_completion_message(paper_count)

if __name__ == '__main__':
    run()