import os
import re

###FILE/DIRECTORY MANAGEMENT###

def get_input_paths(extension:str, input_path:str, directory:str, filename:str=None) -> list[str]:
    if filename: # single file (directory, filename) 
        return [os.path.join(input_path, directory, filename)]
    else: # multiple files (directory)
        directory_path = os.path.join(input_path, directory)
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"❌ {directory_path} does not exist.")
        return [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if filename.endswith(f".{extension}")]

def get_output_path(output_path:str, directory:str) -> str:
    directory_path = os.path.join(output_path, directory)
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    return directory_path

###COMMON TAGGING PATTERNS###

def render_decorations(text:str) -> str:
    ## filled functional: r, s, h (HTML-like tag: <[A] 시작> ~ <[A] 끝>) 
    ## decoration: u, i, b, d (일단 무시)
    ## image: III
    start_tag_pattern = lambda c: f"(?<!{c}){c}(?!{c}+)(.+?)(?<!{c}){c*2}(?!{c}+)"
    end_tag_pattern = lambda c: c * 3
    decoration_pattern = lambda c: f"(?<!{c}){c*2}(?!{c}+)(.+?)(?<!{c}){c*3}(?!{c}+)"
    for c in "rsh":
        matches = re.findall(start_tag_pattern(c), text)
        for name in matches:
            text = text.replace(f"{c}{name}{c*2}", f"<구간 {name} 시작>")
        text = text.replace(end_tag_pattern(c), "<구간 끝>")
    for c in "uibd":
        matches = re.findall(decoration_pattern(c), text)
        for content in matches:
            text = text.replace(f"{c*2}{content}{c*3}", content)
    text = text.replace("III", "[이미지 대체 텍스트]")
    return text