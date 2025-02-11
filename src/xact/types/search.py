


from typing import Any, List, Optional, Union
from pydantic import BaseModel


class SearchMDResponse(BaseModel):
    idx:List[int]=[]
    score:List[Union[int,float]]=[]
    data:List[Union[str,Any]]=[]
    data_embed:Optional[List[List[int]]]=[]