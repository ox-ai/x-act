from typing import List, Union, Dict, Any
from pydantic import BaseModel, Field


code_types = [
    "code",
    "code-input",
    "code-input-intracted",
    "code-qui-head",
    "code-gui-headless",
]


# code_schema_template = {
#     "code_type":  "code"
#         | "code-input"
#         | "code-input-intracted"
#         | "code-qui-head"
#         | "code-gui-headless"
#     ,
#     "code": "path",
#     "input_required": True | False,
#     "input_map": {
#         "arg1": any,
#         "arg2": any,
#     }
#     | ["arg1", "arg2"],
#     "output_format": "text" | "json" | "any",
#     "description": "Brief description of the code's functionality keywords",
#     "metadata": {"keywords": ["code", "code run"]},
# }


class CodeSchema(BaseModel):
    code_type: str = Field(
        ...,
        description="code types",
        example="code",
        pattern=f"^({'|'.join(code_types)})$",
    )

    code: str = Field(..., description="code name")
    code_path: str = Field(..., description="Path to the code")
    input_required: bool = Field(..., description="Indicates if input is required")

    input_map: Union[Dict[str, Any], List[str]] = Field(
        ..., description="Mapping of inputs or a list of argument names"
    )

    output_format: str = Field(
        ...,
        description="Output format type",
        example="text",
        pattern="^(text|json|any)$",
    )

    description: str = Field(
        ..., description="Brief description of the code's functionality"
    )

    metadata: Dict[str, List[str]] = Field(
        ...,
        description="Metadata of the code",
        example={"keywords": ["code", "code run"]},
    )
    keywords: List[str] = Field(
        ...,
        description="keywords related to the code",
        example={"keywords": ["code", "code run"]},
    )

    class Config:
        json_schema_extra = {
            "example": {
                "code_type": "code",
                "code": "code_name",
                "code_path": "path/to/code",
                "input_required": True,
                "input_map": {
                    "arg1": "some_value",
                    "arg2": "another_value",
                },
                "output_format": "text",
                "description": "This is a sample code functionality",
                "metadata": {},
                "keywords": ["code", "code run"],
            }
        }


def test():
    # Example usage:
    schema = CodeSchema(
        code_type="code-input",
        code="code_name",
        code_path="path/to/code",
        input_required=True,
        input_map={"arg1": "value1", "arg2": "value2"},
        output_format="json",
        description="Runs a code block",
        metadata={},
        keywords=["run", "code"],
    )
    print(schema.model_dump_json(indent=4))
