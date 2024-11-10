

#from xact.socket_instance import emit_agent
from xact.llm.openai_client import llm_client
from xact.state import AgentState
from xact.settings import config
from xact.utils.log import logger




agentState = AgentState()


class LLM:
    def __init__(self,model:str=config.XACT_LLM_MODEL):

        self.client = llm_client
        self.model = model

    def generate(self, prompt: str,model:str=config.XACT_LLM_MODEL) -> str:
        self.model = model or self.model
        chat_completion = self.client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt.strip(),
                }
            ],
            model=self.model,
            temperature=0,
        )
        logger.info("llm out generated")
        return chat_completion.choices[0].message.content
