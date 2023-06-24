import sys
import traceback
from k_llmsat_parse.util import get_input_paths, get_output_path
from k_llmsat_parse.build import Builder, BuilderError

INPUT_PATH = "./intermediaries/parsed/"
OUTPUT_PATH = "./results/"

def build():
    if not (2 <= len(sys.argv) <=3):
        raise TypeError(f"❌ Expect 1 or 2 arguments but {len(sys.argv) - 1} are given.")
    parsed_txt_paths = get_input_paths("txt", INPUT_PATH, *sys.argv[1:])
    output_path = get_output_path(OUTPUT_PATH, sys.argv[1])
    builder = Builder()
    for i, parsed_txt_path in enumerate(parsed_txt_paths):
        try:
            builder.build(parsed_txt_path, output_path)
        except BuilderError as e:
            print(f"❌ Error occurred while building JSON from {parsed_txt_path}. ({i + 1}/{len(parsed_txt_paths)})")
            traceback.print_exc()
        except Exception as e:
            print(f"❌ An unexpected Error occurred while building JSON from {parsed_txt_path}. Please report as an issue. ({i + 1}/{len(parsed_txt_paths)})")
            traceback.print_exc()
        finally:
            print(f"✅ Done building JSON from {parsed_txt_path}. ({i + 1}/{len(parsed_txt_paths)})")

if __name__=="__main__":
    try:
        build()
    except Exception as e:
        print(e)
        traceback.print_exc()