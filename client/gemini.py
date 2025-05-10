from google import genai
from config import GLOBAL_CONFIG

class GeminiClient:
    def __init__(self):
        self.client = genai.Client(api_key=GLOBAL_CONFIG.get("gemini_api_key"))
        
gemini_client = GeminiClient()