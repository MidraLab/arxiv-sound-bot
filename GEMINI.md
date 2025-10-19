# GEMINI.md: arxiv-sound-bot

## プロジェクト概要

このプロジェクトは、arXivプレプリントサーバーを監視し、音声処理、3Dモデル生成、モーション合成などの複数の科学カテゴリにわたる新しい論文を検出するPythonベースのボットです。Gemini APIを利用して論文の要旨を日本語に翻訳し、整形された通知を各カテゴリ専用のDiscordチャンネルに投稿します。

このボットは、GitHub Actionsを使用してスケジュール通りに自動実行されるように設計されています。各カテゴリで最後に処理した論文のIDを保存することで状態を維持し、新しい論文のみを報告します。

**主要技術:**
- **言語:** Python 3.10
- **パッケージ管理:** `uv`
- **コアライブラリ:** `requests` (HTTPリクエスト)、`feedparser` (arXivフィード解析)、`google-generativeai` (翻訳)、`python-dotenv` (環境変数管理)
- **CI/CD:** GitHub Actions (スケジュール実行)
- **設定:** `config.json` (検索クエリ、カテゴリ)、`.env` (APIキーなど)

## ビルドと実行

### 前提条件
- Python 3.10以上
- `uv` パッケージマネージャー

### セットアップ
1.  **依存関係のインストール:**
    ```bash
    uv sync
    ```

2.  **環境設定:**
    サンプルをコピーして`.env`ファイルを作成し、APIキーとWebhook URLを記入します。
    ```bash
    cp .env.example .env
    ```
    **環境変数:**
    - `GEMINI_API_KEY`: あなたのGoogle Gemini APIキー
    - `DISCORD_WEBHOOK_SOUND`: 音声カテゴリ用のDiscord Webhook URL
    - `DISCORD_WEBHOOK_3D`: 3Dモデルカテゴリ用のDiscord Webhook URL
    - `DISCORD_WEBHOOK_MOTION`: モーションカテゴリ用のDiscord Webhook URL

### 手動実行
ボットを手動で実行し、最新の論文を取得するには:
```bash
uv run python source/fetch_arxiv_papers.py
```

### スケジュール実行 (GitHub Actions)
このプロジェクトには、毎日00:00 UTC (日本時間9:00) にボットを実行するGitHub Actionsワークフロー (`.github/workflows/arxiv-fetch.yml`) が含まれています。実行には、リポジトリに以下のシークレットを設定する必要があります:
- `GEMINI_API_KEY`
- `DISCORD_WEBHOOK_SOUND`
- `DISCORD_WEBHOOK_3D`
- `DISCORD_WEBHOOK_MOTION`

このアクションは取得スクリプトを実行し、更新された状態ファイル (`opt/*.json`) をリポジトリにコミットします。

## 開発規約

- **設定:** すべての運用パラメータ (検索クエリ、カテゴリ、論文数上限など) は `config.json` で定義されます。これにより、コードを変更することなくボットの動作を簡単に変更できます。
- **状態管理:** ボットは、最後に取得した論文のIDと発行日を `opt/` ディレクトリ内のJSONファイルに保存することで、処理済みの論文を追跡します。各カテゴリには専用の状態ファイル (例: `sound_info.json`) があります。
- **モジュール性:** コードは `source/` ディレクトリ内の複数のモジュールに整理されています:
    - `fetch_arxiv_papers.py`: プロセス全体を調整するメインの実行スクリプト
    - `arxiv.py`: arXiv APIとの通信を処理
    - `discord_util.py`: Discordへのメッセージの整形と送信を管理
    - `gemini_util.py`: (推定) Gemini APIと連携して翻訳を行うロジックを格納
- **環境変数:** APIキーやWebhook URLのような秘匿情報は、ローカル開発では `.env` ファイルから、本番環境ではGitHubのシークレットから読み込まれます。