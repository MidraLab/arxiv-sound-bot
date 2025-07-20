import feedparser
import requests
import time

MAX_RETRIES = 3
RETRY_WAIT_TIME = 5  # 秒

# フィードを取得する関数を定義
def fetch_feed(url, retries=MAX_RETRIES) -> feedparser.FeedParserDict:
    for attempt in range(retries):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # HTTPエラーが発生した場合に例外を発生させる
            return feedparser.parse(response.content)
        except (requests.exceptions.RequestException, ConnectionResetError) as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(RETRY_WAIT_TIME)
            else:
                print("Failed to fetch feed after multiple attempts.")
                raise  # 最終試行でも失敗した場合は例外を再発生させる