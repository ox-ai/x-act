from typing import Optional, List, Dict, Any, Union
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, field_validator, model_validator

from xact.utils.gen import gen_datetime, gen_uuid





class DataX(BaseModel):
    uid: UUID = Field(default_factory=gen_uuid)
    cid: Optional[str] = None
    flow_mode: str = "prompt"
    role: str = "xact"
    content: Union[str, Any]
    content_type: Union[str, Any] = None
    md_content: Optional[Union[str, Any]] = None



    metadata: Optional[Any] = None
    tags: Optional[List[str]] = None
    description: Optional[str] = None  
    source: Optional[Dict[str, Any]] = None
    
    embed: Optional[List[float]] = None
    embed_id: Optional[str] = None

    created_at: datetime = Field(
        default_factory=gen_datetime,
    )  # Automatically set on creation
    time_triggers: Optional[List[datetime]] = None

    @model_validator(mode="after")
    def set_content_type(self):
        self.content_type = type(self.content).__name__
        return self

    @field_validator("embed")
    def check_embedding(cls, v):
        if v is not None:
            if not all(isinstance(x, (int, float)) for x in v):
                raise ValueError("Embedding must be a list of numbers (int or float)")
        return v

    @field_validator("time_triggers")
    def check_time_triggers(cls, v):
        if v is not None:
            if not all(isinstance(x, datetime) for x in v):
                raise ValueError("time_triggers must be a list of datetime objects")
        return v

    def to_dict(self) -> Dict[str, Any]:
        """Returns a dictionary representation of the document"""

        return self.model_dump(exclude_none=True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DataX":
        """Returns a DataX object from a dictionary representation."""
        return cls.model_validate(data)  # Fixed here

    @classmethod
    def from_json(cls, data: str) -> "DataX":
        """Returns a DataX object from a JSON string representation."""
        return cls.model_validate_json(data)
