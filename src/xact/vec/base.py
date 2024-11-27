from typing import Optional, Dict, List, Tuple

from pydantic import BaseModel, ConfigDict


class BaseEmbedder(BaseModel):
    """Base class for managing embedders"""

    dimensions: Optional[int] = 1536

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def generate(self, text: str) -> List[float]:
        raise NotImplementedError
