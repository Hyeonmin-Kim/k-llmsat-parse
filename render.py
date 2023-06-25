import sys
import traceback
from k_llmsat_parse.util import get_input_paths, get_output_path
from k_llmsat_parse.render import Renderer

INPUT_PATH = "./results/"
OUTPUT_PATH = "./prompts/"

def render():
    if not (2 <= len(sys.argv) <=3):
        raise TypeError(f"❌ Expect 1 or 2 arguments but {len(sys.argv) - 1} are given.")
    json_paths = get_input_paths("json", INPUT_PATH, *sys.argv[1:])
    output_path = get_output_path(OUTPUT_PATH, sys.argv[1])
    renderer = Renderer()
    for i, json_path in enumerate(json_paths):
        try:
            renderer.render(json_path, output_path)
        except Exception as e:
            print(f"❌ An unexpected error occurred while rendering {json_path}. Please report as an issue. ({i + 1}/{len(json_path)})")
            traceback.print_exc()
        finally:
            print(f"✅ Done rendering {json_path}. ({i + 1}/{len(json_path)})")

if __name__ == "__main__":
    try:
        render()
    except Exception as e:
        print(e)
        traceback.print_exc()