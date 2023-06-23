import sys

from k_llmsat_parse.build import Builder

INPUT_PATH = f"./intermediaries/parsed/{sys.argv[1]}"
OUTPUT_PATH = f"./results/{sys.argv[1]}"

builder = Builder(INPUT_PATH, OUTPUT_PATH)
builder.build_all()