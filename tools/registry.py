import inspect
from models.tool import Tool

TOOLS = {}


def register(func):
    TOOLS[func.__name__] = Tool(
        name=func.__name__,
        function=func,
        description=inspect.getdoc(func) or "",
        signature=inspect.signature(func),
    )
    return func


def execute(name: str, **kwargs):
    """
    Execute a registered tool by name.
    """
    if name not in TOOLS:
        raise ValueError(f"Unknown tool '{name}'")

    tool = TOOLS[name]

    return tool.function(**kwargs)

def get_tools():
    return TOOLS

def get_llm_tools():
    """
    Return tool definitions suitable for an LLM.
    """

    definitions = []

    for name, tool in TOOLS.items():
        sig = tool.signature

        properties = {}
        required = []

        for param_name, param in sig.parameters.items():

            annotation = param.annotation

            if annotation is int:
                json_type = "integer"
            elif annotation is float:
                json_type = "number"
            elif annotation is bool:
                json_type = "boolean"
            else:
                json_type = "string"

            properties[param_name] = {
                "type": json_type
            }

            if param.default is inspect.Parameter.empty:
                required.append(param_name)

        definitions.append({
            "type": "function",
            "function": {
                "name": name,
                "description": tool.description,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required,
                },
            },
        })

    return definitions