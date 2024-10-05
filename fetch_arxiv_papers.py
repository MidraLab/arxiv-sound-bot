import urllib.parse
import feedparser
from datetime import datetime, timedelta
import requests  # Discordへの送信に使用
import os

# DiscordのWebhook URLを環境変数から取得
WEBHOOK_URL = os.environ.get('DISCORD_WEBHOOK_URL')

if not WEBHOOK_URL:
    print('Error: DISCORD_WEBHOOK_URL is not set.')
    exit(1)

# 現在のUTC時刻を取得
now = datetime.utcnow()

# 3時間前のUTC時刻を取得
time_threshold = now - timedelta(hours=3)

# 検索クエリを定義
# Computer Scienceのカテゴリを指定
query = 'cat:cs.*'

# ベースとなるAPIのURL
base_url = 'http://export.arxiv.org/api/query?'

# APIパラメータの設定
params = {
    'search_query': query,
    'start': 0,                   # 取得開始位置
    'max_results': 300,           # 取得する結果の最大数（必要に応じて増やしてください）
    'sortBy': 'submittedDate',    # 提出日の新しい順にソート
    'sortOrder': 'descending',
}

# パラメータをURLエンコードしてクエリ文字列を作成
query_string = urllib.parse.urlencode(params, safe=':')

# 完全なAPIリクエストURLを構築
url = base_url + query_string

# フィードをパース
feed = feedparser.parse(url)

# Discordに送信した論文の数をカウント
paper_count = 0

# 各論文について、3時間以内に公開されたものをフィルタリングして情報を表示
for entry in feed.entries:
    # 'published' フィールドの日付を解析
    published_str = entry.published
    published = datetime.strptime(published_str, '%Y-%m-%dT%H:%M:%SZ')
    
    # 'published' が3時間以内かを確認
    if published >= time_threshold:
        title = entry.title
        summary = entry.summary.replace('\n', ' ')  # 改行を削除して整形
        paper_id = entry.id.split('/abs/')[-1]
        pdf_url = ''
        for link in entry.links:
            if 'title' in link and link.title == 'pdf':
                pdf_url = link.href
                break
        categories = ', '.join(tag['term'] for tag in entry.tags)
        
        # 論文情報をフォーマット
        message_content = f"""**タイトル:** {title}
**Summary:** {summary}
**論文のID:** {paper_id}
**PDFのURL:** {pdf_url}
**カテゴリー:** {categories}"""

        # Discordに送信するペイロードを作成
        payload = {
            'content': message_content
        }

        # DiscordのWebhookにPOSTリクエストを送信
        response = requests.post(WEBHOOK_URL, data=payload)

        if response.status_code != 204:
            print(f'Failed to send message for paper ID {paper_id}. Status code: {response.status_code}')
        else:
            print(f'Sent paper ID {paper_id} to Discord.')
            paper_count += 1

# 処理が完了したことを表示
print(f'Total {paper_count} papers sent to Discord.')