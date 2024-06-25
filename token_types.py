def get_id():
    for i in range(1000):
        yield i

get_id = get_id()
next_id = lambda: next(get_id)

ENDL = next_id()
INT = next_id()
FLOAT = next_id()
STRING = next_id()
LIST = next_id()
ADD = next_id()
SUBTRACT = next_id()
MULTIPLY = next_id()
DIVIDE = next_id()
VARIABLE = next_id()
DICT = next_id()
LIST_BEGIN = next_id()
LIST_END = next_id()
SEPARATOR = next_id()
DICT_BEGIN = next_id()
DICT_END = next_id()
INPUT = next_id()
BRACKET_OPEN = next_id()
BRACKET_CLOSE = next_id()
NEGATIVE = next_id()
ASSIGN = next_id()
OUTPUT = next_id()
INDENT = next_id()
RANDOM = next_id()
INCREASE = next_id()
IF = next_id()
BIGGER = next_id()
SMALLER = next_id()
EQUALS = next_id()
LOOP = next_id()
BIGGER_EQUALS = next_id()
SMALLER_EQUALS = next_id()
FORLOOP = next_id()
WHILE = next_id()
INDEX = next_id()
CALL = next_id()
MODULO = next_id()
INT_DIVISION = next_id()
ELSE_IF = next_id()
ELSE = next_id()
DECREASE = next_id()
AND = next_id()
OR = next_id()
NOT = next_id()
BOOL = next_id()
CLASS = next_id()
DEFINE_END = next_id()
DEFINE = next_id()
RETURN = next_id()
FUNCTION = next_id()
NO_OUTPUT = next_id()
DOT = next_id()
SELF = next_id()
EOF = next_id()
CHARACTER = next_id()
CODE_GROUP_BEGIN = next_id()
CODE_GROUP_END = next_id()
NOT_EQUALS = next_id()
SMALLER_EQUALS = next_id()
BIGGER_EQUALS = next_id()
RIGHT_SHIFT = next_id()
LEFT_SHIFT = next_id()
BIT_OR = next_id()
BIT_XOR = next_id()
BIT_AND = next_id()
DELIMITER = next_id()
PAIR_DELIMITER = next_id()
DEFINE_FUNCTION = next_id()
GET_ATTRIBUTE = next_id()
CODE_GROUP = next_id()
CREATE = next_id()
SELECT = next_id()
EXPRESSION = next_id()
ANCHOR = next_id()
GOTO = next_id()
SWAP = next_id()
IMPORT = next_id()
MODULE = next_id()

TYPES = {v: i for i, v in globals().items() if i.isupper()}

class Operator:
    def __init__(self, type: int):
        self.type = type

    def __repr__(self):
        return f"{TYPES[self.type]}"

class Indent:
    def __init__(self, value: int):
        self.type = INDENT
        self.value = value

    def __repr__(self):
        return f"INDENT: {self.value}"

class Addition(Operator):
    def __init__(self):
        super().__init__(ADD)

class Subtraction(Operator):
    def __init__(self):
        super().__init__(SUBTRACT)

class Multiplication(Operator):
    def __init__(self):
        super().__init__(MULTIPLY)

class Division(Operator):
    def __init__(self):
        super().__init__(DIVIDE)

class Modulo(Operator):
    def __init__(self):
        super().__init__(MODULO)

class IntDivision(Operator):
    def __init__(self):
        super().__init__(INT_DIVISION)

class BitOr(Operator):
    def __init__(self):
        super().__init__(BIT_OR)

class BitAnd(Operator):
    def __init__(self):
        super().__init__(BIT_AND)

class BitXOR(Operator):
    def __init__(self):
        super().__init__(BIT_XOR)

class Equals(Operator):
    def __init__(self):
        super().__init__(EQUALS)

class Bigger(Operator):
    def __init__(self):
        super().__init__(BIGGER)

class BiggerEquals(Operator):
    def __init__(self):
        super().__init__(BIGGER_EQUALS)

class Smaller(Operator):
    def __init__(self):
        super().__init__(SMALLER)

class SmallerEquals(Operator):
    def __init__(self):
        super().__init__(SMALLER_EQUALS)

class NotEquals(Operator):
    def __init__(self):
        super().__init__(NOT_EQUALS)

class LeftShift(Operator):
    def __init__(self):
        super().__init__(LEFT_SHIFT)

class RightShift(Operator):
    def __init__(self):
        super().__init__(RIGHT_SHIFT)

class GetAttribute(Operator):
    def __init__(self):
        super().__init__(GET_ATTRIBUTE)

class BracketOpen(Operator):
    def __init__(self):
        super().__init__(BRACKET_OPEN)

class BracketClose(Operator):
    def __init__(self):
        super().__init__(BRACKET_CLOSE)

class ListBegin(Operator):
    def __init__(self):
        super().__init__(LIST_BEGIN)

class ListEnd(Operator):
    def __init__(self):
        super().__init__(LIST_END)

class And(Operator):
    def __init__(self):
        super().__init__(AND)

class Or(Operator):
    def __init__(self):
        super().__init__(OR)

class Not(Operator):
    def __init__(self):
        super().__init__(NOT)

class Input(Operator):
    def __init__(self):
        super().__init__(INPUT)

class Random(Operator):
    def __init__(self):
        super().__init__(RANDOM)

class Assign(Operator):
    def __init__(self):
        super().__init__(ASSIGN)

class Increase(Operator):
    def __init__(self):
        super().__init__(INCREASE)

class Decrease(Operator):
    def __init__(self):
        super().__init__(DECREASE)

class Index(Operator):
    def __init__(self):
        super().__init__(INDEX)

class Call(Operator):
    def __init__(self):
        super().__init__(CALL)

class Self(Operator):
    def __init__(self):
        super().__init__(SELF)

class Statement:
    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return TYPES[self.type]

class If(Statement):
    def __init__(self):
        super().__init__(IF)

class Loop(Statement):
    def __init__(self):
        super().__init__(LOOP)

class ForLoop(Statement):
    def __init__(self):
        super().__init__(FORLOOP)

class While(Statement):
    def __init__(self):
        super().__init__(WHILE)

class Else(Statement):
    def __init__(self):
        super().__init__(ELSE)

class ElseIf(Statement):
    def __init__(self):
        super().__init__(ELSE_IF)

class Variable:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{TYPES[self.type]}: {self.value}"

class Int(Variable):
    def __init__(self, value):
        super().__init__(INT, value)

class Bool(Variable):
    def __init__(self, value):
        super().__init__(BOOL, (value == 1))

class Float(Variable):
    def __init__(self, value):
        super().__init__(FLOAT, value)

class String(Variable):
    def __init__(self, value):
        super().__init__(STRING, value)

    def __repr__(self):
        return f"{TYPES[self.type]}: '{self.value}'"

class Character(Variable):
    def __init__(self, value):
        super().__init__(CHARACTER, value)

    def __repr__(self):
        return f"{TYPES[self.type]}: '{self.value}'"

class List(Variable):
    def __init__(self, value):
        super().__init__(LIST, value)

    def __repr__(self):
        return f"{TYPES[self.type]}: [{', '.join([str(i) for i in self.value])}]"


class Dict(Variable):
    def __init__(self, value):
        super().__init__(DICT, value)

    def __repr__(self):
        return f"{TYPES[self.type]}: {'{'}{', '.join(['(' + str(i) + ')' + ': ' + '(' + str(v) + ')' for i, v in self.value.items()])}{'}'}"

class Endl:
    def __init__(self):
        self.type = ENDL

    def __repr__(self):
        return f"END LINE"

class Class:
    def __init__(self, name: str = None):
        self.name = name
        self.type = CLASS

    def __repr__(self):
        if self.name is None:
            return "CLASS"
        else:
            return f"CLASS: {self.name}"

class Define:
    def __init__(self):
        self.type = DEFINE

    def __repr__(self):
        return "DEFINE"

class DefineEnd:
    def __init__(self):
        self.type = DEFINE_END

    def __repr__(self):
        return "DEFINE"

class DefineFunction:
    def __init__(self):
        self.type = DEFINE_FUNCTION

    def __repr__(self):
        return "DEFINE_FUNCTION"

class Return:
    def __init__(self):
        self.type = RETURN

    def __repr__(self):
        return "RETURN"

class Select:
    def __init__(self):
        self.type = SELECT

    def __repr__(self):
        return "SELECT"

class GoTo:
    def __init__(self):
        self.type = GOTO

    def __repr__(self):
        return "GOTO"

class Anchor:
    def __init__(self):
        self.type = ANCHOR

    def __repr__(self):
        return "ANCHOR"

class Create:
    def __init__(self):
        self.type = CREATE

    def __repr__(self):
        return "CREATE"

class EOF:
    def __init__(self):
        self.type = EOF

    def __repr__(self):
        return "EOF"

class CodeGroupBegin:
    def __init__(self):
        self.type = CODE_GROUP_BEGIN

    def __repr__(self):
        return "CODE_GROUP_BEGIN"

class CodeGroupEnd:
    def __init__(self):
        self.type = CODE_GROUP_END

    def __repr__(self):
        return "CODE_GROUP_END"

class Delimiter:
    def __init__(self):
        self.type = DELIMITER

    def __repr__(self):
        return "DELIMITER"

class PairDelimiter:
    def __init__(self):
        self.type = PAIR_DELIMITER

    def __repr__(self):
        return "PAIR_DELIMITER"

class Separator:
    def __init__(self):
        self.type = SEPARATOR

    def __repr__(self):
        return "SEPARATOR"

class Type:
    def __init__(self, type):
        self.type = type

    def __repr__(self):
        return f"TYPE: {TYPES[self.type]}"

class IntType(Type):
    def __init__(self):
        super().__init__(INT)

class StringType(Type):
    def __init__(self):
        super().__init__(STRING)

class Swap(Operator):
    def __init__(self):
        super().__init__(SWAP)

class Import(Operator):
    def __init__(self):
        super().__init__(IMPORT)
