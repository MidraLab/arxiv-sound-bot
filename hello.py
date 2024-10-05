import requests

# ArXiv APIのエンドポイント
base_url = "https://export.arxiv.org/api/query"

# 論文のArXiv ID（例: 2402.10949）
arxiv_id = "2402.10949"

# APIリクエストのパラメータ
params = {
    "id_list": arxiv_id,
    "max_results": 1,
}

# APIリクエストを送信
response = requests.get(base_url, params=params)

# XMLレスポンスをパースする
from xml.etree import ElementTree as ET
root = ET.fromstring(response.text)
print("XMLデータ:")
print(ET.tostring(root, encoding='unicode'))