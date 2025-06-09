env = {} 

def eval_program(ast):
    result = None

    for stmt in ast:
        result = eval_statement(stmt)
    
    return result

def eval_statement(stmt):
    if stmt["type"] == "int_decl":
        name = stmt["id"]
        value = eval_expr(stmt["value"])
        env[name] = value
        return None

    elif stmt["type"] == "return":
        return eval_expr(stmt["value"])

    elif stmt["type"] == "list_decl":
        name = stmt["id"]
        value = eval_expr(stmt["value"])
        env[name] = value
        return None

    elif stmt["type"] == "write_call":
        val = eval_expr(stmt["value"])
        print(val)
        return None

    # ... handle fun_def, func_call, if_else, etc.

    else:
        raise Exception(f"Unknown statement type: {stmt['type']}")

def eval_expr(expr):
    if expr["type"] == "num":
        return expr["value"]

    elif expr["type"] == "var":
        return env[expr["id"]]

    elif expr["type"] == "list":
        return expr["values"]

    elif expr["type"] == "bool_call":
        # Example: check if a list is empty
        var = env[expr["id"]]
        return len(var) == 0 if expr["func"] == "empty" else None

    elif expr["type"] == "func_call":
        # Lookup and evaluate the function body manually
        func = env[expr["id"]]
        args = [eval_expr(arg) for arg in expr["args"]]
        return eval_user_function(func, args)

    elif expr["type"] == "dsr":
        # handle accessing list head/tail
        return handle_dsr(expr)

    else:
        raise Exception(f"Unknown expression type: {expr['type']}")

def eval_user_function(func, args):
    
    return ''

def handle_dsr(expr):

    return ''