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
    
    elif stmt["type"] == "fun_def":
        env[stmt["name"]] = stmt
        return None

    elif stmt["type"] == "write":
        val = eval_expr(stmt["target"])
        print(val)
        return None
    
    elif stmt["type"] == "if_else":
        condition = eval_expr(stmt["condition"])
        if condition:
            return eval_statement(stmt["then"])
        else:
            return eval_statement(stmt["else"])
    
    elif stmt["type"] == "block_with_conditional":
        # Execute all lines first
        for line in stmt["lines"]:
            eval_statement(line)
        # Then execute the conditional
        return eval_statement(stmt["conditional"])
    
    elif stmt["type"] == "block_with_return":
        # Execute all lines first
        for line in stmt["lines"]:
            eval_statement(line)
        # Then execute the return
        return eval_statement(stmt["return"])

    else:
        raise Exception(f"Unknown statement type: {stmt['type']}")

def eval_expr(expr):
    # Handle case where expr might be a string (variable name)
    if isinstance(expr, str):
        return env[expr]
    
    if expr["type"] == "num":
        return expr["value"]

    elif expr["type"] == "var":
        return env[expr["id"]]

    elif expr["type"] == "list":
        return [eval_expr(e) for e in expr["elements"]]
    
    elif expr["type"] == "var_access":
        base = env[expr["base"]]
        attr = expr.get("attr")
        
        if attr is None:
            return base
        elif attr == "empty":
            # Boolean check for empty list
            return len(base) == 0
        elif attr == "head":
            # Return first element of list
            return base[0] if base else None
        elif attr == "tail":
            # Return last element of list
            return base[-1] if base else None
        elif attr == "length":
            return len(base)
        elif attr == "pop_head":
            # Return list without first element
            return base[1:] if base else []
        elif attr == "pop_tail":
            # Return list without last element
            return base[:-1] if base else []
        elif isinstance(attr, tuple) and attr[0] == "push_head":
            # Handle push_head operation
            value_to_push = eval_expr(attr[1]) if not isinstance(attr[1], str) else env[attr[1]]
            new_list = [value_to_push] + base.copy()
            return new_list
        elif isinstance(attr, tuple) and attr[0] == "push_tail":
            # Handle push_tail operation
            value_to_push = eval_expr(attr[1]) if not isinstance(attr[1], str) else env[attr[1]]
            new_list = base.copy() + [value_to_push]
            return new_list
        else:
            raise Exception(f"Unknown var_access attribute: {attr}")

    elif expr["type"] == "binop":
        left = eval_expr(expr["left"])
        right = eval_expr(expr["right"])
        op = expr["operator"]
        
        if op == "+":
            return left + right
        elif op == "-":
            return left - right
        elif op == "*":
            return left * right
        elif op == "/":
            return left / right
        elif op == "%":
            return left % right
        else:
            raise Exception(f"Unknown binary operator: {op}")
    
    elif expr["type"] == "compare":
        left = eval_expr(expr["left"])
        right = eval_expr(expr["right"])
        op = expr["operator"]
        
        if op == ">":
            return left > right
        elif op == "<":
            return left < right
        elif op == ">=":
            return left >= right
        elif op == "<=":
            return left <= right
        elif op == "==":
            return left == right
        elif op == "!=":
            return left != right
        else:
            raise Exception(f"Unknown comparison operator: {op}")
    
    elif expr["type"] == "func_call":
        func_def = env[expr["name"]]
        args = [eval_expr(arg) for arg in expr["args"]]
        return eval_user_function(func_def, args)

    else:
        raise Exception(f"Unknown expression type: {expr['type']}")

def eval_user_function(func_def, args):
    # Create a new local environment
    local_env = {}
    params = func_def["params"]
    
    # Bind parameters to arguments
    for param, arg in zip(params, args):
        local_env[param["id"]] = arg

    # Save the outer environment so we can restore it later
    global env
    outer_env = env.copy()  # Make a copy to preserve outer scope
    
    # Merge local environment with global environment
    env.update(local_env)

    try:
        result = eval_statement(func_def["body"])
    finally:
        # Restore original environment
        env = outer_env

    return result