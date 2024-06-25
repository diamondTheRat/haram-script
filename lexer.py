from typing import TextIO
from token_types import *
from tokens import Tokens
from _io import TextIOWrapper



special_characters = {
    "+": Addition,
    "-": Subtraction,
    "/": Division,
    "*": Multiplication,
    "{": CodeGroupBegin,
    "}": CodeGroupEnd,
    "!": Not,
    "^": BitXOR,
    "|": BitOr,
    "&": BitAnd,
    ">": Bigger,
    "<": Smaller,
    "(": BracketOpen,
    ")": BracketClose,
    "[": ListBegin,
    "]": ListEnd,
    ",": Delimiter,
    ":": PairDelimiter,
    ";": Separator,
    "=": Assign,
    ".": GetAttribute,
    "?": If,
    "%": Modulo
}

keywords = {
    "and": And,
    "or": Or,
    "output": Return,
    "define": DefineFunction,
    "adopt": Create,
    "give": Assign,
    "grab": Select,
    "eat": GoTo,
    "place": Anchor,
    "swap": Swap,
    "true": lambda: Bool(1),
    "false": lambda: Bool(0),
    "import": Import
}

character_groups = {
    "==": Equals,
    "!=": NotEquals,
    ">=": BiggerEquals,
    "<=": SmallerEquals,
    "<<": LeftShift,
    ">>": RightShift,
    "//": IntDivision
}

# deprecated
"""
keywords = {
    **keywords,
    **(types := {
        "int": IntType,
        "string": StringType
    })
}
"""

variable_characters = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPAFGHJKLZXCVBNM_1234567890'

digits = "0123456789"
float_dot = "."

string_identifier = '"'
character_identifier = "'"


def lex(code: TextIO | str) -> Tokens:
    if type(code) is TextIOWrapper:
        code = code.read()

    code = code.split("\n")
    code = [i.split("#")[0] for i in code]
    code = "\n".join(code)

    tokens = Tokens()

    i = -1
    while i + 1 < len(code):
        i += 1
        character = code[i]

        if character in special_characters:
            for group in character_groups.keys():
                if group[0] == character:
                    if len(code) > i + 1 and code[i + 1] == group[1]:
                        tokens.add(character_groups[group]())
                        i += 1
                        break
            else:
                tokens.add(special_characters[character]())

        elif character in digits + float_dot:
            is_float = False
            if character == float_dot:
                is_float = True

            number = character
            while i + 1 < len(code) and code[i + 1] in digits + float_dot:
                i += 1
                character = code[i]

                if character == float_dot:
                    number += "."
                else:
                    number += character

                if is_float and character == float_dot:
                    raise ValueError("nagger whhy float with 2 dots")
                elif not is_float and character == float_dot:
                    is_float = True

            if is_float:
                tokens.add(Float(float(number)))
            else:
                tokens.add(Int(int(number)))

        elif character in variable_characters:
            variable = character
            while i + 1 < len(code) and code[i + 1] in variable_characters:
                i += 1
                character = code[i]

                variable += character

            if variable in keywords:
                tokens.add(keywords[variable]())
            else:
                tokens.add(Variable(VARIABLE, variable))

        elif character == string_identifier:
            string = ''
            while i + 1 < len(code) and code[i + 1] != string_identifier:
                i += 1
                character = code[i]
                string += character

            i += 1

            tokens.add(String(string))

        elif character == character_identifier:
            if i + 2 >= len(code):
                raise TypeError("u didnt close the character thing")

            if code[i + 2] != character_identifier:
                raise TypeError("u didnt close the character thing or made it longer than 1 character")

            tokens.add(Character(code[i + 1]))
            i += 2


    return tokens
