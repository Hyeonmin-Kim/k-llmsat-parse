import os

from pypdf import PdfReader

from k_llmsat_parse.parse import standard_parse

class Extractor:
    separate_pages:bool

    def __init__(self, separate_pages:bool=True):
        self.separate_pages = separate_pages

    def extract(self, filepath:str, output_path:str, header_height:int=50, footer_height:int=50):
        texts = self._extract(filepath, header_height, footer_height)
        self._save_to_txt(filepath, output_path, texts)

    def _extract(self, filepath:str, header_height:int, footer_height:int) -> list[str]:
        reader = PdfReader(filepath)
        total_pages = len(reader.pages)
        texts = []
        def visitor_body(text, cm, tm, fontDict, fontSize):
            y = tm[5]
            if 100 < y < 1030 and (len(text) == 0 or not text.startswith('Çt')):
                texts[-1] += text
        for curr_page in range(total_pages):
            texts.append("")
            try:
                reader.pages[curr_page].extract_text(visitor_text=visitor_body)
                texts[-1] = standard_parse(texts[-1])
            except Exception:
                raise ExtractorError(f"❌ PDF parsing has failed at page {curr_page + 1}.")
        return texts

    def _save_to_txt(self, filepath:str, output_path:str, texts:list[str]):
        filename = os.path.basename(filepath).split('.')[0]
        with open(os.path.join(output_path, f"{filename}.txt"), 'w', encoding="UTF-8-SIG") as file:
            file.write(self._fetch_header())
            for i, page_text in enumerate(texts):
                if self.separate_pages:
                    file.write(f"\n\n===================[PAGE {i + 1}/{len(texts)}]===================\n\n")
                file.write(page_text)

    def _fetch_header(self):
        return "default_q_weight: 2\noption_num: 5\n<START>\n"

class ExtractorError(Exception):
    ...