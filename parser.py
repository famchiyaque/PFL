import subprocess

def clean_tokens(tokens):
    """
    Cleans tokens:
    - Converts numeric strings to integers.
    - Leaves brackets and other characters as-is.
    """
    result = []
    for token in tokens:
        if isinstance(token, str) and token.isdigit():
            result.append(int(token))
        else:
            result.append(token)
    return result


def format_token(token):
    """
    Formats tokens properly for Prolog.
    - Strings get single quotes.
    - Lists are recursively formatted.
    """
    if isinstance(token, list):
        return "[" + ", ".join(format_token(t) for t in token) + "]"
    elif isinstance(token, str):
        return f"'{token}'"
    else:
        return str(token)
    
def parse_code(cleanTokens):
    
    prolog_command = f"consult('parser.pl'), parse_code({cleanTokens}), halt."

    try:
        result = subprocess.run(
            ['swipl', '-q', '-g', prolog_command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode == 0:
            return { "error": False, "tokens": cleanTokens }
        else:
            return { "error": True, "message": result.stderr.decode() }

    except Exception as e:
        return { "error": True, "message": str(e) }
    
def get_ast(cleanTokens):

    prolog_command = (
        f"consult('ast.pl'), parse_code({cleanTokens}, AST), write(AST), nl, halt."
    )

    try:
        result = subprocess.run(
            ['swipl', '-q', '-g', prolog_command],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if result.returncode == 0:
            # print("was 0 in ast func")
            output = result.stdout.decode().strip()
            return { "error": False, "ast": output }
        else:
            # print("was not 0 in ast func")
            return { "error": True, "message": result.stderr.decode() }

    except Exception as e:
        return { "error": True, "message": str(e) }