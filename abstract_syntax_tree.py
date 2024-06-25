from typing import Any


class AbstractSyntaxTree:
    def __init__(self):
        self.instructions = []

    def add(self, item: Any) -> None:
        self.instructions.append(item)

    def __len__(self):
        return len(self.instructions)

    def __getitem__(self, item):
        return self.instructions[item]

    def __repr__(self):
        return "\n".join([str(i) for i in self.instructions])