from token_types import *
from abstract_syntax_tree import AbstractSyntaxTree
from tokens import Tokens
from nodes import Node


class Parser():
    def __init__(self, tokens: Tokens):
        self.tokens = tokens
        self.tree = AbstractSyntaxTree()

        self.index = -1
        self.token = None

    def next(self):
        self.index += 1
        self.token = self.tokens[self.index]

    def back(self):
        self.index -= 1
        self.token = self.tokens[self.index]

    def parse(self):
        while self.index < len(self.tokens) - 1:
            self.next()
            instruction = self.instruction()
            if instruction is not None:
                self.tree.add(instruction)

    def instruction(self):
        if self.token.type is SEPARATOR:
            return None
        if self.token.type is DEFINE_FUNCTION:
            return self.get_function()
        # elif self.token.type is CODE_GROUP_BEGIN:
        #     code = []
        #     while self.token.type is not CODE_GROUP_END:
        #         self.next()
        #         print(self.token)
        #         instruction = self.instruction()
        #         if instruction is not None:
        #             code.append(instruction)
        #     self.next()
        #     return Node(CODE_GROUP, code)
        elif self.token.type is CREATE:
            self.next()
            if self.token.type is not VARIABLE or self.token.value not in ["rat", "rats"]:
                raise TypeError("Missing keyword 'rat' or 'rats' after 'adopt'")
            rat_or_rats = self.token.value
            self.next()
            if self.token.type is not VARIABLE or self.token.value != "named":
                raise TypeError(f"Missing keyword 'named' after '{rat_or_rats}' during adoption")
            self.next()
            rats = self.sequence(stop=SEPARATOR)
            if any(i.type is not VARIABLE for i in rats):
                raise TypeError("Rat names are wrong, they will get bullied")
            return Node(CREATE, rats)
        elif self.token.type is SELECT:
            self.next()
            var = self.expression()
            if var.type not in [VARIABLE, INDEX, GET_ATTRIBUTE]:
                raise TypeError("Can only grab rats by their name, index or an attribute")
            self.next()
            return Node(SELECT, var)
        elif self.token.type is ASSIGN:
            self.next()
            exp = self.expression()
            self.next()
            return Node(ASSIGN, exp)
        elif self.token.type is ANCHOR:
            self.next()
            if self.token.type is not VARIABLE or self.token.value != "cheese":
                raise TypeError(f"Missing keyword 'cheese' after 'place'")
            self.next()
            if self.token.type is not VARIABLE:
                raise TypeError("Cheese name must use variable name format")
            name = self.token
            self.next()
            return Node(ANCHOR, name)
        elif self.token.type is GOTO:
            self.next()
            if self.token.type is not VARIABLE:
                raise TypeError("Cheese name must use variable name format")
            name = self.token
            self.next()
            return Node(GOTO, name)
        elif self.token.type is RETURN:
            self.next()
            exp = self.expression()
            self.next()
            return Node(RETURN, exp)
        elif self.token.type is IMPORT:
            self.next()
            files = self.sequence(stop = SEPARATOR)
            if any(i.type not in [VARIABLE, GET_ATTRIBUTE] for i in files):
                raise TypeError("Module names should be names or name.other_name or smth idk how to explain it its just python importing but a little more limited")

            return Node(IMPORT, files)

        else:
            expression = self.expression()
            self.next()
            return expression
        # if self.token.type is not SEPARATOR:
        #     raise TypeError("Missing ; at the end of the line")

    def get_function(self):
        self.next()
        name = self.token.value
        self.next()
        if self.token.type is not BRACKET_OPEN:
            raise TypeError("() after function name")
        self.next()
        args = []
        while self.token.type is not BRACKET_CLOSE:
            if self.token.type is not VARIABLE:
                raise TypeError("Please only put variable names in function arguments")
            args.append(self.token.value)
            self.next()
            if self.token.type is ASSIGN:
                self.next()
                value = self.expression() # self.expression()
                self.next()
                if value is None:
                    raise TypeError("Invalid default parameter")
                args[-1] = [args[-1], value]
            elif len(args) >= 2 and type(args[-2]) is list:
                raise TypeError("Can't have non-default parameter for an argument after arguments using default parameters")


            if self.token.type not in [BRACKET_CLOSE, DELIMITER]:
                raise TypeError("Expected comma or ')' after function argument")
            if self.token.type is DELIMITER:
                self.next()

        self.next()
        if self.token.type != VARIABLE or self.token.value != "as":
            raise TypeError("Expected keyword 'as' after function definition")
        self.next()
        code = self.instruction()
        return Node(DEFINE_FUNCTION, args, code, name)

    def sequence(self, stop: int = BRACKET_CLOSE):
        content = []
        while self.token.type is not stop:
            content.append(self.expression())
            self.next()
            if self.token.type is DELIMITER:
                self.next()
        return content

    def expression(self) -> Node:
        left = self.logic_expression()
        self.next()
        while self.token.type is IF:
            exp_type = self.token.type
            self.next()
            left = Node(exp_type, left, self.instruction())
            self.next()
        self.back()

        return left

    def logic_expression(self) -> Node:
        left = self.comparison_expression()
        self.next()
        while self.token.type in [AND, OR]:
            exp_type = self.token.type
            self.next()
            left = Node(exp_type, left, self.comparison_expression())
            self.next()
        self.back()

        return left

    def comparison_expression(self) -> Node:
        left = self.arithmetic_expression()
        self.next()
        while self.token.type in [BIGGER, SMALLER, SMALLER_EQUALS, BIGGER_EQUALS, EQUALS]:
            exp_type = self.token.type
            self.next()
            left = Node(exp_type, left, self.arithmetic_expression())
            self.next()
        self.back()

        return left

    def arithmetic_expression(self) -> Node:
        left = self.term()
        self.next()
        while self.token.type in [ADD, SUBTRACT]:
            exp_type = self.token.type
            self.next()
            left = Node(exp_type, left, self.term())
            self.next()
        self.back()

        return left

    def term(self) -> Node:
        left = self.postfix()
        self.next()
        while self.token.type in [MULTIPLY, BIT_OR, BIT_AND, BIT_XOR, LEFT_SHIFT, RIGHT_SHIFT, DIVIDE, MODULO, INT_DIVISION]:
            exp_type = self.token.type
            self.next()
            left = Node(exp_type, left, self.postfix())
            self.next()
        self.back()
        return left

    def postfix(self) -> Node:
        left = self.atom()
        self.next()
        while self.token.type in [BRACKET_OPEN, LIST_BEGIN, GET_ATTRIBUTE]:
            rat = self.token.type
            self.next()
            if rat is BRACKET_OPEN:
                args = []
                kwargs = dict()
                got_kwargs = False
                while self.token.type is not BRACKET_CLOSE:
                    args.append(self.expression())
                    self.next()
                    if self.token.type is ASSIGN:
                        got_kwargs = True
                        if args[-1].type is not VARIABLE:
                            raise SyntaxError("Keyword arguments can only be variable names")
                        self.next()
                        kwargs[args.pop(-1)] = self.expression()
                        self.next()
                    elif got_kwargs:
                        raise SyntaxError("Can't have normal arguments after keyword arguments")
                    if self.token.type is DELIMITER:
                        self.next()

                sequence = self.sequence(stop = BRACKET_CLOSE)
                left = Node(CALL, left,
                            {
                                "args": args,
                                "kwargs": kwargs
                            }
                            )
            elif rat is GET_ATTRIBUTE:
                var = self.token
                if var.type is not VARIABLE:
                    raise TypeError("Get attribute must use a variable name not wtv the fuck u gave it")
                left = Node(GET_ATTRIBUTE, left, var)
            else:
                left = Node(INDEX, left, self.expression())
                self.next()

            self.next()
        self.back()
        return left

    def atom(self):
        if self.token.type is SUBTRACT:
            self.next()
            return Node(NEGATIVE, self.atom())
        elif self.token.type is VARIABLE:
            left = self.token
            self.next()
            while self.token.type in [INCREASE, DECREASE]:
                left = Node(self.token.type, left)
                self.next()
            self.back()
            return left
        elif self.token.type in [INT, STRING, FLOAT, BOOL]:
            return self.token
        elif self.token.type is NOT:
            self.next()
            return Node(NOT, self.atom())
        elif self.token.type is BRACKET_OPEN:
            self.next()
            expression = self.expression()
            self.next()
            return expression
        elif self.token.type is LIST_BEGIN:
            self.next()
            sequence = self.sequence(stop=LIST_END)
            return Node(LIST, sequence)
        elif self.token.type is CODE_GROUP_BEGIN:
            index = self.index
            self.next()
            self.instruction()
            self.index = index
            if self.token.type is SEPARATOR:
                self.token = self.tokens[self.index]
                self.next()
                code = []
                while self.token.type is not CODE_GROUP_END:
                    instruction = self.instruction()
                    if instruction is not None:
                        code.append(instruction)
                    self.next()

                return Node(CODE_GROUP, code)
            else:
                if self.token.type is not PAIR_DELIMITER:
                    raise SyntaxError("No idea what you tried doing but you probably forgot a ;")
                content = {}
                while self.token.type is not CODE_GROUP_END:
                    self.next()
                    key = self.expression()
                    self.next()
                    if self.token.type is not PAIR_DELIMITER:
                        raise SyntaxError("Missing ':' after a dictionary key")
                    self.next()
                    value = self.expression()
                    self.next()
                    content[key] = value
                return Node(DICT, content)
        elif self.token.type is SWAP:
            return self.token

def parse(tokens: Tokens) -> AbstractSyntaxTree:
    parser = Parser(tokens)

    parser.parse()

    return parser.tree
