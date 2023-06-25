# K-LLMSAT-PARSE

A helper module for efficient test parsing

## TODO
- [ ] Table Parsing
- [ ] Image Extraction

## How to Use

### STEP 0: Installation
`Poetry`를 활용해서 dependency를 관리하고 있습니다. `K-LLMSAT-PARSE` directory에서 dependency를 설치해주세요.
```
poetry install
```
### STEP 1: Extracting text from pdf files
이제 아래 예시와 같이 `resources` directory에 텍스트를 추출하고 싶은 pdf들을 배치합니다.  
반드시 `resources` 하부에 category를 나타내는 directory(이름은 자유)를 하나 만들고, 그 안에 pdf를 배치해주세요.
```
K-LLMSAT-PARSE
└── resources
    └── 수능
        └── 수능2306국어.pdf
        └── 수능2211국어.pdf
        └── ...
``` 
그 후 한 category 전체에 대해 extraction을 수행하고 싶으면,  
```
poetry run python extract.py 수능
```
개별 파일만 수행하고 싶으면  
```
poetry run python extract.py 수능 수능2306국어.pdf
```
와 같이 실행해주시면 됩니다.
`intermediaries/converted`에서 추출된 txt 파일을 확인하실 수 있습니다.  
### STEP 2: Manually format the text
이제 추출된 텍스트를 정해진 형식에 맞추어 수정해주어야 합니다.  
임시로 사용한 형식은 별도의 markdown에 서술했습니다.  
`example` directory에서 수정 예시를 확인하실 수 있습니다.  
완성된 txt 파일을 `intermediaries/parsed`에 아래 예시와 같이 배치해주세요.  
마찬가지로 category를 나타내는 directory(이름은 자유)를 하나 만들고, 그 안에 txt를 배치해주세요.
```
K-LLMSAT-PARSE
└── intermediaries
    └── parsed
        └── 수능
            └── 수능2306국어.txt
            └── 수능2211국어.txt
            └── ...
```
### STEP 3: Build JSON file from parsed txt files
한 category 전체에 대해 build를 수행하고 싶으면,
```
poetry run python build.py 수능
```
개별 파일만 수행하고 싶으면
```
poetry run python build.py 수능 수능2306국어.txt
```
와 같이 실행해주면 됩니다.  
제대로 parsing이 이루어졌는지 기초적인 확인을 해주는 summary도 console을 통해 제공되니 확인해보시면 됩니다.  
`results`에서 구축된 json 파일을 확인하실 수 있습니다.
### STEP 4: Render prompts from JSON
이제 JSON 파일로부터 LLM에 직접 제공할 수 있는 형태의 prompt를 생성합니다.  
이 부분은 `LangChain`을 이용해서 추후에 더 효율적으로 구현해야 할 것 같습니다. (지금은 PoC 느낌)  
(Parsing 팀과 Leaderboard 팀이 나누어지면 Step 3까지는 parsing 팀으로, Step 4는 leaderboard 팀으로 넘어갈 것 같습니다)  
임시로 사용한 prompt 형식은 별도의 markdown에 서술했습니다.
한 category 전체에 대해 rendering을 수행하고 싶으면,
```
poetry run python render.py 수능
```
개별 파일만 수행하고 싶으면
```
poetry run python render.py 수능 수능2306국어.json
```
와 같이 실행해주면 됩니다.
`prompts`에서 최종 prompt를 확인하실 수 있습니다.