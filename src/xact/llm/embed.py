from typing import Optional, List
from pydantic import BaseModel, Field
from typing_extensions import Literal
from openai.types.create_embedding_response import CreateEmbeddingResponse

from xact.config.config import ConfigVar
from xact.config.gen import config
from xact.llm.openai_client import OpenAI, llm_client
from xact.log.config import log_manager

log = log_manager.init(__name__)


class Embedder:
    dimensions: int = 1536
    encoding_format: Literal["float", "base64"] = "float"
    def __init__(
        self,
        llm_client: Optional[OpenAI] = llm_client,
        model: str = config.XACT_LLM_EMBEDDING_MODEL,
        encoding_format: Literal["float", "base64"] = "float",
        **kwargs
    ):
        super().__init__(**kwargs)
        self.llm_client = llm_client or self.llm_client
        self.model = ConfigVar(model,config.XACT_LLM_EMBEDDING_MODEL)
        
        self.encoding_format = encoding_format

    def generate(
        self,
        prompt: str | List[str] ,
        model: str = None,
        encoding_format: Literal["float", "base64"] = "float",
    ) -> CreateEmbeddingResponse :
        prompts = []
        if  isinstance(prompt,str):
            prompts.append(prompt)
        elif isinstance(prompt,list):
            prompts = prompt

        for i,pmt in enumerate(prompts):
            prompts[i] = pmt.replace("\n", " ")
        model = self.model(model,config.XACT_LLM_EMBEDDING_MODEL)
        encoding_format=encoding_format or self.encoding_format 

        try:
            response = self.llm_client.embeddings.create(input=prompts, model=model,encoding_format=encoding_format)
            return response
        except Exception as e:
            log.warning(e)
            raise e
