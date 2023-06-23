import os
import traceback

from pypdf import PdfReader

from k_llmsat_parse.parse import standard_parse

class Extractor:
    input_dir:str
    output_dir:str

    def __init__(self, input_dir:str, output_dir:str):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def parse_all(self):
        for pdf in os.listdir(self.input_dir):
            if pdf.endswith(".pdf"):
                print(f"✅ Start parsing {pdf}...")
                self.parse_file(pdf)

    def parse_file(self, filename:str):
        filepath = os.path.join(self.input_dir, filename)
        texts = self._parse(filepath)
        self._save_to_txt(filename, texts)

    def _parse(self, filepath:str) -> list[str]:
        reader = PdfReader(filepath)
        total_pages = len(reader.pages)
        result = []
        for curr_page in range(total_pages):
            try:
                text = reader.pages[curr_page].extract_text()
                result.append(standard_parse(text))
            except Exception:
                print(f"❌ PDF parsing has failed at page {curr_page + 1}.")
                traceback.print_exc()
        print(f"✅ Done parsing {filepath}")
        return result

    def _save_to_txt(self, filename:str, texts:list[str]):
        filepath = os.path.join(self.output_dir, f"{filename}.txt")
        with open(filepath, 'w', encoding="UTF-16") as file:
            for page_text in texts:
                file.write(page_text)
        print(f"✅ Parsed result saved at {filepath}")