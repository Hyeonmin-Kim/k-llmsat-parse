import sys
from k_llmsat_parse.extract import Extractor

INPUT_PATH = f"./resources/{sys.argv[1]}"
OUTPUT_PATH = f"./intermediaries/converted/{sys.argv[1]}"

extractor = Extractor(INPUT_PATH, OUTPUT_PATH)
extractor.parse_all()