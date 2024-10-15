import google.generativeai as genai

class GeminiUtil:
    def __init__(self):
        self.api_key = WEBHOOK_URL = os.environ.get('GENIMI_API_KEY')
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction="あなたは日本と英語の翻訳を行うAIです。渡した内容の文章を日本語に翻訳してください。"
        )
    
    def translate(self, text) -> str:
        """

        Args:
            text (_type_): _description_

        Returns:
            str: _description_
        """
        res = model.generate_content(text)
        return res.text