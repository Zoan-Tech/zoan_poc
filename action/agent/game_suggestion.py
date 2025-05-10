from action.agent import BaseAgent
from langchain_core.prompts import ChatPromptTemplate
from action.agent.tools import game_suggestion

from config.prompt import GameSuggestorPrompt


class GameSuggestor(BaseAgent):
    def __init__(self, modules=[], **kwargs):
        """
        Initialize the ProductStatus agent.
        """
        # Define the prompt for the agent
        prompt = ChatPromptTemplate.from_messages([
            ("system", GameSuggestorPrompt.SYSTEM),
            ("placeholder", "{messages}"),
        ])
        
        super().__init__(modules, prompt=prompt, **kwargs)

modules = [game_suggestion]