from itertools import chain
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

PARENT_DICT = {
    'GGG': {'dataset'},
    'QQQ': {'group'},
    'DDD': {'group', 'question'},
    'PPP': {'group', 'question'},
    'OOO': {'question'}
}

class Builder:

    def __init__(self, option_num:int):
        self.success_flag = True
        self.option_num = option_num

    def build(self, filepath:str, output_path:str):
        # 1. initialization
        self.success_flag = True
        filename = os.path.basename(filepath).split(".")[0]
        dataset = {
            'type': 'dataset',
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
            temp_idx = self.__parse(temp=dataset, temp_idx=temp_idx, lines=lines, filepath=filepath)
        # 4. saving
        self.__save_as_json(filename, output_path, dataset)
        # 5. summary
        self.__verify_and_summurize_result(filename, dataset)


    def __parse(self, temp:dict, temp_idx:int, lines:list[str], filepath:str) -> int:
        mode = lines[temp_idx][:3]
        info = (temp_idx, lines, filepath)
        try:
            self.__check(mode, temp, *info)
            if mode == 'GGG': 
                temp_idx = self.__create_group(temp['contents'], *info)
            elif mode == 'DDD': 
                temp_idx = self.__create_direction(temp['direction'], *info)
            elif mode == 'PPP': 
                temp_idx = self.__create_passage(temp['passages'], *info)
            elif mode == 'QQQ': 
                temp_idx = self.__create_question(temp['questions'], *info)
            elif mode == 'OOO': 
                temp_idx = self.__create_options(temp['options'], *info)
            else:
                raise BuilderError(f"🚧 Unexpected token at line {temp_idx} of {filepath} : {lines[temp_idx]}")
            return temp_idx
        except BuilderError as e:
            self.success_flag = False
            print(e)
            temp_idx += 1
            while temp_idx < len(lines) and lines[temp_idx][:3] not in PARENT_DICT.keys():
                temp_idx += 1
            return temp_idx
    
    def __check(self, mode:str, temp:dict, temp_idx:int, lines:list[str], filepath:str):
        if mode not in PARENT_DICT.keys():
            raise BuilderError(f"🚧 Unexpected token at line {temp_idx} of {filepath} : {lines[temp_idx]}")
        if temp["type"] not in PARENT_DICT[mode]:
            raise BuilderError(f"🚧 Parsing failed at line {temp_idx} of {filepath} : {lines[temp_idx]}")
    
    def __create_group(self, temp:list, temp_idx:int, lines:list[str], filepath:str) -> int:
        new_group = {
            'type': 'group',
            'direction': [],
            'passages': [],
            'questions': [],
        }
        temp_idx += 1
        while temp_idx < len(lines) and lines[temp_idx][:3] not in STOPWORD_DICT['GGG']:
            temp_idx = self.__parse(temp=new_group, temp_idx=temp_idx, lines=lines, filepath=filepath)
        temp.append(new_group)
        return temp_idx
    
    ## TODO: Parsing out question numbers
    def __create_direction(self, temp:list, temp_idx:int, lines:list[str], filepath:str) -> int:
        temp_idx += 1
        while temp_idx < len(lines) and lines[temp_idx][:3] not in STOPWORD_DICT['DDD']:
            temp.append(lines[temp_idx])
            temp_idx += 1
        return temp_idx
    
    def __create_passage(self, temp:list, temp_idx:int, lines:list[str], filepath:str) -> int:
        new_passage = {
            'type': 'passage',
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
    
    def __create_question(self, temp:list, temp_idx:int, lines:list[str], filepath:str) -> int:
        new_question = {
            'type': 'question',
            'number': -1,           ## TODO: Parsing question numbers
            'weight': 10,           ## TODO: Parsing assigned score for each questions
            'direction' : [],
            'passages': [],
            'options': []
        }
        temp_idx += 1
        new_question['direction'].append(lines[temp_idx])
        temp_idx += 1
        while temp_idx < len(lines) and lines[temp_idx][:3] not in STOPWORD_DICT['QQQ']:
            temp_idx = self.__parse(temp=new_question, temp_idx=temp_idx, lines=lines, filepath=filepath)
        temp.append(new_question)
        return temp_idx
    
    ## TODO: Parsing out option numbers
    def __create_options(self, temp:list, temp_idx:int, lines:list[str], filepath:str) -> int:
        temp_idx += 1
        while temp_idx < len(lines) and lines[temp_idx][:3] not in STOPWORD_DICT['OOO']:
            temp.append(lines[temp_idx])
            temp_idx += 1
        return temp_idx
    
    def __save_as_json(self, filename:str, output_path:str, dataset:dict):
        filepath = os.path.join(output_path, f"{filename}.json")
        with open(filepath, 'w', encoding="UTF-8-SIG") as file:
            json.dump(dataset, file, indent=4)

    def __verify_and_summurize_result(self, filename:str, dataset:dict, width:int=80):
        issues = []
        print('=' * width)
        print(f"Build Result Summary of {filename} {'✅' if self.success_flag else '❌'}".center(width))
        print()
        print(f"<{len(dataset['contents'])} groups>".center(width))
        for i, group in enumerate(dataset['contents']):
            verificaiton_result = self.__verify_group(group, i)
            issues += verificaiton_result
            q_names = [str(q['number']) for q in group['questions']]
            print(f"{'❌' if verificaiton_result else '✅'} Group {str(i + 1).ljust(3)} : {', '.join(q_names)}")
        print()
        questions = list(chain(*[group['questions'] for group in dataset['contents']]))
        print(f"<{len(questions)} questions>".center(width))
        q_width = (width - 20) // 2
        for j, question in enumerate(questions):
            verificaiton_result = self.__verify_question(question, j)
            issues += verificaiton_result
            direction = question['direction'][0]
            print(f"{'❌' if verificaiton_result else '✅'} Q{str(j + 1).ljust(5)} ({len(question['passages'])}) {str(question['weight']).rjust(3)}pts   {direction[:q_width]}{'...' if len(direction) > q_width else ''}")
        print()
        print(f"<issues>".center(width))
        for issue in issues:
            print(issue)
        print()
        if issues:
            self.success_flag = False
        print(f"<stats>".center(width))
        print(f"Number of questions: {len(questions)}")
        print(f"Total score: {sum([q['weight'] for q in questions])}")
        print(f"Parsing Result: {'✅ Success' if self.success_flag else '❌ Error present'}")
        print('=' * width)

    def __verify_group(self, group:dict, group_idx:int) -> list[str]:
        issues = []
        if not group['direction']:
            issues.append(f"❌ Group {group_idx} : Empty direction!")
        if not group['passages']:
            issues.append(f"❌ Group {group_idx} : No passage present!")
        else:
            for p_idx, passage in enumerate(group['passages']):
                issues += self.__verify_passage(passage, f"Group {group_idx}, Passage {p_idx}")
        return issues
    
    def __verify_question(self, question:dict, q_idx:int) -> list[str]:
        issues = []
        if not question['direction']:
            issues.append(f"❌ Question {q_idx} : Empty direction!")
        if len(question['options']) != self.option_num:
            issues.append(f"❌ Question {q_idx} : {len(question['options'])} options are given where {self.option_num} are expected.")
        if question['passages']:
            for p_idx, passage in enumerate(question['passages']):
                issues += self.__verify_passage(passage, f"Question {q_idx}, Passage {p_idx}")
        return issues

    def __verify_passage(self, passage:dict, passage_name:str) -> list[str]:
        issues = []
        if not passage['paragraphs']:
            issues.append(f"❌ {passage_name} : Empty passage!")
        return issues


class BuilderError(Exception):
    ...