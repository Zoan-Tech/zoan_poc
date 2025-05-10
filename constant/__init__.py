from enum import Enum
from constant.llm_model import LLMModel
import os

class Constant(Enum):
    """
    This class contains constants used in the application.
    """
    # LLM Model
    GEMINI_FLASH = LLMModel.GEMINI_FLASH.value
    GEMINI_FLASH_IMAGE = LLMModel.GEMINI_FLASH_IMAGE.value

    # Project working directory
    PWD = os.getcwd()

    # Asset Library Path
    ASSET_LIBRARY_PATH = f"{PWD}/asset_library"
    
    # Geneerated Directory
    GENERATED_IMG = f"{PWD}/generated_img"
    GENERATED_GAME = f"{PWD}/generated_game"
    
    
    # File Path
    HISTORY_FILE = f"{PWD}/history.txt"
    REF_GAME_FILE = f"{PWD}/reference/snake_game.py"