import re
import sys

# valid_pattern = re.compile(
#     r"(int|list|fun|return|write|[a-z]|[A-Z]|[0-9]+|"
#     r"\+|\-|\*|\/|<=|>=|<|>|=|;|\(|\)|\{|\}|\[|\]|,|\.head|\.tail|"
#     r"\.pushHead|\.popHead|\.pushTail|\.popTail|\.empty|\?|:)"
# )

valid_pattern = re.compile(
    r"(int|list|fun|return|write|[a-z][a-zA-Z0-9_]*|[A-Z][a-zA-Z0-9_]*|"
    r"\-?[0-9]+|"
    r"\+|\-|\*|\/|<=|>=|<|>|=|;|\(|\)|\{|\}|\[|\]|,|\.head|\.tail|"
    r"\.pushHead|\.popHead|\.pushTail|\.popTail|\.empty|\?|:)"
)

def validate_word(word):
    # print("current 'word': ", word)
    # Check if it's a number (positive or negative)
    # if re.fullmatch(r"\-?[0-9]+", word):
    #     try:
    #         num = int(word)
    #         return -sys.maxsize - 1 <= num <= sys.maxsize
    #     except (ValueError, OverflowError):
    #         return False
    return bool(valid_pattern.fullmatch(word))

def validate_code(words):
    for word in words:
        if not validate_word(word):
            return False
    return True
