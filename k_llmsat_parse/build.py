import json
import os

CODE_LEN = 3

STOPWORD_DICT = {
    'GGG': {'GGG'},
    'QQQ': {'GGG', 'QQQ'},
    'DDD': {'GGG', 'DDD', 'PPP', 'OOO', 'QQQ'},
    'PPP': {'GGG', 'DDD', 'PPP', 'OOO', 'QQQ'},
    'OOO': {'GGG', 'DDD', 'PPP', 'OOO', 'QQQ'}
    }

class Builder:
    input_dir:str
    output_dir:str

    def __init__(self, input_dir:str, output_dir:str):
        self.input_dir = input_dir
        self.output_dir = output_dir

    def build_all(self):
        for txt in os.listdir(self.input_dir):
            if txt.endswith(".txt"):
                print(f"✅ Start building data from {txt}...")
                self.build_data(txt)

    def build_data(self, filename:str):
        data = self._build(filename)

    def _build(self, filename:str) -> dict:
        # 1. initialization
        filepath = os.path.join(self.input_dir, filename)
        data = {
            'name': filename,
            'contents': []
        }
        # 2. file input
        with open(filepath, 'r', encoding="UTF-8-SIG") as file:
             lines = file.readlines()
        lines = list(map(lambda line: line.strip(), lines))
        # 3. parsing
        temp_idx = 0
        while temp_idx < len(lines):
            temp_idx = self._parse(temp=data['contents'], temp_idx=temp_idx, lines=lines, filename=filename)
        print(data)
        # 4. saving
        self._save_as_json(filename=filename, data=data)


    def _parse(self, temp:object, temp_idx:int, lines:list[str], filename:str) -> int:
        mode = lines[temp_idx][:3]
        if mode == 'GGG': 
            temp_idx = self._create_group(temp, temp_idx, lines, filename)
        elif mode == 'DDD': 
            temp_idx = self._create_direction(temp['direction'], temp_idx, lines, filename)
        elif mode == 'PPP': 
            temp_idx = self._create_passage(temp['passages'], temp_idx, lines, filename)
        elif mode == 'QQQ': 
            temp_idx = self._create_question(temp['questions'], temp_idx, lines, filename)
        elif mode == 'OOO': 
            temp_idx = self._create_options(temp['options'], temp_idx, lines, filename)
        else:
            print(f"⚠️ Unexpected token at line {temp_idx} of {filename} : {mode}")
            temp_idx += 1
        return temp_idx
    
    def _create_group(self, temp:list, temp_idx:int, lines:list[str], filename:str) -> int:
        new_group = {
            'direction': [],
            'passages': [],
            'questions': [],
        }
        temp_idx += 1
        while temp_idx < len(lines) and lines[temp_idx][:3] not in STOPWORD_DICT['GGG']:
            temp_idx = self._parse(temp=new_group, temp_idx=temp_idx, lines=lines, filename=filename)
        temp.append(new_group)
        return temp_idx
    
    def _create_direction(self, temp:list, temp_idx:int, lines:list[str], filename:str) -> int:
        temp_idx += 1
        while temp_idx < len(lines) and lines[temp_idx][:3] not in STOPWORD_DICT['DDD']:
            temp.append(lines[temp_idx])
            temp_idx += 1
        return temp_idx
    
    def _create_passage(self, temp:list, temp_idx:int, lines:list[str], filename:str) -> int:
        new_passage = {
            'name': "",
            'paragraphs': []
        }
        if len(lines[temp_idx]) > 3:
            new_passage['name'] = lines[temp_idx][CODE_LEN + 1:]
        temp_idx += 1
        while temp_idx < len(lines) and lines[temp_idx][:3] not in STOPWORD_DICT['PPP']:
            new_passage['paragraphs'].append(lines[temp_idx])
            temp_idx += 1
        temp.append(new_passage)
        return temp_idx
    
    def _create_question(self, temp:list, temp_idx:int, lines:list[str], filename:str) -> int:
        new_question = {
            'number': -1,           ## TODO
            'weight': -1,           ## TODO
            'direction' : [],
            'passages': [],
            'options': []
        }
        temp_idx += 1
        new_question['direction'].append(lines[temp_idx])
        temp_idx += 1
        while temp_idx < len(lines) and lines[temp_idx][:3] not in STOPWORD_DICT['QQQ']:
            temp_idx = self._parse(temp=new_question, temp_idx=temp_idx, lines=lines, filename=filename)
        temp.append(new_question)
        return temp_idx
    
    def _create_options(self, temp:list, temp_idx:int, lines:list[str], filename:str) -> int:
        temp_idx += 1
        while temp_idx < len(lines) and lines[temp_idx][:3] not in STOPWORD_DICT['OOO']:
            temp.append(lines[temp_idx])
            temp_idx += 1
        return temp_idx
    
    def _save_as_json(self, filename:str, data:dict):
        filepath = os.path.join(self.output_dir, f"{filename}.json")
        with open(filepath, 'w', encoding="UTF-8") as file:
            json.dump(data, file, indent=4)