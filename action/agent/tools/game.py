from typing import (
    Annotated,
    Optional,
)
from langchain_google_genai import ChatGoogleGenerativeAI
from constant import Constant
import uuid

from langchain_core.tools import tool

llm = ChatGoogleGenerativeAI(
    model=Constant.GEMINI_FLASH.value,
    temperature=0.7
)

import os
base_assest_path = Constant.ASSET_LIBRARY_PATH.value
generated_game_dir = Constant.GENERATED_GAME.value

asset_folder = {
    "monad": [f for f in os.listdir(os.path.join(base_assest_path, "monad")) if os.path.isfile(os.path.join(base_assest_path, "monad", f))],
    "zoan": [f for f in os.listdir(os.path.join(base_assest_path, "zoan")) if os.path.isfile(os.path.join(base_assest_path, "zoan", f))],
    "emmy": [f for f in os.listdir(os.path.join(base_assest_path, "emmy")) if os.path.isfile(os.path.join(base_assest_path, "emmy", f))],
    "six_pose": [f for f in os.listdir(os.path.join(base_assest_path, "six_pose")) if os.path.isfile(os.path.join(base_assest_path, "six_pose", f))]
}

def load_sample_game(file_name=None):
    """
    Load a sample game specification.
    """
    if not file_name:
        with open(Constant.REF_GAME_FILE.value, 'r') as file:
            return file.read()
    else:
        with open(file_name, 'r') as file:
            return file.read()

@tool
def load_provider_asset(provider: Annotated[str, "provider name"]):
    """
    Load the provider asset.
    """
    return asset_folder.get(provider, [])

@tool
def game_generator(
    specification: Annotated[str, "game specification"],
    provider: Annotated[str, "asset's provider name"], assets: Annotated[str, "the character states and their corresponding assets name chosen by user"],
    adjustment: Optional[Annotated[str, "the file name of the game code that the customer wants to adjust"]] = None
):
    """
    Generate a python game based on the provided request.
    """
    game_example = load_sample_game()
    
    PROMPT = """
You are a game generator. You will be provided with a specification, and you need to generate a game based on that specification.
The game should be engaging and creative, including simple interface using Python and pygame package.
Create a Python game with these specifications:
{specification}
The game should include the following assets:
{assets}
Remember to resize the assets to fit the game screen and suitable display. Remember which assets to be loaded and which to be created. The created assets should be simple shapes or colors.

The current path to load the assets is {base_assest_path}/{provider}.
Only generate valid Python code without explanations.
The code should be complete and runnable.

Here is an example of a simple snake game:
{game_example}
""".format(specification=specification, assets=assets, base_assest_path=base_assest_path, provider=provider, game_example=game_example)

    if adjustment:
        game_code = load_sample_game(adjustment)
        PROMPT += f"""
Here is the game code that the customer wants to adjust:
{game_code}
The customer wants to adjust the game code above. Please make the necessary adjustments and provide the updated code.
"""

    response = llm.invoke(
        input=PROMPT,
        generation_config=dict(response_modalities=["TEXT"])
    )
    
    game_code = response.content.replace("```python", "").replace("```", "")
    filename = f"generated_game_{uuid.uuid4()}.py"
    filename = os.path.join(generated_game_dir, filename)
    
    with open(filename, 'w') as file:
        file.write(game_code)
        
    return "Game code generated successfully. You can find it at: " + "/".join(filename.split("/")[-2:])

tools = [
    load_provider_asset,
    game_generator,
]