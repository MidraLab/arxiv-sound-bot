from dotenv import load_dotenv
import os
import requests
from gemini_util import GeminiUtil as GeminiUtilClass

class DiscordUtil:
    def __init__(self):
        """discord utilの初期化
        """
        load_dotenv()
        self.discord_web_hook = os.environ.get('DISCORD_WEBHOOK_URL')
        self.gemini_util = GeminiUtilClass()  # インスタンス生成
        
    def send_message(self, entry) -> None:
        """
        Send message to discord webhook

        Args:
            entry (dict): the paper entry to send
        """
        
        title = entry.title
        summary = entry.summary.replace('\n', ' ')  # 改行を削除して整形
        paper_id = entry.id.split('/abs/')[-1]
        pdf_url = ''
        for link in entry.links:
            if 'title' in link and link.title == 'pdf':
                pdf_url = link.href
                break
        categories = ', '.join(tag['term'] for tag in entry.tags)
        
        # URLを生成
        arxiv_url = f"https://arxiv.org/abs/{paper_id}"
        alphaxiv_url = f"https://www.alphaxiv.org/abs/{paper_id}"
        
        # 論文情報をフォーマット
        message_content = (
            f"📄 **{title}**\n\n"
            f"📝 **要約（日本語）:**\n{self.gemini_util.translate(summary)}\n\n"
            f"🔗 **リンク:**\n"
            f"• [AlphaXivで読む]({alphaxiv_url}) - コメント・議論付き\n"
            f"• [PDF]({pdf_url}) | [arXiv]({arxiv_url})\n\n"
            f"🏷️ **カテゴリ:** {categories}\n"
            f"📅 **公開日:** {entry.published}"
        )

        # Discordに送信するペイロードを作成
        payload = {
            'content': message_content
        }
        
        print(message_content)

        # DiscordのWebhookにPOSTリクエストを送信
        response = requests.post(self.discord_web_hook, data=payload)

        if response.status_code != 204:
            print(f'Failed to send message for paper ID {paper_id}. Status code: {response.status_code}.message count: {len(message_content)}')
        else:
            print(f'Sent paper ID {paper_id} to Discord.')
    
    def send_completion_message(self, paper_count) -> None:
        """discord に情報を送信したことを通知するメッセージを送信

        Args:
            paper_count (_type_): _description_
        """
            # この時間の通知が完了したことを通知
        payload = {
            'content': f'✅ 新着論文の通知が完了しました\n📊 送信した論文数: {paper_count}件'
        }

        response = requests.post(self.discord_web_hook, data=payload)

        if response.status_code != 204:
            print(f'Failed to send completion message. Status code: {response.status_code}')
        else:
            print('Sent completion message to Discord.')
        print(f'Total {paper_count} papers sent to Discord.')