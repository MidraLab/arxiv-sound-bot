import urllib.parse
import feedparser

# 検索クエリを定義
query = 'all:"LLM" OR all:"Text to Speech" OR all:"Speech to Text" OR all:"AI Character"'

# クエリをURLエンコード
encoded_query = urllib.parse.quote(query)

# ベースとなるAPIのURL
base_url = 'http://export.arxiv.org/api/query?'

# APIパラメータの設定
params = {
    'search_query': encoded_query,
    'start': 0,            # 取得開始位置
    'max_results': 10,     # 取得する結果の最大数
    'sortBy': 'submittedDate',   # 提出日の新しい順にソート
    'sortOrder': 'descending',
}

# パラメータをURLエンコードしてクエリ文字列を作成
query_string = '&'.join(f'{key}={value}' for key, value in params.items())

# 完全なAPIリクエストURLを構築
url = base_url + query_string

# フィードをパース
feed = feedparser.parse(url)

# 各論文についてタイトルと要約を表示
for entry in feed.entries:
    title = entry.title
    summary = entry.summary.replace('\n', ' ')  # 改行を削除して整形
    print(f'タイトル: {title}')
    print(f'要約: {summary}')
    print('-' * 80)