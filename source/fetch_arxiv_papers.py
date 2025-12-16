import urllib.parse
from datetime import datetime, timedelta
import requests  
import time
import os
import json
from discord_util import DiscordUtil
from arxiv import fetch_feed

JSON_FILE_DIR = "opt"

def save_latest_entry(latest_entry, json_file_path):
    """最新のエントリ（IDや公開日など）を保存する"""
    if not os.path.exists(JSON_FILE_DIR):
        os.makedirs(JSON_FILE_DIR)
    with open(json_file_path, 'w') as f:
        json.dump(latest_entry, f)

def load_latest_entry(json_file_path):
    """最新のエントリ（IDや公開日など）を読み込む"""
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as f:
            data = json.load(f)
            return data
    else:
        if not os.path.exists(JSON_FILE_DIR):
            os.makedirs(JSON_FILE_DIR)
        with open(json_file_path, 'w') as f:
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

def load_config():
    """設定ファイルを読み込む"""
    config_path = "config.json"
    if not os.path.exists(config_path):
        print(f"設定ファイル {config_path} が見つかりません。")
        return None
    
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def process_category(category_config, config):
    """カテゴリごとに論文を処理する"""
    print(f"\n=== {category_config['name']} ({category_config['description']}) の処理を開始 ===")
    
    # Discord webhook URLを環境変数から取得
    webhook_url = os.environ.get(category_config['webhook_env'])
    if not webhook_url:
        print(f"警告: {category_config['webhook_env']} が設定されていません。このカテゴリをスキップします。")
        return 0
    
    # DiscordUtilインスタンスを作成（webhook URL付き）
    discord_util = DiscordUtil(webhook_url)
    
    # ベースとなるAPIのURL
    base_url = 'http://export.arxiv.org/api/query?'
    
    # APIパラメータの設定
    params = {
        'search_query': category_config['query'],
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
    json_file_path = category_config['json_file']
    latest_entry = load_latest_entry(json_file_path)
    latest_id = latest_entry.get("latest_id", None)
    
    # Discordに送信した論文の数をカウント
    paper_count = 0
    
    # 指定日数前の日付を計算
    days_ago = datetime.now() - timedelta(days=config.get('days_to_check', 7))
    
    # 各論文について、最新のIDと比較して新しいものを処理する
    for entry in feed.entries:
        current_id = entry.id.split('/')[-1]
        current_date = entry.published
        
        # 公開日をdatetimeオブジェクトに変換
        published_datetime = parse_date(current_date)
        if published_datetime is None:
            continue
            
        # 指定日数以上前の論文はスキップ
        if published_datetime < days_ago:
            print(f"{config.get('days_to_check', 7)}日以上前の論文のためスキップ: {current_date}")
            break
        
        # 最新のIDが存在しないか、現在のIDが最新のIDよりも新しい場合に処理を続行
        if latest_id is not None and current_id == latest_id:
            print("最新のコンテンツまで到達しました。")
            break
        
        # カテゴリ別の最大論文数に達した場合は終了
        if paper_count >= config.get('max_papers_per_category', 10):
            print(f"カテゴリ別の最大論文数（{config.get('max_papers_per_category', 10)}件）に達しました。")
            break
        
        # 環境変数が設定されている場合のみDiscordに送信
        if os.environ.get('OPENAI_API_KEY'):
            discord_util.send_message(entry)
        else:
            print(f"環境変数未設定のため、Discordへの送信をスキップ: {current_id}")
        paper_count += 1
        
        # 最初のエントリのデータを保存
        if paper_count == 1:
            save_latest_entry({
                "latest_id": current_id,
                "published_date": current_date
            }, json_file_path)
        
        time.sleep(config.get('wait_time_seconds', 5))  # 連続して送信しないように待機
    
    # Discordに完了したことを通知（環境変数が設定されている場合のみ）
    if os.environ.get('OPENAI_API_KEY') and paper_count > 0:
        discord_util.send_completion_message(paper_count, category_config['name'])
    else:
        print(f"処理完了: {paper_count}件の論文を処理しました。")
    
    return paper_count

def run():
    """メイン処理"""
    # 設定ファイルを読み込む
    config = load_config()
    if not config:
        return
    
    # OpenAI APIキーの確認
    if not os.environ.get('OPENAI_API_KEY'):
        print("エラー: OPENAI_API_KEY が設定されていません。")
        return
    
    # 各カテゴリを処理
    total_papers = 0
    for category in config.get('categories', []):
        papers_processed = process_category(category, config)
        total_papers += papers_processed
        
        # カテゴリ間の待機時間
        if papers_processed > 0:
            time.sleep(10)  # カテゴリ間は10秒待機
    
    print(f"\n=== 全体の処理完了: 合計 {total_papers}件の論文を処理しました ===")

if __name__ == '__main__':
    run()