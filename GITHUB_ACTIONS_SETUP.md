# GitHub Actions セットアップガイド

このボットはGitHub Actionsを使用して自動実行できます。

## 必要なシークレットの設定

GitHubリポジトリの Settings > Secrets and variables > Actions から以下のシークレットを設定してください：

### 既に設定済みのシークレット
- **GEMINI_API_KEY** ✅ - 設定済み（必須）
- **DISCORD_WEBHOOK_URL** ✅ - 設定済み（サウンド論文用として使用）

### 追加で設定が必要なシークレット（オプション）
以下は3DモデルやモーションカテゴリーをDiscordに通知したい場合のみ設定：

- **DISCORD_WEBHOOK_3D** - 3Dモデル生成論文用のDiscord Webhook URL
- **DISCORD_WEBHOOK_MOTION** - モーション生成論文用のDiscord Webhook URL

※ これらのWebhook URLは、Discordチャンネルの設定 > 連携サービス > ウェブフックから作成できます。

## 現在の動作
既存の設定で、音声処理関連の論文のみがDiscordに通知されます。
3Dモデルとモーションカテゴリーは、対応するWebhookが設定されていないためスキップされます。

## 実行スケジュール

デフォルトでは毎日JST 9:00（UTC 0:00）に実行されます。

`.github/workflows/arxiv-fetch.yml`の`cron`設定を変更することで、実行時間を調整できます：

```yaml
schedule:
  - cron: '0 0 * * *'  # 毎日 UTC 0:00
```

### cron書式の例
- `0 0 * * *` - 毎日 UTC 0:00（JST 9:00）
- `0 12 * * *` - 毎日 UTC 12:00（JST 21:00）
- `0 0 * * 1` - 毎週月曜日 UTC 0:00
- `0 0,12 * * *` - 毎日 UTC 0:00と12:00

## 手動実行

Actions タブから「Fetch ArXiv Papers」ワークフローを選択し、「Run workflow」ボタンで手動実行も可能です。

## 状態ファイルの管理

- ボットは`opt/`ディレクトリに各カテゴリの最新論文IDを保存します
- GitHub Actionsは実行後、これらのファイルを自動的にコミット・プッシュします
- これにより、重複した論文の通知を防ぎます

## トラブルシューティング

### エラー: "API key not valid"
→ `GEMINI_API_KEY`シークレットが正しく設定されているか確認

### エラー: "Discord webhook URLが設定されていません"
→ 対応するDiscord Webhookシークレットが設定されているか確認

### 論文が取得されない
→ Actions実行ログで検索クエリの結果を確認
→ `config.json`の`days_to_check`を確認（デフォルト7日）

## カテゴリの無効化

特定のカテゴリを無効にしたい場合は、対応するWebhookシークレットを設定しないでください。
そのカテゴリはスキップされます。