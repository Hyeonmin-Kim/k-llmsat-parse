import re

def standard_parse(text:str) -> str:
    text = remove_newline(text)
    text = remove_redundant_whitespace(text)
    text = correct_isolated_punctuation(text)
    return text

def remove_newline(text:str, replacement:str=' ') -> str:
    return re.sub('\n', replacement, text)

def remove_redundant_whitespace(text:str) -> str:
    return re.sub('\s+', ' ', text)

def correct_isolated_punctuation(text:str) -> str:
    PRE_PUNCTUATIONS = ['\(', '\[', '\{', '<']
    POST_PUNCTUATIONS = ['\.', ',', '!', '\?', '\)', '\]', '\}', '>']
    for p in PRE_PUNCTUATIONS:
        text = re.sub(f"{p}\s+", p[-1:], text)
    for p in POST_PUNCTUATIONS:
        text = re.sub(f"\s+{p}", p[-1:], text)
    return text