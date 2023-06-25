import json
import os
import re

## TODO: Refactor using LangChain

class Renderer:

    def __init__(self):
        ...

    def render(self, filepath:str, output_path:str):
        filename = os.path.basename(filepath).split(".")[0]
        output_filepath = os.path.join(output_path, f"{filename}.txt")
        with open(filepath, 'r', encoding="UTF-8-SIG") as file:
            data = json.load(file)
        with open(output_filepath, 'w', encoding="UTF-8-SIG") as file:
            for group in data['contents']:
                for question in group['questions']:
                    rendered = self._render_question(group['direction'], group['passages'], question)
                    file.writelines(rendered)

    def _render_question(self, general_direction:list[str], passages:list[dict], question:dict) -> str:
        general_direction = map(self._render_decorations, general_direction)
        gen_d = ' '.join(general_direction)
        ps = []
        for passage in passages:
            passage_text = '\n'.join(map(self._render_decorations, passage['paragraphs']))
            ps.append(f"<글 {passage['name']}>: {passage_text}")
        p = '\n'.join(ps)
        q = ' '.join(map(self._render_decorations, question['direction']))
        qps = []
        for q_passage in question['passages']:
            q_passage_text = '\n'.join(map(self._render_decorations, q_passage['paragraphs']))
            qps.append(f"<{q_passage['name'] or '보기'}>: {q_passage_text}")
        qp = '\n' + '\n'.join(qps) + '\n' if len(qps) > 0 else ''
        o = '\n'.join(map(self._render_decorations, question['options']))
        rendered  = f"""### {gen_d} ###

{p}

<질문>: {q} 하나만 골라 그 번호만 쓰시오.
{qp}
<선지>:
{o}

<답변>:"""
        return rendered + '\n\n'

    def _render_decorations(self, text:str) -> str:
        ## filled functional: r, s, h (HTML-like tag: <[A] 시작> ~ <[A] 끝>) 
        ## decoration: u, i, b, d (일단 무시)
        ## image: III
        start_tag_pattern = lambda c: f"(?<!{c}){c}(?!{c}+)(.+?)(?<!{c}){c*2}(?!{c}+)"
        end_tag_pattern = lambda c: c * 3
        for c in "rsh":
            matches = re.findall(start_tag_pattern(c), text)
            for name in matches:
                text = text.replace(f"{c}{name}{c*2}", f"<구간 {name} 시작>")
            text = text.replace(end_tag_pattern(c), "<구간 끝>")
        decoration_pattern = lambda c: f"(?<!{c}){c*2}(?!{c}+)(.+?)(?<!{c}){c*3}(?!{c}+)"
        for c in "uibd":
            matches = re.findall(decoration_pattern(c), text)
            for content in matches:
                text = text.replace(f"{c*2}{content}{c*3}", content)
        text = text.replace("III", "[이미지 대체 텍스트]")
        return text