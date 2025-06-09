import subprocess
import json
import sys

from lexer import tokenize_and_validate
from parser import get_ast
from converter import ast_to_json
from interpreter import eval_program

def run_lexer(file_name):
    try:
        result = tokenize_and_validate(file_name)
        return {"success": True, "data": result}
    except FileNotFoundError:
        return {"success": False, "error": f"File '{file_name}' not found."}
    except SyntaxError as e:
        return {"success": False, "error": f"Lexical error: {str(e)}"}
    except Exception as e:
        return {"success": False, "error": f"Unexpected error during tokenization: {str(e)}"}


def run_ast(tokens):
    try:
        result = get_ast(tokens)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": f"Parsing error: {str(e)}"}


def run_converter(ast):
    try:
        result = ast_to_json(ast)
        return {"success": True, "data": result}
    except Exception as e:
        return {"success": False, "error": f"AST conversion error: {str(e)}"}


def run_interpreter(ast_json):
    try:
        eval_program(ast_json)
        return {"success": True}
    except Exception as e:
        return {"success": False, "error": f"Runtime error: {str(e)}"}


if __name__ == "__main__":
    # Check for command-line arguments
    if len(sys.argv) != 2:
        print("Usage: python master.py <filename>")
        print("Example: python master.py ex.pfl")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Stage 1: Tokenizing/Lexing
    print(f"Stage 1: Tokenizing/Lexing '{filename}'...")
    tokens_result = run_lexer(filename)
    if not tokens_result["success"]:
        print("Failed in tokenizing/lexing stage.")
        print(tokens_result["error"])
        sys.exit(1)
    
    tokens = tokens_result["data"]
    print("✓ Tokenizing/Lexing completed successfully.")

    # Stage 2: Parsing/AST Generation
    print("\nStage 2: Parsing/AST Generation...")
    ast_result = run_ast(tokens)
    if not ast_result["success"]:
        print("Failed in parsing/AST stage.")
        print(ast_result["error"])
        sys.exit(1)
    
    # Handle your existing parser's error format
    ast_data = ast_result["data"]
    if isinstance(ast_data, dict) and ast_data.get("error"):
        print("Failed in parsing/AST stage.")
        print("Syntax Error")
        print(ast_data.get("message", ""))
        sys.exit(1)
    
    ast = ast_data["ast"] if isinstance(ast_data, dict) and "ast" in ast_data else ast_data
    print("✓ Parsing/AST Generation completed successfully.")

    # Stage 3: AST to JSON Conversion
    print("\nStage 3: AST to JSON Conversion...")
    json_result = run_converter(ast)
    if not json_result["success"]:
        print("Failed in AST conversion stage.")
        print(json_result["error"])
        sys.exit(1)
    
    ast_json = json_result["data"]
    print("✓ AST to JSON Conversion completed successfully.")

    # Stage 4: Interpretation/Execution
    print("\nStage 4: Interpretation/Execution...")
    print("Program output:")
    print("-" * 20)
    
    interpreter_result = run_interpreter(ast_json)
    if not interpreter_result["success"]:
        print("-" * 20)
        print("Failed in interpretation/execution stage.")
        print(interpreter_result["error"])
        sys.exit(1)
    
    print("-" * 20)
    print("✓ Program executed successfully.")