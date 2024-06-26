from lexer import lex
from parser import parse
from interpreter import interpret


with open("main.haram") as file:
    tokens = lex(file)
    # print(tokens)

ast = parse(tokens)
# print(ast)

interpret(ast)
