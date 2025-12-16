from openai import OpenAI
from dotenv import load_dotenv
import os

class OpenAIUtil:
    def __init__(self):
        load_dotenv()
        self.client = OpenAI(api_key=os.environ.get('OPENAI_API_KEY'))

    def translate(self, text) -> str:
        """
        Translate English text to Japanese using OpenAI GPT-5 nano.

        Args:
            text: English text to translate

        Returns:
            str: Japanese translation
        """
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "あなたは日本語と英語の翻訳を行うAIです。渡した内容の文章を日本語に翻訳してください。"},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content
