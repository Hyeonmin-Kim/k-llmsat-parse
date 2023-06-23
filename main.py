from k_llmsat_parse.extract import Extractor

INPUT_PATH = "./resources/수능"
OUTPUT_PATH = "./results/수능"

extractor = Extractor(INPUT_PATH, OUTPUT_PATH)
extractor.parse_all()