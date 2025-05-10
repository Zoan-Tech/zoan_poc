import os
from dotenv import load_dotenv
from constant import Constant
from config import GLOBAL_CONFIG

def init_folder_generation():
    if not os.path.exists(Constant.GENERATED_IMG.value):
        os.makedirs(Constant.GENERATED_IMG.value)
        
    if not os.path.exists(Constant.GENERATED_GAME.value):
        os.makedirs(Constant.GENERATED_GAME.value)

def init_history_file():
    if not os.path.exists(Constant.HISTORY_FILE.value):
        with open(Constant.HISTORY_FILE.value, "w") as f:
            f.write("")
        
def init_env_variables():
    os.environ["DEEPSEEK_API_KEY"] = GLOBAL_CONFIG.get("deepseek").get("api_key")
    os.environ["GOOGLE_API_KEY"] = GLOBAL_CONFIG.get("google").get("api_key")

def init():
    load_dotenv()
    init_folder_generation()
    init_env_variables()
    init_history_file()