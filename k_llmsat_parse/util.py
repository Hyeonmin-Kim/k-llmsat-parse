import os

###FILE/DIRECTORY MANAGEMENT###

def get_input_paths(extension:str, input_path:str, directory:str, filename:str=None) -> list[str]:
    if filename: # single file (directory, filename) 
        return [os.path.join(input_path, directory, filename)]
    else: # multiple files (directory)
        directory_path = os.path.join(input_path, directory)
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"❌ {directory_path} does not exist.")
        return [os.path.join(directory_path, filename) for filename in os.listdir(directory_path) if filename.endswith(f".{extension}")]

def get_output_path(output_path:str, directory:str) -> str:
    directory_path = os.path.join(output_path, directory)
    if not os.path.exists(output_path):
        os.mkdir(output_path)
    if not os.path.exists(directory_path):
        os.mkdir(directory_path)
    return directory_path