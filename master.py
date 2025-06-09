import subprocess
import json

# from tokenizer import tokenize_code
# from lexer import validate_code
from lexer2 import tokenize_and_validate
from parser import parse_code, get_ast
from converter import ast_to_json
from interpreter import eval_program

# def tokenize(file_name):
#     tokens = tokenize_code(file_name=file_name)
#     return tokens


# def run_lexer(tokens):
#     result = validate_code(tokens)
#     if result is True:
#         return {"data": tokens, "error": False}
#     else:
#         return {"data": [], "error": True}

def run_lexer(file_name):
    result = tokenize_and_validate(file_name)
    return result


def run_parser(cleanTokens):
    result = parse_code(cleanTokens)
    return result


def run_ast(tokens):
    # result = get_ast(tokens["data"])
    result = get_ast(tokens)
    return result


def run_converter(ast):
    result = ast_to_json(ast)
    return result

def run_interpreter(ast_json):
    eval_program(ast_json)

if __name__ == "__main__":
    tokens = run_lexer("new.pfl")
    print(tokens)

    cleanSyntax = run_parser(tokens)
    if cleanSyntax["error"]:
        print("Syntax error")
        print(cleanSyntax.get("message", ""))
        exit()
    print(cleanSyntax)

    ast = run_ast(tokens)
    if ast["error"]:
        print("Syntax Error")
        print(ast.get("message", ""))
        exit()

    ast = ast["ast"]
    print(ast)

    ast_json = run_converter(ast)
    print(ast_json)

    run_interpreter(ast_json)

    print("----------End of program-------------")
