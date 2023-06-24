import sys

from k_llmsat_parse.render import Renderer

INPUT_PATH = f"./results/{sys.argv[1]}"
OUTPUT_PATH = f"./"

renderer = Renderer(INPUT_PATH, OUTPUT_PATH)
renderer.render_all()