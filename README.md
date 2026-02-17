# ArXiv Sound Bot
ArXivから音声処理・3Dモデル生成・モーション生成・AI Townシミュレーションなどに関する論文を取得し、Discordに通知するボット

> 📌 **既存ユーザーの方へ**: シングルカテゴリー版からの移行は[MIGRATION_GUIDE.md](MIGRATION_GUIDE.md)を参照してください。

## 機能
- 複数カテゴリの論文を監視
  - 音声処理（音声合成・認識・感情分析）
  - 3Dモデル生成（NeRF、Gaussian Splatting等）
  - モーション生成（アニメーション、人体動作）
  - 動画生成（テキストから動画生成）
  - セキュリティインテリジェンス（脅威分析・マルウェア検知）
  - AI Town系シミュレーション（生成エージェント社会・マルチエージェントシミュレーション）
- 各カテゴリごとに異なるDiscordチャンネルに通知
- 論文要約を日本語に翻訳（OpenAI GPT-5 nano使用）

## セットアップ
```bash
# 依存関係のインストール
uv sync

# 環境変数の設定
cp .env.example .env
# .envファイルを編集して必要な情報を設定
```

## 環境変数
- `OPENAI_API_KEY`: OpenAI APIキー（必須）
- `DISCORD_WEBHOOK_SOUND`: 音声処理論文用のWebhook URL
- `DISCORD_WEBHOOK_3D`: 3Dモデル生成論文用のWebhook URL
- `DISCORD_WEBHOOK_MOTION`: モーション生成論文用のWebhook URL
- `DISCORD_WEBHOOK_MOVIE`: 動画生成論文用のWebhook URL
- `DISCORD_WEBHOOK_INTELLIGENCE`: セキュリティインテリジェンス論文用のWebhook URL
- `DISCORD_WEBHOOK_AI_TOWN`: AI Town系シミュレーション論文用のWebhook URL

## 実行
```bash
uv run python source/fetch_arxiv_papers.py
```

## 設定
`config.json`で以下を設定可能：
- 各カテゴリの検索クエリ
- 最大取得論文数
- チェック対象日数
- 待機時間

## 定期実行

### GitHub Actions（推奨）
GitHub Actionsで自動実行する場合は、リポジトリのSecretsに以下を設定：
- `OPENAI_API_KEY`
- `DISCORD_WEBHOOK_SOUND`
- `DISCORD_WEBHOOK_3D`
- `DISCORD_WEBHOOK_MOTION`
- `DISCORD_WEBHOOK_MOVIE`
- `DISCORD_WEBHOOK_INTELLIGENCE`
- `DISCORD_WEBHOOK_AI_TOWN`

詳細は[GITHUB_ACTIONS_SETUP.md](GITHUB_ACTIONS_SETUP.md)を参照。

### ローカルcron
```bash
0 9 * * * cd /path/to/arxiv-sound-bot && uv run python source/fetch_arxiv_papers.py
```