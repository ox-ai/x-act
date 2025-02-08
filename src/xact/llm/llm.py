from typing import Any, Literal
from xact.config.config import ConfigVar
from xact.llm.openai_client import llm_client
from xact.config.gen import config
from xact.log.config import log_manager

log = log_manager.init(__name__)


class LLM:
    def __init__(self, model: str = None):

        self.client = llm_client
        self.model = ConfigVar(model, config.XACT_LLM_MODEL)

    def get_model(self):
        return self.model()

    def generate(
        self,
        prompt: str = None,
        model: str = None,
        messages: list = None,
        temperature:int=0,
        response_format: Any = None,
        generate_format: Literal[
            "chat",
            "gen",
            "struct",
        ] = "chat",
        **kwargs,
    ) -> str:
        """llm output generater"""
        model = self.model(model, config.XACT_LLM_MODEL)
    
        messages = messages or [
                    {
                        "role": "system",
                        "content": "you are ox-ai helpful ai assistant you are excelent at resonaing and assisting in any tasks",
                    },
                    {
                        "role": "user",
                        "content": prompt.strip(),
                    },
                ]
        
  

        if response_format :
            generate_format = "struct" 
        # else:
        #     del kwargs["response_format"]
    
                
        # del kwargs["generate_format"]

        if generate_format == "chat":

            chat_completion = self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                **kwargs,
            )
            res = chat_completion.choices[0].message.content
            

        elif generate_format == "gen":
            completion = self.client.completions.create(
                prompt=prompt,
                model=model,
                temperature=temperature,
                **kwargs,
            )

        elif generate_format == "struct":

            completion = self.client.beta.chat.completions.parse(
                messages=messages,
                model=model,
                temperature=temperature,
                response_format=response_format,
                **kwargs,       
            )

            res = completion.choices[0].message.parsed

        log.info("llm out generated")

        return res
