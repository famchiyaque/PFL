import ast
import re
import json

def tokenize(prolog_ast_str):
    # Replace Prolog-style atoms with quoted strings so Python can parse them
    # Examples: int_decl -> "int_decl", num(16) stays num(16)
    tokens = re.sub(r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b', r'"\1"', prolog_ast_str)
    tokens = tokens.replace('none', 'null')  # for JSON compatibility
    return tokens

def parse_ast(node):
    if isinstance(node, list):
        return [parse_ast(elem) for elem in node]
    
    if isinstance(node, tuple):
        head = node[0]
        args = node[1:]
        
        if head == "int_decl":
            return {"type": "int_decl", "id": args[0], "value": parse_ast(args[1])}
        
        elif head == "list_decl":
            return {"type": "list_decl", "id": args[0], "value": parse_ast(args[1])}
        
        elif head == "list":
            return {"type": "list", "elements": args[0]}
        
        elif head == "num":
            return {"type": "num", "value": args[0]}
        
        elif head == "fun_def":
            return {
                "type": "fun_def",
                "name": args[0],
                "params": [parse_ast(p) for p in args[1]],
                "body": parse_ast(args[2])
            }
        
        elif head == "param":
            return {"type": "param", "datatype": args[0], "id": args[1]}
        
        elif head == "if_else":
            return {
                "type": "if_else",
                "condition": parse_ast(args[0]),
                "then": parse_ast(args[1]),
                "else": parse_ast(args[2])
            }
        
        elif head == "bool_call":
            return {"type": "bool_call", "base": args[0], "attr": args[1]}
        
        elif head == "func_call":
            return {"type": "func_call", "name": args[0], "args": [parse_ast(a) for a in args[1]]}
        
        elif head == "return":
            return {"type": "return", "value": parse_ast(args[0])}
        
        elif head == "var_access":
            return {"type": "dsr", "base": args[0], "attr": args[1]}
        
        elif head == "dsr":
            return {"type": "dsr", "base": args[0], "attr": args[1] if args[1] != "null" else None}
        
        elif head == "writ_call":
            return {"type": "write_call", "target": parse_ast(args[0])}
        
        elif head == "e":
            return parse_ast(args[0])
        
        else:
            # fallback
            return {"type": head, "args": [parse_ast(a) for a in args]}
    
    elif isinstance(node, str):
        return {"type": "var", "id": node}
    
    else:
        return node
    
def ast_to_json(ast):
    # === Convert to Python-readable ===
    tokenized = tokenize(ast)
    print(tokenized)
    parsed_raw = ast.literal_eval(tokenized)
    print(parsed_raw)
    json_ast = parse_ast(parsed_raw)
    print(json_ast)

    # === Output as JSON ===
    print(json.dumps(json_ast, indent=2))

    return json_ast
