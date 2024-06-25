from token_types import *
from settings import Settings


class Tokens:
    def __init__(self, tokens: list | tuple = None):
        self.tokens = tokens or []
        self.index = -1

    def append(self, token):
        self.tokens.append(token)

    def add(self, token):
        self.tokens.append(token)

    def __len__(self):
        return len(self.tokens)

    def __next__(self):
        self.index += 1
        if self.index >= len(self.tokens):
            self.index = min(len(self.tokens), self.index)
            return EOF()

        return self.tokens[self.index]

    def __getitem__(self, item):
        if item >= len(self.tokens):
            return EOF()
        return self.tokens[item]

    def back(self):
        self.index -= 1
        if Settings.warnings and self.index < 0:
            print("WARNING TRYING TO ACCESS NEGATIVE TOKEN INDEX")

        return self.tokens[self.index]

    def __iter__(self):
        return Tokens(self.tokens)

    def __repr__(self):
        representation = ""
        indent = ""
        indented = False
        for index, token in enumerate(self.tokens):
            if token.type == SEPARATOR:
                representation += str("\n")
                indented = True
            elif token.type == CODE_GROUP_BEGIN:
                representation += str("\n")
                indent += "\t"
                indented = True
            elif token.type == CODE_GROUP_END:
                representation += str("\n")
                indent = indent[:-1]
                indented = True
            else:
                if indented:
                    representation += indent
                indented = False
                representation += str(token)
                if index < len(self.tokens) - 1 and self.tokens[index + 1].type not in [SEPARATOR, CODE_GROUP_BEGIN, CODE_GROUP_END]:
                    representation += " | "
        return representation
