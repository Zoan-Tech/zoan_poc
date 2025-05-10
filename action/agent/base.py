import json, logging
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from langchain_core.messages import (
    AIMessage,
    HumanMessage,
    ToolMessage,
)

from functools import reduce

class BaseAgent:
    def __init__(self, modules=[], model_name="gpt-4o", prompt="", mode="openai", **kwargs):
        tools = reduce(lambda acc, module: acc + module.tools, modules, [])
        chat_model = self.get_chat_model(mode)
        llm = chat_model(model=model_name)
        self.agent_executor = create_react_agent(llm, tools=tools, prompt=prompt)
        
    def get_chat_model(self, mode="openai") -> object:
        if mode == "openai":
            return ChatOpenAI
        elif mode == "google":
            return ChatGoogleGenerativeAI
        else:
            return None

    def process_invoke_result(self, result) -> tuple:
        intermediate_steps = []
        answer = None
        try:
            for i, r in enumerate(result["messages"]):
                step = {}

                if isinstance(r, HumanMessage):
                    step["HumanMessage"] = r.model_dump(include=["content"])

                elif isinstance(r, AIMessage):
                    step["AIMessage"] = r.model_dump(include=["content", "tool_calls"])
                elif isinstance(r, ToolMessage):
                    step["ToolMessage"] = r.model_dump(include=["content"])
                
                intermediate_steps.append(step)
            
            # Get the agent outcome
            answer = result.get("messages")[-1].content
        except Exception as e:
            logging.error(f"Error in file {__file__.split('/')[-1]} at line {e.__traceback__.tb_lineno}: {str(e)}")
            answer = "Đã xảy ra lỗi, vui lòng thử lại sau nhé."
            intermediate_steps = []
            
        return answer, intermediate_steps

    def invoke(self, question: str, history: str, **kwargs) -> str:
        """
        Get the product status based on the question.
        """ 
        inputs = {
            "messages": [
                ("user", "history: " + history),
                ("user", question),
            ]
        }
        
        config = {}

        result = self.agent_executor.invoke(
            inputs,
            config=config,
        )
        
        answer, intermediate_steps = self.process_invoke_result(result)
            
        return answer, intermediate_steps