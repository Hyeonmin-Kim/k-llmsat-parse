import json
import os
import re

from k_llmsat_parse.util import render_decorations

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
        general_direction = map(render_decorations, general_direction)
        gen_d = ' '.join(general_direction)
        ps = []
        for passage in passages:
            passage_text = '\n'.join(map(render_decorations, passage['paragraphs']))
            ps.append(f"<글 {passage['name']}>: {passage_text}")
        p = '\n'.join(ps)
        q = ' '.join(map(render_decorations, question['direction']))
        qps = []
        for q_passage in question['passages']:
            q_passage_text = '\n'.join(map(render_decorations, q_passage['paragraphs']))
            qps.append(f"<{q_passage['name'] or '보기'}>: {q_passage_text}")
        qp = '\n' + '\n'.join(qps) + '\n' if len(qps) > 0 else ''
        o = '\n'.join(map(render_decorations, question['options']))
        rendered  = f"""### {gen_d} ###

{p}

<질문>: {q} 하나만 골라 그 번호만 쓰시오.
{qp}
<선지>:
{o}

<답변>:"""
        return rendered + '\n\n'