import json
import re

class PrologParser:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.length = len(text)
    
    def peek(self):
        if self.pos >= self.length:
            return None
        return self.text[self.pos]
    
    def consume(self):
        if self.pos >= self.length:
            return None
        char = self.text[self.pos]
        self.pos += 1
        return char
    
    def skip_whitespace(self):
        while self.pos < self.length and self.text[self.pos].isspace():
            self.pos += 1
    
    def parse_atom(self):
        start = self.pos
        while (self.pos < self.length and 
               (self.text[self.pos].isalnum() or self.text[self.pos] == '_')):
            self.pos += 1
        return self.text[start:self.pos]
    
    def parse_number(self):
        start = self.pos
        if self.peek() == '-':
            self.consume()
        while self.pos < self.length and self.text[self.pos].isdigit():
            self.pos += 1
        if self.peek() == '.':
            self.consume()
            while self.pos < self.length and self.text[self.pos].isdigit():
                self.pos += 1
        return float(self.text[start:self.pos]) if '.' in self.text[start:self.pos] else int(self.text[start:self.pos])
    
    def parse_term(self):
        self.skip_whitespace()
        
        if self.peek() == '[':
            return self.parse_list()
        elif self.peek() and (self.peek().isdigit() or self.peek() == '-'):
            return self.parse_number()
        elif self.peek() == '*':
            # Handle operators like *, +, -, etc.
            op = self.consume()
            return op
        elif self.peek() == '+':
            op = self.consume()
            return op
        elif self.peek() == '-' and self.pos + 1 < self.length and not self.text[self.pos + 1].isdigit():
            # Handle minus as operator (not negative number)
            op = self.consume()
            return op
        elif self.peek() == '/':
            op = self.consume()
            return op
        elif self.peek() == '%':
            op = self.consume()
            return op
        elif self.peek() == '>':
            op = self.consume()
            if self.peek() == '=':
                op += self.consume()
            return op
        elif self.peek() == '<':
            op = self.consume()
            if self.peek() == '=':
                op += self.consume()
            return op
        elif self.peek() == '=':
            op = self.consume()
            if self.peek() == '=':
                op += self.consume()
            return op
        elif self.peek() == '!':
            op = self.consume()
            if self.peek() == '=':
                op += self.consume()
            return op
        elif self.peek() and (self.peek().isalpha() or self.peek() == '_'):
            atom = self.parse_atom()
            self.skip_whitespace()
            if self.peek() == '(':
                # It's a compound term
                self.consume()  # consume '('
                args = []
                self.skip_whitespace()
                if self.peek() != ')':
                    args.append(self.parse_term())
                    while True:
                        self.skip_whitespace()
                        if self.peek() == ')':
                            break
                        if self.peek() == ',':
                            self.consume()
                            args.append(self.parse_term())
                        else:
                            break
                self.skip_whitespace()
                if self.peek() == ')':
                    self.consume()
                return (atom, *args)
            else:
                # It's just an atom
                return atom
        else:
            raise ValueError(f"Unexpected character at position {self.pos}: {self.peek()}")
    
    def parse_list(self):
        self.consume()  # consume '['
        items = []
        self.skip_whitespace()
        if self.peek() != ']':
            items.append(self.parse_term())
            while True:
                self.skip_whitespace()
                if self.peek() == ']':
                    break
                if self.peek() == ',':
                    self.consume()
                    items.append(self.parse_term())
                else:
                    break
        self.skip_whitespace()
        if self.peek() == ']':
            self.consume()
        return items

def parse_prolog_ast(prolog_str):
    """Parse a Prolog AST string into Python data structures"""
    parser = PrologParser(prolog_str)
    return parser.parse_term()

def parse_ast(node):
    """Convert parsed Prolog terms to JSON-friendly format"""
    if isinstance(node, list):
        return [parse_ast(elem) for elem in node]
    
    if isinstance(node, tuple):
        if len(node) == 0:
            return {}
            
        head = node[0]
        args = node[1:] if len(node) > 1 else []
        
        # Handle all the AST node types from your Prolog output
        if head == "int_decl":
            return {"type": "int_decl", "id": args[0], "value": parse_ast(args[1])}
        
        elif head == "list_decl":
            return {"type": "list_decl", "id": args[0], "value": parse_ast(args[1])}
        
        elif head == "list":
            return {"type": "list", "elements": parse_ast(args[0]) if args else []}
        
        elif head == "num":
            return {"type": "num", "value": args[0]}
        
        elif head == "fun_def":
            return {
                "type": "fun_def",
                "name": args[0],
                "params": [parse_ast(p) for p in args[1]] if len(args) > 1 else [],
                "body": parse_ast(args[2]) if len(args) > 2 else None
            }
        
        elif head == "param":
            return {"type": "param", "datatype": args[0], "id": args[1]}
        
        elif head == "block_with_conditional":
            return {
                "type": "block_with_conditional",
                "lines": parse_ast(args[0]) if args else [],
                "conditional": parse_ast(args[1]) if len(args) > 1 else None
            }
        
        elif head == "block_with_return":
            return {
                "type": "block_with_return",
                "lines": parse_ast(args[0]) if args else [],
                "return": parse_ast(args[1]) if len(args) > 1 else None
            }
        
        elif head == "if_else":
            return {
                "type": "if_else",
                "condition": parse_ast(args[0]),
                "then": parse_ast(args[1]),
                "else": parse_ast(args[2])
            }
        
        elif head == "bool_call":
            return {"type": "var_access", "base": args[0], "attr": args[1]}
        
        elif head == "func_call":
            return {
                "type": "func_call", 
                "name": args[0], 
                "args": [parse_ast(a) for a in args[1]] if len(args) > 1 else []
            }
        
        elif head == "return":
            return {"type": "return", "value": parse_ast(args[0])}
        
        elif head == "var":
            return {"type": "var", "id": args[0]}
        
        elif head == "list_op":
            return {"type": "var_access", "base": args[0], "attr": args[1]}
        
        elif head == "var_access":
            return {"type": "var_access", "base": args[0], "attr": args[1]}
        
        elif head == "dsr":
            return {"type": "var_access", "base": args[0], "attr": args[1] if len(args) > 1 and args[1] != "none" and args[1] is not None else None}
        
        elif head == "write":
            return {"type": "write", "target": parse_ast(args[0])}
        
        elif head == "binop":
            return {
                "type": "binop",
                "operator": args[0],
                "left": parse_ast(args[1]),
                "right": parse_ast(args[2])
            }
        
        elif head == "compare":
            return {
                "type": "compare",
                "operator": args[0],
                "left": parse_ast(args[1]),
                "right": parse_ast(args[2])
            }
        
        else:
            # Fallback for unknown node types
            return {"type": head, "args": [parse_ast(a) for a in args]}
    
    elif isinstance(node, str):
        # Handle string literals (variable names, operators, etc.)
        if node == "none":
            return None
        return node
    
    elif node is None:
        return None
    
    else:
        # Handle primitive types (numbers, booleans)
        return node

def ast_to_json(prolog_ast):
    """Main function to convert Prolog AST string to JSON"""
    try:
        # print("=== Original Prolog AST ===")
        # print(prolog_ast)
        # print()
        
        # Parse the Prolog term
        # print("=== Parsing... ===")
        parsed_prolog = parse_prolog_ast(prolog_ast)
        # print("Parsed successfully!")
        # print()
        
        # Convert to JSON-friendly format
        # print("=== Converting to JSON... ===")
        json_ast = parse_ast(parsed_prolog)
        # print(json.dumps(json_ast, indent=2))
        # print()
        
        return json_ast
        
    except Exception as e:
        print(f"Error converting AST: {e}")
        import traceback
        traceback.print_exc()
        return None

# # Test with your AST
# test_ast = "[int_decl(a,num(20)),list_decl(g,list([num(2),num(4),num(6),num(8)])),fun_def(F,[param(int,x),param(list,y)],block_with_conditional([int_decl(z,binop(*,x,var_access(y,head)))],if_else(compare(>,z,num(10)),return(var(z)),return(var(x))))),int_decl(b,func_call(F,[var(a),var(g)])),write(dsr(b,none))]"

# result = ast_to_json(test_ast)