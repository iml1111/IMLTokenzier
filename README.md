# IMLTokenizer
**한국어를 위한 커스텀 형태소 분석기 Ver 1.0**입니다.

Konlpy-mecab 클래스를 상속받아 구현하였고, 형태소 분석기는 100%의 정확도 성능을 보여줄 수 없기에,

토큰화 과정에서 잘못 분석된 토큰에 대한 예외처리를 중심으로 추출기를 구현해보았습니다.



## Install Dependencies
**Supported: Xenial(16.04.3 LTS), Bionic(18.04.3 LTS), Disco(19.04), Eoan(19.10)**

```
$ ./requirements/requirements.sh
```



# Get Started

```python
from IMLTokenizer import Tokenizer
from IMLTokenizer import Refiner


msg = (
	"@%!@$% 아름다운 개는 짖는다."
	"사람은 밥을 먹는다. 커스터마이징,"
	" 그래디언트 디센트"
)

refiner = Refiner()
msg = refiner.char_filter(msg)

tokenizer = Tokenizer()
print(tokenizer.get_nouns(msg))
# ['개', '사람', '밥', '커스터마이징', '그래디언트', '디센트']
print(tokenizer.get_tokens(msg))
# ['아름다운', '개', '짖', '다', '사람', '밥', '먹', '다', '커스터마이징', '그래디언트', '디센트']
```



# References

https://konlpy.org/ko/latest/install/#ubuntu