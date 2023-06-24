import sys
import traceback
from k_llmsat_parse.util import get_input_paths, get_output_path
from k_llmsat_parse.extract import Extractor, ExtractorError

INPUT_PATH = "./resources/"
OUTPUT_PATH = "./intermediaries/converted/"

def extract():
    if not (2 <= len(sys.argv) <=3):
        raise TypeError(f"❌ Expect 1 or 2 arguments but {len(sys.argv) - 1} are given.")
    pdf_paths = get_input_paths("pdf", INPUT_PATH, *sys.argv[1:])
    output_path = get_output_path(OUTPUT_PATH, sys.argv[1])
    extractor = Extractor(separate_pages=True)
    for i, pdf_path in enumerate(pdf_paths):
        try:
            extractor.extract(pdf_path, output_path)
        except ExtractorError as e:
            print(f"❌ Error occurred while parsing {pdf_path}. ({i + 1}/{len(pdf_paths)})")
            traceback.print_exc()
        except Exception as e:
            print(f"❌ An unexpected error occurred while parsing {pdf_path}. Please report as an issue. ({i + 1}/{len(pdf_paths)})")
            traceback.print_exc()
        finally:
            print(f"✅ Done extracting text from {pdf_path}. ({i + 1}/{len(pdf_paths)})")


if __name__ == "__main__":
    try:
        extract()
    except Exception as e:
        print(e)
        traceback.print_exc()