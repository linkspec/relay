from dataclasses import dataclass
from inspect import Signature
from typing import Callable


@dataclass
class Tool:
    name: str
    function: Callable
    description: str
    signature: Signature