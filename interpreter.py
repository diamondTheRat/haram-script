from token_types import *
from abstract_syntax_tree import AbstractSyntaxTree
from typing import Any
from nodes import Node
from parser import parse
from lexer import lex


operations = {
    ADD: lambda x, y: x + y,
    SUBTRACT: lambda x, y: x - y,
    MULTIPLY: lambda x, y: x * y,
    DIVIDE: lambda x, y: x / y,
    INT_DIVISION: lambda x, y: x // y,
    MODULO: lambda x, y: x % y,
    LEFT_SHIFT: lambda x, y: x << y,
    RIGHT_SHIFT: lambda x, y: x >> y,
    BIT_OR: lambda x, y: x | y,
    BIT_AND: lambda x, y: x & y,
    BIT_XOR: lambda x, y: x ^ y,
    BIGGER: lambda x, y: x > y,
    SMALLER: lambda x, y: x < y,
    BIGGER_EQUALS: lambda x, y: x >= y,
    SMALLER_EQUALS: lambda x, y: x <= y,
    EQUALS: lambda x, y: x == y,
    INDEX: lambda x, y: x[y]
}

unary_operations = {
    NEGATIVE: lambda x: -x,
    NOT: lambda x: not x
}

expressions = [
    AND, OR, NOT, BIT_AND, BIT_OR, BIT_XOR,
    BIGGER, SMALLER, SMALLER_EQUALS, BIGGER_EQUALS, EQUALS,
    ADD, SUBTRACT,
    MULTIPLY, LEFT_SHIFT, RIGHT_SHIFT, DIVIDE, MODULO, INT_DIVISION,
    CALL, INDEX, GET_ATTRIBUTE,
    NEGATIVE, LIST, DICT, INT, FLOAT, STRING, VARIABLE, CODE_GROUP, SWAP, IF
]

simple_types = [
    INT, STRING, FLOAT, BOOL
]

compound_types = [
    LIST, DICT
]

builtin_functions = {
    i: v for i, v in globals()["__builtins__"].items() if callable(v)
}

class Module:
    def __init__(self, variables: dict):
        for i, v in variables.items():
            self.__setattr__(i, v)

class Interpreter:
    def __init__(self, ast: AbstractSyntaxTree):
        self.ast: AbstractSyntaxTree = ast

    def interpret(self, ast: AbstractSyntaxTree | None = None, variables: dict[str: Any] = None):
        ast: AbstractSyntaxTree = ast or self.ast
        i = -1
        variables = variables or {"0": None, "1": None, **builtin_functions}
        while i < len(ast) - 1:
            i += 1
            instruction: Node = ast[i]
            if instruction.type in expressions:
                (self.eval(instruction, variables, execute_code=True))
            elif instruction.type is GOTO:
                name = instruction.first.value
                while instruction.type is not ANCHOR or instruction.first.value != name:
                    i -= 1
                    if i == -1:
                        raise SyntaxError(f"idk what error this should be but you're missing the '{name}' anchor or it's outside this code group")
                    instruction: Node = ast[i]
            elif instruction.type is CREATE:
                for var in instruction.first:
                    variables[var.value] = None
            elif instruction.type is ASSIGN:
                var = variables["0"]
                if not isinstance(var, str):
                    indexes = []
                    while var.type in [INDEX, GET_ATTRIBUTE]:
                        if var.type is INDEX:
                            indexes.append(Node(INDEX, self.eval(var.second, variables)))
                        else:
                            indexes.append(Node(GET_ATTRIBUTE, var.second.value))
                        var = var.first

                    if var.type is not VARIABLE:
                        raise ValueError("idk what you grabbed but its definitely not an indexed element, an attribute or a variable")

                    var = variables[var.value]
                    for i in indexes[-1:1:-1]:
                        if i.type is INDEX:
                            var = var[i.first]
                        else:
                            var = getattr(var, i.first)
                    if indexes[0].type is GET_ATTRIBUTE:
                        setattr(var, indexes[0].first, instruction.first.value)
                    else:
                        var[indexes[0].first] = self.eval(instruction.first, variables)
                else:
                    variables[var] = self.eval(instruction.first, variables)
            elif instruction.type is SELECT:
                variables["1"] = variables["0"]
                if instruction.first.type in [INDEX, GET_ATTRIBUTE]:
                    variables["0"] = instruction.first
                else:
                    variables["0"] = instruction.first.value
            elif instruction.type is DEFINE_FUNCTION:
                name = instruction.name
                code = instruction.second
                args = instruction.first
                variables[name] = Node(FUNCTION, args, code, name)
                variables[name].variables = variables.copy()
            elif instruction.type is RETURN:
                return self.eval(instruction.first, variables)
            elif instruction.type is IMPORT:
                for file in instruction.first:
                    module_variables = {'0': None, '1': None, **builtin_functions}
                    with open(f"{file.value}.haram") as f:
                        tokens = lex(f)

                    temp_ast = parse(tokens)
                    self.interpret(temp_ast, module_variables)
                    variables[file.value] = Module(module_variables)

        return True

    def get_current_variable(self, variables: dict):
        var = variables["0"]
        if not isinstance(var, str):
            indexes = []
            while var.type in [INDEX, GET_ATTRIBUTE]:
                if var.type is INDEX:
                    indexes.append(Node(INDEX, self.eval(var.second, variables)))
                else:
                    indexes.append(Node(GET_ATTRIBUTE, var.second.value))
                var = var.first

            if var.type is not VARIABLE:
                raise ValueError(
                    "idk what you grabbed but its definitely not an indexed element, an attribute or a variable")

            var = variables[var.value]
            for i in indexes[::-1]:
                if i.type is INDEX:
                    var = var[i.first]
                else:
                    var = getattr(var, i.first)
            return var
        else:
            return variables[variables["0"]]

    def eval(self, instruction: Node | Variable, variables: dict, execute_code: bool = False, ignore_rat: bool = False) -> Any:
        if instruction.type in simple_types:
            return instruction.value
        elif instruction.type in [AND, OR]:
            if instruction.type is OR:
                return self.eval(instruction.first, variables) or self.eval(instruction.second, variables)
            return self.eval(instruction.first, variables) and self.eval(instruction.second, variables)
        elif instruction.type in compound_types:
            if instruction.type is LIST:
                return [self.eval(i, variables) for i in instruction.first]
            elif instruction.type is DICT:
                return {self.eval(i, variables): self.eval(v, variables) for i, v in instruction.first.items()}
        elif instruction.type is CODE_GROUP:
            if execute_code:
                ast = AbstractSyntaxTree()
                ast.instructions = instruction.first
                return self.interpret(ast, variables)
            else:
                return instruction
        elif instruction.type in operations:
            left = self.eval(instruction.first, variables)
            right = self.eval(instruction.second, variables)
            return operations[instruction.type](left, right)
        elif instruction.type in unary_operations:
            value = self.eval(instruction.first, variables)
            return unary_operations[instruction.type](value)
        elif instruction.type is VARIABLE:
            if instruction.value == "rat":
                if type(variables[variables["0"]]) is Node:
                    return self.eval(variables[variables["0"]], variables, execute_code=variables[variables["0"]].type is CODE_GROUP)
                else:
                    return variables[variables["0"]]
            else:
                if ignore_rat:
                    variables[variables["0"]]
                else:
                    raise ValueError("Can only refer to variables as 'rat' meaning the selected variable")
                # raise NameError(f"Variable '{instruction.value}' does not exist")
            # return variables[instruction.value]
        elif instruction.type is SWAP:
            variables["0"], variables["1"] = variables["1"], variables["0"]
            return self.get_current_variable(variables)
        elif instruction.type is CALL:
            func = self.eval(instruction.first, variables)
            args = [self.eval(i, variables) for i in instruction.second["args"]]
            kwargs = {i.value: self.eval(v, variables) for i, v in instruction.second["kwargs"].items()}
            if callable(func):
                return func(*args, **kwargs)
            elif func.type is FUNCTION:
                function_args = func.first
                code = func.second
                f_variables = func.variables
                args_index = 0
                for arg in function_args:
                    if isinstance(arg, list):
                        variables[arg[0]] = self.eval(arg[1], variables)

                for i, v in enumerate(args):
                    f_variables[function_args[i] if not isinstance(function_args[i], list) else function_args[i][0]] = v
                for i, v in kwargs.items():
                    f_variables[i] = v

                ast = AbstractSyntaxTree()
                if code.type is CODE_GROUP:
                    ast.instructions = code.first
                else:
                    ast.instructions = [code]

                return self.interpret(ast, f_variables)
            else:
                raise TypeError(f"Can't call variable of type {TYPES[func.type]}")
        elif instruction.type is GET_ATTRIBUTE:
            obj = self.eval(instruction.first, variables)
            if isinstance(obj, Node):
                return obj.first[instruction.second.value]
            else:
                attribute = instruction.second.value
                return getattr(obj, attribute)
        elif instruction.type is IF:
            condition = self.eval(instruction.first, variables)
            if condition:
                self.eval(instruction.second, variables, execute_code=True)
                return True
            return False
        elif instruction.type in [MODULE, FUNCTION]:
            return instruction


def interpret(ast: AbstractSyntaxTree) -> None:
    interpreter = Interpreter(ast)

    interpreter.interpret()
