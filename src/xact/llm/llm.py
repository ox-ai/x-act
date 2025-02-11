from typing import Any, Literal, Union

from pydantic import BaseModel
from xact.config.config import ConfigVar
from xact.llm.openai_client import OpenAI
from xact.llm.openai_client import llm_client as base_llm_client
from xact.config.gen import config
from xact.log.config import log_manager

log = log_manager.init(__name__)


class LLMGenerated(BaseModel):
    data: Union[str,Any]
    completion: Any
    gen_format: str


class LLM:
    def __init__(self, llm_client: OpenAI = base_llm_client, model: str = None):

        self.client = llm_client
        self.model = ConfigVar(model, config.XACT_LLM_MODEL)

    def get_model(self):
        return self.model()

    def list(
        self,
    ):

        models = []
        for data in self.client.models.list():
            models.append(data.id)

        return models

    def generate(
        self,
        prompt: str = None,
        model: str = None,
        messages: list = None,
        temperature: int = 0,
        tools: list = [],
        response_format: Any = None,
        gen_format: Literal[
            "chat",
            "gen",
            "struct",
        ] = "chat",
        **kwargs,
    ) -> LLMGenerated:
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

        if response_format:
            gen_format = "struct"

        completion = None

        if gen_format == "chat":

            completion = self.client.chat.completions.create(
                messages=messages,
                model=model,
                temperature=temperature,
                tools=tools,
                **kwargs,
            )
            res = completion.choices[0].message.content

        elif gen_format == "gen":
            completion = self.client.completions.create(
                prompt=prompt,
                model=model,
                temperature=temperature,
                **kwargs,
            )
            res = completion.choices[0].text

        elif gen_format == "struct":

            completion = self.client.beta.chat.completions.parse(
                messages=messages,
                model=model,
                temperature=temperature,
                tools=tools,
                response_format=response_format,
                **kwargs,
            )

            res = completion.choices[0].message.parsed

        log.info("llm out generated")

        return LLMGenerated(
            data=res,
            completion=completion,
            gen_format=gen_format,
        )
