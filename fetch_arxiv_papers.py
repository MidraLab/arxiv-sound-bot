import urllib.parse
import feedparser
from datetime import datetime, timedelta

# 現在のUTC時刻を取得
now = datetime.utcnow()

# 24時間前のUTC時刻を取得
time_threshold = now - timedelta(hours=5)

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

# 各論文について、24時間以内に公開されたものをフィルタリングして情報を表示
for entry in feed.entries:
    # 'published' フィールドの日付を解析
    published_str = entry.published
    published = datetime.strptime(published_str, '%Y-%m-%dT%H:%M:%SZ')
    
    # 'published' が24時間以内かを確認
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
        
        print(f'タイトル: {title}')
        print(f'Summary: {summary}')
        print(f'論文のID: {paper_id}')
        print(f'PDFのURL: {pdf_url}')
        print(f'カテゴリー: {categories}')
        print('-' * 80)