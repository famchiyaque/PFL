import re
import sys

# Token regex with named groups for clarity
token_pattern = re.compile(
    r"\b(?:int|list|fun|return|write)\b|"                  # keywords
    r"\-?[0-9]+|"                                          # numbers (including negative)
    r"\.head|\.tail|\.empty|\.length|\.popHead|\.pushHead|\.pushTail|\.popTail|"  # dot access
    r"==|<=|>=|!=|=|<|>|\+|\-|\*|\/|"                      # operators
    r"[A-Za-z_][A-Za-z0-9_]*|"                             # identifiers
    r"[{}\[\]();,:?]"                                      # punctuation
)

# Pattern for validating individual tokens
valid_pattern = re.compile(
    r"^(int|list|fun|return|write|[a-zA-Z_][a-zA-Z0-9_]*|"
    r"\-?[0-9]+|"
    r"\+|\-|\*|\/|<=|>=|<|>|=|==|!=|;|\(|\)|\{|\}|\[|\]|,|\.head|\.tail|"
    r"\.pushHead|\.popHead|\.pushTail|\.popTail|\.empty|\.length|\?|:)$"
)

def tokenize_and_validate(file_name):
    with open(file_name, 'r') as file:
        code = file.read()

    tokens = []
    for match in token_pattern.finditer(code):
        token = match.group()

        if not valid_pattern.fullmatch(token):
            raise SyntaxError(f"Invalid token: {token}")

        if re.fullmatch(r"\-?[0-9]+", token):  # if token is an integer literal
            tokens.append(int(token))
        else:
            tokens.append(token)

    return tokens
