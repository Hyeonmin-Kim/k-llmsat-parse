import sys
import os
import traceback
from k_llmsat_parse.extract import Extractor, ExtractorError

INPUT_PATH = "./resources/"
OUTPUT_PATH = "./intermediaries/converted/"

def extract():
    if not (2 <= len(sys.argv) <=3):
        raise TypeError(f"❌ Expect 1 or 2 arguments but {len(sys.argv) - 1} are given.")
    pdf_paths = get_pdf_paths(*sys.argv[1:])
    output_path = get_output_path(sys.argv[1])
    extractor = Extractor()
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
            print(f"✅ Done parsing {pdf_path}. ({i + 1}/{len(pdf_paths)})")
    
def get_pdf_paths(directory:str, filename:str=None) -> list[str]:
    if filename: # single file (directory, filename) 
        return [os.path.join(INPUT_PATH, directory, filename)]
    else: # multiple files (directory)
        directory_path = os.path.join(INPUT_PATH, directory)
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"❌ {directory_path} does not exist.")
        return [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if filename.endswith(".pdf")]

def get_output_path(directory:str) -> str:
    directory_path = os.path.join(OUTPUT_PATH, directory)
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    return directory_path


if __name__ == "__main__":
    try:
        extract()
    except Exception as e:
        print(e)
        traceback.print_exc()