import os
import base64
import json

class GlobalConfig:
    def __init__(self):
        service = json.loads(base64.b64decode(os.getenv('service')).decode('utf-8'))
        self._config = {
            "deepseek": {
                "api_key": service.get("deepseek", {}).get("api_key"),
            },
            "google": {
                "api_key": service.get("google", {}).get("api_key"),
            },
        }
        
    def get(self, key):
        return self._config.get(key)
    
GLOBAL_CONFIG = GlobalConfig()