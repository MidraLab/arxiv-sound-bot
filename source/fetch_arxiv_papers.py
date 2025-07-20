import urllib.parse
from datetime import datetime, timedelta
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
        # UTCとしてパース（Zはゼロタイムゾーン = UTC）
        dt = datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%SZ')
        # タイムゾーン情報を削除（naiveなdatetimeにする）
        return dt.replace(tzinfo=None)
    except ValueError as e:
        print(f"Error parsing date: {e}")
        return None

def run():
    # 検索クエリを定義（音声合成・音声認識・感情分析に特化）
    # eess.AS: Audio and Speech Processing (音声処理の主要カテゴリ)
    # cs.SD: Sound (音響関連)
    # cs.CL: Computation and Language (音声認識・合成で言語処理を含む場合)
    # これらのカテゴリの論文を取得
    query = 'cat:eess.AS OR cat:cs.SD OR (cat:cs.CL AND (abs:"speech" OR abs:"voice" OR abs:"audio"))'

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
    
    # 7日前の日付を計算（一時的に制限を緩和）
    three_days_ago = datetime.now() - timedelta(days=7)

    # 各論文について、最新のIDと比較して新しいものを処理する
    for entry in feed.entries:
        current_id = entry.id.split('/')[-1]
        current_date = entry.published
        
        # 公開日をdatetimeオブジェクトに変換
        published_datetime = parse_date(current_date)
        if published_datetime is None:
            continue
            
        # 3日以上前の論文はスキップ
        if published_datetime < three_days_ago:
            print(f"3日以上前の論文のためスキップ: {current_date}")
            break

        # 最新のIDが存在しないか、現在のIDが最新のIDよりも新しい場合に処理を続行
        if latest_id is not None and current_id == latest_id:
            print("最新のコンテンツまで到達しました。")
            break
        
        # 環境変数が設定されている場合のみDiscordに送信
        if os.environ.get('DISCORD_WEBHOOK_URL') and os.environ.get('GEMINI_API_KEY'):
            discord_util.send_message(entry)
        else:
            print(f"環境変数未設定のため、Discordへの送信をスキップ: {current_id}")
        paper_count += 1

        # 最初のエントリのデータを保存
        if paper_count == 1:
            save_latest_entry({
                "latest_id": current_id,
                "published_date": current_date
            })

        time.sleep(5)  # 連続して送信しないように5秒待機
    
    # Discordに完了したことを通知（環境変数が設定されている場合のみ）
    if os.environ.get('DISCORD_WEBHOOK_URL') and os.environ.get('GEMINI_API_KEY'):
        discord_util.send_completion_message(paper_count)
    else:
        print(f"処理完了: {paper_count}件の論文を処理しました。")

if __name__ == '__main__':
    run()