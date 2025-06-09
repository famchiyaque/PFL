import re

def tokenize_code(file_name):
    with open(file_name, 'r') as file:
        code = file.read()

    # Split by tokens using regex: match words, numbers, and symbols
    token_pattern = re.compile(
        r"\b(?:int|list|fun|return|write)\b|"    # keywords
        r"[A-Za-z_][A-Za-z0-9_]*|"               # identifiers
        r"[0-9]+|"                               # numbers
        r"\.head|\.tail|\.empty|\.popHead|\.pushHead|"  # dot-access
        r"==|<=|>=|!=|=|<|>|\+|\-|\*|\/|"        # operators
        r"[{}\[\]();,:?]"                        # punctuation
    )

    tokens = token_pattern.findall(code)
    
    # tokens = []
    # for match in token_pattern.finditer(code):
    #     token = match.group()
    #     # Convert numbers to integers immediately
    #     if re.fullmatch(r"-?\d+", token):
    #         tokens.append(int(token))
    #     else:
    #         tokens.append(token)

    return tokens