# NounEx
**한국어를 위한 커스텀 명사 추출기**입니다.

Konlpy-mecab 클래스를 상속받아 구현하였고, 형태소 분석기는 100%의 정확도 성능을 보여줄 수 없기에,

토큰화 과정에서 잘못 분석된 토큰에 대한 예외처리를 중심으로 명사 추출기를 구현해보았습니다.



## Install Dependencies
**Supported: Xenial(16.04.3 LTS), Bionic(18.04.3 LTS), Disco(19.04), Eoan(19.10)**

```
$ ./requirements/requirements.sh
```



# Get Started

```python
>>> from tokenizer import NounEx
>>> obj = NounEx()
>>> msg = "사람은 밥을 먹는다"
>>> result = obj.get_tk(msg)
>>> result
['사람', '밥']
```



# References

https://konlpy.org/ko/latest/install/#ubuntu