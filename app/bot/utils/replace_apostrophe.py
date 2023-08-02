import re


def replace_apostrophe(string: str) -> str:
    return re.sub(r'\'|\*|"', "`", string)
