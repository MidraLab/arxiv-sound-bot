from dotenv import load_dotenv
import os
import requests
from openai_util import OpenAIUtil

class DiscordUtil:
    def __init__(self, webhook_url=None):
        """discord utilの初期化
        
        Args:
            webhook_url (str, optional): Discord webhook URL. If not provided, uses DISCORD_WEBHOOK_URL from env.
        """
        load_dotenv()
        self.discord_web_hook = webhook_url or os.environ.get('DISCORD_WEBHOOK_URL')
        self.openai_util = OpenAIUtil()  # インスタンス生成
        
    def send_message(self, entry) -> None:
        """
        Send message to discord webhook

        Args:
            entry (dict): the paper entry to send
        """
        if not self.discord_web_hook:
            print("Discord webhook URLが設定されていません。")
            return
        
        title = entry.title
        summary = entry.summary.replace('\n', ' ')  # 改行を削除して整形
        paper_id = entry.id.split('/abs/')[-1]
        pdf_url = ''
        for link in entry.links:
            if 'title' in link and link.title == 'pdf':
                pdf_url = link.href
                break
        categories = ', '.join(tag['term'] for tag in entry.tags)
        
        # URLを生成（<>で囲むとプレビューが無効になる）
        arxiv_url = f"<https://arxiv.org/abs/{paper_id}>"
        alphaxiv_url = f"<https://www.alphaxiv.org/abs/{paper_id}>"
        
        # 論文情報をフォーマット
        message_content = (
            f"📄 **{title}**\n\n"
            f"📝 **要約（日本語）:**\n{self.openai_util.translate(summary)}\n\n"
            f"🔗 **リンク:**\n"
            f"• [AlphaXivで読む]({alphaxiv_url}) - コメント・議論付き\n"
            f"• [PDF](<{pdf_url}>) | [arXiv]({arxiv_url})\n\n"
            f"🏷️ **カテゴリ:** {categories}\n"
            f"📅 **公開日:** {entry.published}"
        )

        # Discordに送信するペイロードを作成
        payload = {
            'content': message_content
        }
        
        print(f"論文ID {paper_id} を処理中...")

        # DiscordのWebhookにPOSTリクエストを送信
        response = requests.post(self.discord_web_hook, data=payload)

        if response.status_code != 204:
            print(f'Failed to send message for paper ID {paper_id}. Status code: {response.status_code}.message count: {len(message_content)}')
        else:
            print(f'Sent paper ID {paper_id} to Discord.')
    
    def send_completion_message(self, paper_count, category_name="") -> None:
        """discord に情報を送信したことを通知するメッセージを送信

        Args:
            paper_count (int): 送信した論文数
            category_name (str, optional): カテゴリ名
        """
        if not self.discord_web_hook:
            print("Discord webhook URLが設定されていません。")
            return
            
        # カテゴリ名を含めたメッセージ
        category_text = f"（{category_name}）" if category_name else ""
        
        # この時間の通知が完了したことを通知
        payload = {
            'content': f'✅ 新着論文{category_text}の通知が完了しました\n📊 送信した論文数: {paper_count}件'
        }

        response = requests.post(self.discord_web_hook, data=payload)

        if response.status_code != 204:
            print(f'Failed to send completion message. Status code: {response.status_code}')
        else:
            print(f'Sent completion message to Discord.')
        print(f'Total {paper_count} papers sent to Discord for {category_name}.')