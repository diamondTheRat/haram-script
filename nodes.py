from typing import Any
from token_types import *



class Node:
    def __init__(self, type: int, first: Any = None, second: Any = None, name: str = None):
        self.type = type
        self.name = name
        self.first = first
        self.second = second

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.first == other.first
        return False

    def __hash__(self):
        return hash(str(self))

    def __repr__(self):
        if self.type is CODE_GROUP:
            return "{\n\t" + "\n\t".join(["\n\t".join(str(i).split("\n")).rstrip(';') + ";" for i in self.first]) + "\n}"
        if self.type is DEFINE_FUNCTION:
            return f"function '{self.name}'" "(" + ', '.join([str(i) for i in self.first]) + ")" " {" + "\n".join(str(self.second).split("\n")) + "}"
        if self.second is None:
            return "{}({})".format(TYPES[self.type], self.first or "")
        return "{}({}, {})".format(TYPES[self.type], self.first or "", self.second)