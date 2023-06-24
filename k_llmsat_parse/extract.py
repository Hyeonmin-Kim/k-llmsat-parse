import os

from pypdf import PdfReader

from k_llmsat_parse.parse import standard_parse

class Extractor:
    separate_pages:bool

    def __init__(self, separate_pages:bool=True):
        self.separate_pages = separate_pages

    def extract(self, filepath:str, output_path:str):
        texts = self.__extract(filepath)
        self.__save_to_txt(filepath, output_path, texts)

    def __extract(self, filepath:str) -> list[str]:
        reader = PdfReader(filepath)
        total_pages = len(reader.pages)
        texts = []
        for curr_page in range(total_pages):
            try:
                text = reader.pages[curr_page].extract_text()
                texts.append(standard_parse(text))
            except Exception:
                raise ExtractorError(f"❌ PDF parsing has failed at page {curr_page + 1}.")
        return texts

    def __save_to_txt(self, filepath:str, output_path:str, texts:list[str]):
        filename = os.path.basename(filepath).split('.')[0]
        with open(os.path.join(output_path, f"{filename}.txt"), 'w', encoding="UTF-8-SIG") as file:
            for i, page_text in enumerate(texts):
                if self.separate_pages:
                    file.write(f"\n\n===================[PAGE {i + 1}/{len(texts)}]===================\n\n")
                file.write(page_text)

class ExtractorError(Exception):
    ...