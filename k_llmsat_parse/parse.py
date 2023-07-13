import re

def standard_parse(text:str) -> str:
    # text = remove_newline(text)
    # text = remove_redundant_whitespace(text)
    text = correct_isolated_punctuation(text)
    text = mark_group(text)
    text = mark_question(text)
    text = mark_options(text)
    text = mark_question_passages(text)
    text = mark_group_passages(text)
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

def mark_group(text):
    matches = re.findall('\[\d+(?:～|~)\d+\]', text)
    for m in matches:
        text = re.sub(re.escape(m), f"\nGGG {m}\n", text)
    return text

def mark_question(text):
    matches = re.findall('\d+\.', text)
    for m in matches:
        text = re.sub(re.escape(m), f"\nQQQ {m[:-1]}\n", text)
    return text

def mark_options(text):
    text = re.sub('①', f"\nOOO\n①", text)
    return text

def mark_question_passages(text):
    for match in re.finditer('QQQ([^Q]*(?:\?|\[\d점\]))((?:(?:\s|\n)*<.*>)?)([^Q]*)OOO', text):
        groups = match.groups()
        if not groups[2].isspace():
            text = re.sub(re.escape(match.group()), f"QQQ{groups[0]}\nPPP {groups[1].strip()}\n{groups[2]}\nOOO", text)
    return text

def mark_group_passages(text):
    text = re.sub('물음에 답하시오\.(?:\s)*\n\(가\)', f"물음에 답하시오.\nPPP (가)\n", text)
    matches = re.findall('(\s\([나-힣]\)\s)', text)
    for m in matches:
        text = re.sub(re.escape(m), f"\nPPP {m.strip()}\n", text)
    text = re.sub('물음에 답하시오\.(\s)*\n(?!PPP)', f"물음에 답하시오.\nPPP\n", text)
    return text