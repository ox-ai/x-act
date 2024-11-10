from typing import Optional, Dict, List, Tuple, Any
from typing_extensions import Literal

from xact.vec.base import Embedder
from xact.settings import config
from xact.llm.openai_client import OpenAI,llm_client
from xact.utils.log import logger


class Embedder(Embedder):
    model: str = "text-embedding-ada-002"
    dimensions: int = 1536
    encoding_format: Literal["float", "base64"] = "float"

    def __init__(
        self,
        llm_client: Optional[OpenAI] = llm_client,
        model: str = None,
        encoding_format: Literal["float", "base64"] = "float",
    ):
        self.llm_client = llm_client 
        self.model = model or config.XACT_LLM_EMBEDDING_MODEL
        self.encoding_format = encoding_format 

    def get_embedding(
        self,
        text: str,
        model: str = None,
        encoding_format: Literal["float", "base64"] = "float",
    ) -> List[float]:
        text = text.replace("\n", " ")
        self.model = model or self.model
        self.encoding_format = encoding_format 

        try:
            response = self.llm_client.embeddings.create(input=[text], model=self.model)
            return response.data[0].embedding
        except Exception as e:
            logger.warning(e)
            return []


