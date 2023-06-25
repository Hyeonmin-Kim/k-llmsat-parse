# Parsing Rules (Tentative)

우선 시작하기에 앞서, pdf를 text로 추출하는 과정에서 불필요한 공백이 단어 사이에 삽입되는 경우가 많으므로 이 부분을 최대한 수정해주어야 합니다.  
PoC에서는 우선 한글 맞춤법 검사기를 통해 일일히 고쳐주었지만 LLM을 활용하는 게 더 좋을 수도 있겠네요. (TODO)

## Meta Tags
첫줄부터 빈 줄 없이 아래 예시처럼 meta 정보를 제공해줍니다.
```
default_q_weight: 2
option_num: 5
<START>
```
- `default_q_weight`는 별도로 문제의 배점을 제공하지 않았을 때 해당 문제에 배정하는 배점입니다.
- `option_num`는 한 문제가 가지는 선지의 개수입니다. (Parsing 결과를 검증할 때 사용합니다.)
- 마지막 `<START>`는 meta 정보가 끝이 났음을 표시해줍니다.

## Section Tags
아래 다섯 가지 tag를 규칙에 맞추어 집어넣어 줍니다.
- `GGG`: 지시 + 지문(1개 이상) + 질문(1개 이상)으로 이루어진 문제 묶음(`group`)의 시작부분
- `DDD`: `group`에 소속된 지시문
- `QQQ`: 문제(`question`)의 시작부분
- `PPP`: `group`이나 `question`에 소속된 지문의 시작부분
- `OOO`: `question`에 소속된 선지들의 시작부분  

참고로, `QQQ`의 경우에는 아래와 같이 문제 번호(필수), 배점(선택)을 입력할 수 있습니다.
```
QQQ 1 (3)  # 1번 문제 시작, 배점 3점
QQQ 2      # 2번 문제 시작, 배점은 meta 부분에서 준 default_q_weight
```
또한 `PPP`의 경우에도 지문의 이름을 선택적으로 입력할 수 있습니다.  
(문제의 지시문에서 지문을 이름으로 지칭하는 경우가 있어서 이름이 있다면 이름을 넣어주어야 합니다.)  
```
PPP        # 지문 시작, 이름 없음
PPP <보기>  # 지문 시작, 지문 이름은 <보기>
```

## Decoration Tags
이제 뜻을 가진 서식을 표현해줍니다.
### Region Tags
아래와 같이 특정 구역을 지시하는 서식들을 표현해줍니다.

- `highlight` : 예를 들어, 무언가를 기억하는 사람은 자기의 기억이 무엇인지 <u>ⓓ알아보기</u> 위해 아무것에도 의존할 필요가 없다.  
- `region` :   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;┌─  독서의 ‘때문에 동기’는 독서 행위를 하게 만든 이유를  
[A]│  의미한다. 이는 독서 행위를 유발한 계기가 되므로 독서  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;└─ 이전 시점에 이미 발생한 사건이나 경험에 해당한다.
- `square` : 이미 그 속에 가 있었기에 `의리`를 `이욕`에 빼앗겨서 초연히 버리고 돌아오지 못하였다. (네모 표시)

이런 서식은 아래와 같이 구역 이름이 포함되도록 표시해줍니다. (`square`와 같은 경우는 그냥 번호를 붙여줍니다.)
```
자기의 기억이 무엇인지 hⓓhh알아보기hhh 위해 아무것에도
r[A]rr독서의 ‘때문에 동기’는 ... 경험에 해당한다.rrr
이미 그 속에 가 있었기에 s1ss의리sss를 s2ss이욕sss에 빼앗겨서
```
### Style Tags
아래와 같이 시각적인 강조효과(`bold`, `italic`, `underline`, `deleteline`)를 주는 서식들을 표현해줍니다.
```
bb굵은 글씨bbb
ii기울인 글씨iii
uu밑줄 글씨uuu
dd취소선 글씨ddd
```

## Images
이미지는 아래와 같이 직접 대체 텍스트를 입력해줍니다.  
Image 문제를 완전히 제외할지, 대체 텍스트를 붙인다면 대체 텍스트 생성 시 규칙들도 논의해볼 지점인 것 같습니다.
```
III 가로축이 흡착 세기(오른쪽으로 갈수록 강해짐), 세로축이 촉매 활성(위로 갈수록 높아짐)인 산점도이다. 산점도 위에 여러 점들이 있는데, 점 ⓐ, ⓑ, ⓒ는 순서대로 원점으로부터 오른쪽 위 방향으로 점차 멀어지도록 찍혀 있다. 점 ⓓ는 점 ⓒ보다 더 오른쪽에 있지만 높이만 봤을 때에는 점 ⓐ보다도 살짝 낮은 위치에 찍혀있다.
```

## Tables
TBD