from client.gemini import gemini_client

class GeminiService:
    def __init__(self):
        self.client = gemini_client.client
    
    def generate(self, message):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash",
            contents=message,
        )
        
        return response