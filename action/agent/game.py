from action.agent import BaseAgent
from langchain_core.prompts import ChatPromptTemplate

from action.agent.tools import game
from config.prompt import GameGeneratorPrompt


class GameGenerator(BaseAgent):
    def __init__(self, modules=[], **kwargs):
        """
        Initialize the ProductStatus agent.
        """
        # Define the prompt for the agent
        prompt = ChatPromptTemplate.from_messages([
            ("system", GameGeneratorPrompt.SYSTEM),
            ("placeholder", "{messages}"),
        ])
        
        super().__init__(modules, prompt=prompt, **kwargs)

modules = [game]