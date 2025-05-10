from langchain_google_genai import ChatGoogleGenerativeAI
from constant import Constant
import uuid

from langchain_core.tools import tool

from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

client = genai.Client()

assest_llm = ChatGoogleGenerativeAI(
    model=Constant.GEMINI_FLASH.value,
    temperature=0.7
)

image_llm = ChatGoogleGenerativeAI(
    model=Constant.GEMINI_FLASH_IMAGE.value,
    temperature=0.7
)

generated_img_dir = Constant.GENERATED_IMG.value

@tool
def storyline_generator(prompt: str) -> str:
    """
    Generate a storyline based on the provided prompt.
    """
    PROMPT = """
You are a storyline generator. You will be provided with a prompt, and you need to generate a storyline based on that prompt.
The storyline should be engaging and creative, suitable for a game or a narrative. The prompt will be provided in the following format.
Generate a storyline based on the prompt provided.
Prompt: {}
""".format(prompt)

    response = assest_llm.invoke(
        input=PROMPT,
        generation_config=dict(response_modalities=["TEXT"])
    )
    print(response)
    return response.content

@tool
def quest_generator(prompt: str) -> str:
    """
    Generate a quest based on the provided prompt.
    """
    PROMPT = """
You are a quest generator. You will be provided with a prompt, and you need to generate a quest based on that prompt.
The quest should be engaging and creative, suitable for a game or a narrative. The prompt will be provided in the following format.
Generate a quest based on the prompt provided.
Prompt: {}
""".format(prompt)
    response = assest_llm.invoke(
        input=PROMPT,
        generation_config=dict(response_modalities=["TEXT"])
    )
    return response.content

@tool
def character_dialogue_generator(prompt: str) -> str:
    """
    Generate character dialogues based on the provided prompt.
    """
    PROMPT = """
You are a character dialogue generator. You will be provided with a character description, and you need to generate engaging dialogues for that character.
The dialogues should reflect the character's personality, background, and the context of the game. The character description will be provided in the following format:
Character Name: [Name]
Character Background: [Background]
Character Personality: [Personality]
Generate dialogues for the character based on the description provided.
Prompt: {}
""".format(prompt)
    response = assest_llm.invoke(
        input=PROMPT,
        generation_config=dict(response_modalities=["TEXT"])
    )
    return response.content

@tool
def image_generator(prompt: str) -> str:
    """
    Generate an image based on the provided prompt.
    """
    PROMPT = """
You are an image generator. You will be provided with storyline, character descriptions, and you need to generate a image theme for the game.
The images should reflect the character's personality, background, and the context of the game

Description: {}
    """.format(prompt)
    
    response = client.models.generate_content(
        model=Constant.GEMINI_FLASH_IMAGE.value,
        contents=PROMPT,
        config=types.GenerateContentConfig(
        response_modalities=['Text', 'Image']
        )
    )
    tool_msg = "Generated Image:\n"
    import os
    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            img_num = uuid.uuid4()
            file_path = "{generated_img_dir}/{img_num}.png".format(
                generated_img_dir=generated_img_dir,
                img_num=img_num
            )
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(file_path)
            # Convert image data to base64 for markdown embedding
            tool_msg += "* {}\n".format("/".join(file_path.split("/")[-2:]))
            
    return tool_msg

tools = [
    storyline_generator,
    quest_generator,
    character_dialogue_generator,
    image_generator,
]