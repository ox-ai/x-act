from typing import Optional, List
from pydantic import BaseModel, Field
from typing_extensions import Literal

from xact.vec.base import BaseEmbedder
from xact.settings import config
from xact.llm.openai_client import OpenAI, llm_client
from xact.utils.log import logger


class Embedder(BaseEmbedder):
    model: str = config.XACT_LLM_EMBEDDING_MODEL
    dimensions: int = 1536
    encoding_format: Literal["float", "base64"] = "float"
    llm_client: OpenAI = Field(default_factory=lambda: llm_client)

    def __init__(
        self,
        llm_client: Optional[OpenAI] = None,
        model: str = None,
        encoding_format: Literal["float", "base64"] = "float",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.llm_client = llm_client or self.llm_client
        self.model = model or self.model
        self.encoding_format = encoding_format

    def generate(
        self,
        prompt: str | List[str] ,
        model: str = None,
        encoding_format: Literal["float", "base64"] = "float",
    ) -> List[List[float]] :
        prompts = []
        if  isinstance(prompt,str):
            prompts.append(prompt)
        elif isinstance(prompt,list):
            prompts = prompt

        for i,pmt in enumerate(prompts):
            prompts[i] = pmt.replace("\n", " ")
        self.model = model or self.model
        self.encoding_format = encoding_format

        try:
            response = self.llm_client.embeddings.create(input=prompts, model=self.model)
            return response.data
        except Exception as e:
            logger.warning(e)
            return [[]]
