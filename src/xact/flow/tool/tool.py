
import inspect
from xact.log.config import log_manager

log = log_manager.init(__name__)

__all__=[
    "gen_function_schema","Tool","tool"
]




class Tool:
    def __init__(
        self,
        func: callable = None,
        description: str = None,
        param_description: dict = None,
    ):
        self.func = func
        self.description = description
        self.param_description = param_description
        self.fun_schema = gen_function_schema(func=func)
        self.name = self.fun_schema["function"]["name"]

    def run(self, *args, **kwargs):
        name = self.fun_schema["function"]["name"]
        log.info(f"executing tool : {name}")
        return self.func(*args, **kwargs)

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)

    def get_schema(self, is_param_description: bool = True):
        fun_schema = self.fun_schema
        if is_param_description:
            if self.param_description:
                for k, v in fun_schema["function"]["parameters"]["properties"].items():
                    if k in self.param_description:
                        fun_schema["function"]["parameters"]["properties"][k][
                            "description"
                        ] = self.param_description[k]

        if self.description:
            fun_schema["function"]["description"] = (
                fun_schema["function"]["description"] + " \n " + self.description
            )

        return fun_schema


def tool(
    description: str = None, param_description: dict = None,func:callable=None 
)-> Tool:
    if func:
        if isinstance(func,Tool):
            return func
        
        _tool = Tool(func=func, description=description, param_description=param_description)
        return _tool
        
    def decorator(func):

        _tool = Tool(func=func, description=description, param_description=param_description)
        return _tool



    return decorator


def gen_function_schema(func) -> dict:
    """
    Converts a Python function into a JSON-serializable dictionary
    that describes the function's signature, including its name,
    description, and parameters.

    Args:
        func: The function to be converted.

    Returns:
        A dictionary representing the function's signature in JSON format.
    """
    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean",
        list: "array",
        dict: "object",
        type(None): "null",
    }

    try:
        signature = inspect.signature(func)
    except ValueError as e:
        raise ValueError(
            f"Failed to get signature for function {func.__name__}: {str(e)}"
        )

    parameters = {}
    for param in signature.parameters.values():
        try:
            param_type = type_map.get(param.annotation, "string")
        except KeyError as e:
            raise KeyError(
                f"Unknown type annotation {param.annotation} for parameter {param.name}: {str(e)}"
            )
        parameters[param.name] = {"type": param_type}

    required = [
        param.name
        for param in signature.parameters.values()
        if param.default == inspect._empty
    ]

    fun_schema = {
        "type": "function",
        "function": {
            "name": func.__name__,
            "description": func.__doc__ or "",
            "parameters": {
                "type": "object",
                "properties": parameters,
                "required": required,
            },
        },
    }

    fun_schema["function"]["description"] = fun_schema["function"]["description"].strip()

    return fun_schema